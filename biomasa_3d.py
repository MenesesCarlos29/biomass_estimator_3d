import open3d as o3d
import numpy as np
from typing import Tuple, Optional

def generate_synthetic_bush(n_points: int = 2000) -> o3d.geometry.PointCloud:
    """
    Generates a synthetic point cloud resembling a bush using Gaussian distributions.
    Includes random noise to simulate sensor artifacts.
    """
    clusters = [
        np.random.normal(loc=[0, 0, 0], scale=0.15, size=(n_points // 2, 3)),
        np.random.normal(loc=[-0.2, 0.1, 0.1], scale=0.10, size=(n_points // 4, 3)),
        np.random.normal(loc=[0.2, 0.15, -0.1], scale=0.10, size=(n_points // 4, 3))
    ]
    points = np.concatenate(clusters)

    # Add sensor noise (outliers)
    noise = np.random.uniform(low=-1, high=1, size=(50, 3))
    all_points = np.concatenate([points, noise])

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(all_points)
    pcd.paint_uniform_color([0, 0.4, 0]) # Dark Green
    
    return pcd

def preprocess_point_cloud(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
    """
    Applies Statistical Outlier Removal (SOR) to clean sensor noise.
    """
    # nb_neighbors=20, std_ratio=2.0 are standard empirical values for vegetation
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    clean_pcd = pcd.select_by_index(ind)
    
    print(f"Preprocessing: Removed {len(pcd.points) - len(clean_pcd.points)} noise points.")
    return clean_pcd

def calculate_biomass_volume(pcd: o3d.geometry.PointCloud) -> Tuple[float, o3d.geometry.TriangleMesh]:
    """
    Computes the Convex Hull of the point cloud to estimate volumetric biomass.
    Returns the volume (m3) and the mesh for visualization.
    """
    hull_mesh, _ = pcd.compute_convex_hull()
    
    # Check if hull is watertight for accurate volume calculation
    if hull_mesh.is_watertight():
        volume = hull_mesh.get_volume()
    else:
        # Fallback for non-watertight meshes (rare with Convex Hull)
        volume = 0.0
        print("Warning: Generated hull is not watertight.")

    return volume, hull_mesh

def visualize_results(pcd: o3d.geometry.PointCloud, hull_mesh: o3d.geometry.TriangleMesh):
    """
    Renders the point cloud and the wireframe of the convex hull.
    """
    # Create a wireframe for the hull to visualize the enclosure without hiding points
    hull_wireframe = o3d.geometry.LineSet.create_from_triangle_mesh(hull_mesh)
    hull_wireframe.paint_uniform_color([1, 0, 0]) # Red for the bounding volume

    o3d.visualization.draw_geometries(
        [pcd, hull_wireframe], 
        window_name="Farm3 Demo: Biomass Estimation",
        width=1024, height=768,
        left=50, top=50
    )

if __name__ == "__main__":
    print("--- 3D Biomass Estimation PoC ---")
    
    # 1. Data Ingestion
    raw_pcd = generate_synthetic_bush()
    
    # 2. Preprocessing
    clean_pcd = preprocess_point_cloud(raw_pcd)
    
    # 3. Analysis (Convex Hull)
    volume, hull_mesh = calculate_biomass_volume(clean_pcd)
    
    print(f"Estimated Volumetric Biomass: {volume:.4f} m3")
    print(f"Note: Volume serves as a proxy for fresh weight in yield prediction models.")
    
    # 4. Visualization
    visualize_results(clean_pcd, hull_mesh)