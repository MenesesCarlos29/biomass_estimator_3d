# 3D Biomass Estimation: Point Cloud Analysis

## Project Overview
This repository contains a Proof of Concept (PoC) for non-invasive plant phenotyping within the context of Precision Agriculture. The project demonstrates the application of computational geometry to estimate crop biomass using 3D Point Cloud data.

In vertical farming and automated greenhouse environments, correlating geometric volume with biological mass is critical for non-destructive Yield Prediction. This pipeline simulates the acquisition of sensor data (LiDAR/Depth Camera), cleanses the input, and calculates volumetric metrics using a Convex Hull algorithm.

## Technical Methodology
The pipeline is structured into three distinct stages:

1.  **Synthetic Data Generation:**
    Simulates organic plant structures using Gaussian distribution clusters to model foliage. Random noise is injected into the dataset to replicate common sensor artifacts found in real-world agricultural deployments.

2.  **Preprocessing (Denoising):**
    Implementation of **Statistical Outlier Removal (SOR)**. This step filters out noise (e.g., dust, flying insects, sensor errors) based on the mean distance to neighboring points. This is a critical data hygiene step, as outliers can significantly skew volumetric calculations.

3.  **Biometric Estimation (Convex Hull):**
    The system computes the Convex Hull of the cleaned point cloud.
    * **Algorithm Choice:** The Convex Hull was selected over Voxel Grids for its computational efficiency O(n log n) and its robustness as a standard proxy for "Fresh Weight" (biomass) in agronomic studies.

## Visualization
The image below illustrates the output of the pipeline: the cleaned synthetic plant (Green) enclosed by the calculated Convex Hull wireframe (Red), representing the estimated volume.

![Biomass Estimation Preview](demo_preview.png)

## Installation and Usage

### Prerequisites
* Python 3.8+
* Open3D
* NumPy

### Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/3d-biomass-estimation.git](https://github.com/YOUR_USERNAME/3d-biomass-estimation.git)
    cd 3d-biomass-estimation
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the estimation script:**
    ```bash
    python biomass_estimator.py
    ```

## Project Structure
* `biomass_estimator.py`: Main execution script containing the generation, cleaning, and analysis logic.
* `requirements.txt`: List of necessary Python libraries.
* `demo_preview.png`: Visualization artifact of the model output.

## Key Competencies
* **3D Computer Vision:** Manipulation and visualization of Point Cloud data using Open3D.
* **Data Preprocessing:** Implementation of statistical filters for sensor noise reduction.
* **Computational Geometry:** Application of Convex Hull algorithms for biological volume estimation.
