# TNC California Conservation Technology EarthEngine Workflows

This repository contains EarthEngine work flows to be shared, used, 
and re-used by Conservation tech

## Preparation (for all examples)

Please try to replicate and create Github issues whenever you get 
stuck. The goal is to have a tutorial that is easy to reproduce. Getting stuck
will reflect on me, my writing, or my implicit assumptions.

#### 1. Create a conda environment

Performan this step only once to get started with the project, everything
created here will persist on your system unless explicitely deleted:

- Open your Conda enabled terminal (Windows: Cmd symbol in 
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
    
    - create environment from the environment definition in this repository
    
    ```
    conda env create -f environment.yml     
    ```

#### 2. Activate and update the environment and update code

Every time you work on the project

- Open a conda-enabled terminal

- Activate the conda environment created above
    
  ```
  conda activate ee_workflows
  ```
  
 - It might be necessary to update the conda environment
 
 ```
 conda env create -f environment.yml
 ```
 
 - Pull the newest changes fom Github
 
    - change into the root directory of this project and call
    
    ```
    git pull origin master
    ```
    
#### 3. Proceed to example projects


