# GeoDesign EarthEngine Workflows

This repo contains EarthEngine work flows to be shared, used, and re-used by 
Conservation tech

## (GDE) Raster statistics

Extract raster stats from Google EarthEngine using a shapefile on disk

### Steps

Please try to replicate and file issue when you get stuck.

#### 1. Create conda environment

This step does NOT have been repeated every single time you work on the 
project

- Open your Conda enabled shell (Windows: in the Anaconda/Miniconda/Conda 
folder of the start menu)

- Git clone this repo (make sure Git is installed):
    ```
    git clone https://github.com/tnc-ca-geo/ee_workflows.git
    ```

- Install conda environment:
    
    - change directory (cd) into the ee_workflows folder created by the prior 
    step
    
    - run
    ```
    conda create environment.yml
    ```

#### 2. Activate environment

Before ever time you work on the project

- Activate the conda environment created above
    
  ```
  conda activate ee_workflows
  ```
