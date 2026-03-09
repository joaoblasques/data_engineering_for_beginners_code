
# Data Engineering for Beginners 

The code for SQL, Python, and data model sections are written using Spark SQL. To run the code, you will need the prerequisites listed below.

## Setup 

**Prerequisites**

1. [git version >= 2.37.1](https://github.com/git-guides/install-git)
2. [Docker version >= 20.10.17](https://docs.docker.com/engine/install/) and [Docker compose v2 version >= v2.10.2](https://docs.docker.com/compose/#compose-v2-and-the-new-docker-compose-command).

**Windows users**: please setup WSL and a local Ubuntu Virtual machine following **[the instructions here](https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview)**. 

Install the above prerequisites on your ubuntu terminal; if you have trouble installing docker, follow **[the steps here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04#step-1-installing-docker)** (only Step 1 is necessary). 

Fork this repository **[data_engineering_for_beginners_code](https://github.com/josephmachado/data_engineering_for_beginners_code/tree/main?tab=readme-ov-file#setup)**.                                                                      
![GitHub Fork](./images/fork.png)
After forking, clone the repo to your local machine and start the containers as shown below:

```bash
# Replace your-user-name with your github username
git clone https://github.com/your-user-name/data_engineering_for_beginners_code.git 
cd data_engineering_for_beginners_code
docker compose up -d --build 
sleep 30 
```

Open Jupyter Lab at [http://localhost:8888](http://localhost:8888) and run the code at [./notebooks/starter-notebook.ipynb](./notebooks/starter-notebook.ipynb) to create the data and check that your setup worked.


After the data is created open the Airflow UI with [http://localhost:8080/](http://localhost:8080/) and trigger the DAG and ensure that it runs successfully.

## Shut down

After you are done, shut down the containers with 

```bash 
docker compose down -v
```

