import open3d as o3d
import numpy as np
from typing import Tuple

def generate_synthetic_bush(n_points: int = 2000) -> o3d.geometry.PointCloud:
    """
    Generates a synthetic point cloud resembling a bush using Gaussian distributions.
    Includes random noise to simulate sensor artifacts.
    """
    # Generate main foliage clusters
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
    
    # Default color: Dark Green
    pcd.paint_uniform_color([0, 0.4, 0])
    
    return pcd

if __name__ == "__main__":
    print("--- 3D Biomass Estimation PoC ---")
    pcd = generate_synthetic_bush()
    print(f"Generated point cloud with {len(pcd.points)} points.")
    
    # Quick visualization check
    o3d.visualization.draw_geometries([pcd], window_name="Raw Data Check")