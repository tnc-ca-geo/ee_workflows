# GeoDesign EarthEngine Workflows

This repository contains EarthEngine work flows to be shared, used, 
and re-used by Conservation tech

## (GDE) Raster statistics

Extract raster statistics from Google EarthEngine Image using a 
shapefile on a local disk

Please try to replicate and file an Github issue whenever you get 
stuck in order to improve this documentation and make the project full 
portable.

### Preparation

#### 1. Create a conda environment

This step has performanced only once to get started with the project:

- Open your Conda enabled shell (Windows: Cmd symbol in 
the Anaconda/Miniconda/Conda directory of the start menu). 
The prompt inidicating that you are in the conda base environment 
should look something like this:
  
  ```
  (base) C:/{...}
  ```


- Git clone this repo (make sure Git is installed) in a directory (wherever
you would like to store it):
    
    ```
    git clone https://github.com/tnc-ca-geo/ee_workflows.git
    ```

- Install the conda environment defined within this project:
    
    - change directory (cd) to the ee_workflows folder created by git clone
    
    - run
    ```
    conda create environment.yml
    ```

#### 2. Activate environment

Before every time you work on the project

- Activate the conda environment created above
    
  ```
  conda activate ee_workflows
  ```
