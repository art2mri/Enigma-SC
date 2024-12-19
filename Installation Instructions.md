# Installation Instructions

## 1) System Requirements  

- To install **Enigma-SC** at least 40 GB of free space is required in your hard disk.    

- This software has been tested on Ubuntu 20.04, Ubuntu 20.10 and Ubuntu 22.04.

- The **Enigma-SC** fundamentally runs its application on top of other tools, so it's necessary for the user to install of the following applications:
  
  **I)** Python 3.11.5 - [Installation](https://www.python.org/downloads/)
  
  **II)** Docker Engine - [Installation](https://docs.docker.com/engine/install/ubuntu/)  
   **OR**  
  Singularity - [Installation](https://github.com/apptainer/singularity/blob/master/INSTALL.md)  
   **OR**  
  Apptainer - [Installation](https://apptainer.org/docs/user/latest/quick_start.html#quick-installation)

  **III)** CUDA Container Toolkit [Installation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)  

- We strongly reccomend the GPU integration for optimizing the prediction time of the pipeline. However, inference times are typically still manageable on CPU and MPS (Apple M1/M2). If using a GPU, it should have at least 4 GB of available (unused) VRAM.    

## 2) Download and Install Enigma-SC 

### Installing Enigma-SC

To download and install Enigma-SC, open a terminal and type:  
  
```bash
git clone https://github.com/art2mri/Enigma-SC.git  
chmod -R 777 Enigma-SC/Enigma-SC.sh
```   
 
 It will clone all the Enigma-SC repository files to an Enigma-SC folder that will be created in your computer. **NOTE: Please don't rename the Enigma-SC folder, because this will cause issues while running the pipeline later. You can move the entire folder to any other locations, but never changing its name**.

 ### Installing virtual environment to run Enigma-SC GUI 

 Inside of the **Enigma-SC** folder, open a terminal and type the following commands:  

 ```bash
pip install virtualenv
```
 ```bash
apt install python3-venv
```
 ```bash
python3.11 -m venv venv
```
 ```bash
source venv/bin/activate
```
 ```bash
pip install Pillow
```
 ```bash
pip3 install tkfilebrowser
```
 ```bash
apt-get install python3-tk
```
 ```bash
deactivate
```

**If you couldn't install the packages above due to permission problems, you can run the pipeline via command line, please check the section 4) Running Enigma-SC** and no packages need to be installed.  

[command line tutorial](/command%20line%20TUTORIAL.md)  

## 3) Docker and Singularity Containers  

- You don't necessarily need to install both of these applications; you can choose to install one of them to run the spinal cord vertebral labeling. The containers will be automatically initialized from an existing Docker image that is already available on [DockerHub](https://hub.docker.com/repository/docker/art2mri/vertebral_labeling/general).

  ### Docker
  
  If you have already correctly installed the Docker Engine, run the following command on Linux Terminal:
   - ```bash
     docker pull art2mri/vertebral_labeling:3.0
     ```
  Adding a user to the docker group grants significant permissions, equivalent to root access, because the Docker daemon (dockerd) runs as root. Ensure you trust the users you are adding to   
  the docker group:
  
   - ```bash
     sudo groupadd docker
     ```
     
   - ```bash
     sudo groupadd docker
     ```     
  ### Singularity

  If you have correctly installed Singularity, open the Linux terminal **inside of the Enigma-SC folder** and run the following command:
  - ```bash
    singularity build --sandbox vertebral_labeling.simg docker://art2mri/vertebral_labeling:3.0
    ```
  - ```bash
    chmod -R 777 vertebral_labeling.simg
    ```

  ### Apptainer

  If you have correctly installed Apptainer, open the Linux terminal **inside of the Enigma-SC folder** and run the following command:
  - ```bash
    apptainer build --sandbox vertebral_labeling.simg docker://art2mri/vertebral_labeling:3.0
    ```
  - ```bash
    chmod -R 777 vertebral_labeling.simg
    ```  
  - After that, a folder named ***vertebral_labeling.simg*** will appear on the **Enigma-SC** folder. Please don't rename it.  
  

## 4) Running Enigma-SC  

To run the **Enigma-SC** software and open the interface, open a terminal **inside of the Enigma-SC folder** and type:  

 ```bash
source venv/bin/activate  
./Enigma-SC.sh
```
If you are running **Enigma-SC** in a server, or if you couldn`t install all the packages listed on the section **2) Download and Install Enigma-SC**, you can run the pipeline without opening the GUI, via command line, by opening a terminal **inside of the Enigma-SC folder** and typing:  

 ```bash 
./nographmode.sh
```  
[command line tutorial](/command%20line%20TUTORIAL.md)  
 
## 5) Uninstalling Enigma-SC     
 






  
   
  

  

  
