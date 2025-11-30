import open3d as o3d
import numpy as np
from typing import Tuple

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
    pcd.paint_uniform_color([0, 0.4, 0])
    
    return pcd

def preprocess_point_cloud(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
    """
    Applies Statistical Outlier Removal (SOR) to clean sensor noise.
    """
    # nb_neighbors=20, std_ratio=2.0 are standard empirical values for vegetation
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    
    clean_pcd = pcd.select_by_index(ind)
    
    # Visual feedback: Original noise points count
    noise_count = len(pcd.points) - len(clean_pcd.points)
    print(f"Preprocessing complete. Removed {noise_count} outlier points.")
    
    return clean_pcd

if __name__ == "__main__":
    print("--- 3D Biomass Estimation PoC ---")
    
    # 1. Generation
    raw_pcd = generate_synthetic_bush()
    
    # 2. Preprocessing
    clean_pcd = preprocess_point_cloud(raw_pcd)
    
    # Visual check: Cleaned data
    o3d.visualization.draw_geometries([clean_pcd], window_name="Cleaned Data Check")