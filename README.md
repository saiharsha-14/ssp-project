# New York Taxi Fare Scalable Analysis

This project involves a scalable analysis of the New York City Taxi Fare dataset using Apache Hadoop and Apache Spark. The project includes clustering analysis and MapReduce operations on large-scale data, leveraging distributed computing environments.

## Table of Contents

- [Overview](#overview)
- [Installation Requirements](#installation-requirements)
- [Setup Instructions](#setup-instructions)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [UI Access](#ui-access)
- [Acknowledgements](#acknowledgements)

## Overview

This project analyzes New York City Taxi Fare data, focusing on clustering techniques to extract meaningful patterns. The data is processed using Spark's MLlib for clustering and Hadoop's MapReduce for distributed data processing. Visualization of results is done using Plotly.

## Installation Requirements

To run this project, ensure you have the following installed:

1. **Hadoop 3.3.6**
2. **Apache Spark 3.5.1**
3. **Java 11** (OpenJDK & Default JRE)
4. **Python 3.x**
5. **pip** (Python package installer)
6. Python libraries:
   - **pandas**: `pip install pandas`
   - **plotly**: `pip install plotly`
   - **pyspark**: `pip install pyspark`
   - **kaleido**: `pip install kaleido`

## Setup Instructions

Follow these steps to set up the environment on three Ubuntu VMs:

1. **Create 3 Ubuntu VMs**: 
   - `ssp-master`
   - `ssp-worker-1`
   - `ssp-worker-2`

2. **Install Java**:
   ```bash
   sudo apt update
   sudo apt install default-jre
   sudo apt install default-jdk
   ```

3. **Modify `/etc/hosts` file**: Remove the `localhost` entry and add the hostname beside the internal IP.

4. **Create Hadoop User**:
   ```bash
   sudo groupadd hadoop
   sudo useradd -g hadoop hduser -m -s /bin/bash
   sudo passwd hduser
   sudo usermod -aG sudo hduser
   su - hduser
   ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
   cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
   ssh-copy-id username@hostname  # Replace with the hostname of other VMs
   ```

5. **Disable IPv6**:
   ```bash
   sudo vim /etc/sysctl.conf
   ```
   Add the following lines:
   ```bash
   net.ipv6.conf.all.disable_ipv6=1
   net.ipv6.conf.default.disable_ipv6=1
   net.ipv6.conf.lo.disable_ipv6=1
   ```
   Then apply the changes:
   ```bash
   sudo sysctl -p
   ```

6. **Download and Install Hadoop and Spark**:
   ```bash
   cd ~
   curl -O http://ftp.heanet.ie/mirrors/www.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
   curl -O https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
   sudo tar xvf hadoop-3.3.6.tar.gz -C /usr/local/
   sudo tar xvf spark-3.5.1-bin-hadoop3.tgz -C /usr/local/
   sudo ln -s /usr/local/hadoop-3.3.6 /usr/local/hadoop
   sudo ln -s /usr/local/spark-3.5.1-bin-hadoop3 /usr/local/spark
   sudo chown -R hduser:hadoop /usr/local/hadoop*
   sudo chown -R hduser:hadoop /usr/local/spark*
   ```

7. **Configure Environment Variables**:
   ```bash
   vi /home/hduser/.bashrc
   ```
   Add the following lines:
   ```bash
   export HADOOP_CLASSPATH=/usr/lib/jvm/java-11-openjdk-amd64/lib/tools.jar:/usr/local/hadoop/bin/hadoop
   export HADOOP_MAPRED_HOME=/usr/local/hadoop
   export HADOOP_HDFS_HOME=/usr/local/hadoop
   export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
   export PATH=$PATH:/usr/lib/jvm/java-11-openjdk-amd64/bin:/usr/local/hadoop/bin
   export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
   export LD_LIBRARY_PATH=/usr/local/hadoop/lib/native:$LD_LIBRARY_PATH
   export SPARK_HOME=/usr/local/spark
   export PYSPARK_PYTHON=python3
   export PATH=$SPARK_HOME/bin:$PATH
   export PATH=$PATH:/home/hduser/.local/bin
   ```
   Apply the changes:
   ```bash
   source /home/hduser/.bashrc
   ```

8. **Configure Hadoop and Spark**:
   - Modify the following configuration files located in `/usr/local/hadoop/etc/hadoop/`:
     - `core-site.xml`
     - `hdfs-site.xml`
     - `mapred-site.xml`
   - Add `JAVA_HOME` to `hadoop-env.sh`:
     ```bash
     export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
     ```

9. **Create Necessary Directories**:
   ```bash
   mkdir ~/tmp
   mkdir ~/hdfs
   chmod 750 ~/hdfs
   ```

10. **Format NameNode and Start DFS/YARN**:
    ```bash
    cd /usr/local/hadoop
    bin/hdfs namenode -format  # Run on all VMs
    sbin/start-dfs.sh  # Run on ssp-master VM
    sbin/start-yarn.sh  # Run on ssp-master VM
    hdfs --daemon start datanode  # Run on ssp-worker-1 and ssp-worker-2 VMs
    ```

11. **Configure Spark**:
    - Modify `spark-env.sh` with internal and external IPs located in `/usr/local/spark/conf/`.
    - Start Spark on all VMs:
      ```bash
      cd /usr/local/spark
      sbin/start-master.sh  # On ssp-master VM
      sbin/start-worker.sh spark://ssp-master:7077  # On all VMs
      ```

12. **Set Up Jupyter Notebook as a Service**:
    ```bash
    pip3 install jupyter
    jupyter notebook --generate-config
    jupyter notebook password
    vi ~/.jupyter/jupyter_notebook_config.py
    ```
    Add the following:
    ```bash
    c.NotebookApp.ip = '0.0.0.0'
    c.NotebookApp.open_browser = False
    c.NotebookApp.port = 8888
    ```
    Create a service file:
    ```bash
    vi /etc/systemd/system/jupyter.service
    ```
    Add the following:
    ```bash
    [Unit]
    Description=Jupyter Notebook

    [Service]
    Type=simple
    PIDFile=/run/jupyter.pid
    ExecStart=/usr/local/bin/jupyter-notebook --no-browser --port=8888 --ip=0.0.0.0 --allow-root
    WorkingDirectory=/root
    User=root
    Group=root
    Restart=always
    RestartSec=10

    [Install]
    WantedBy=multi-user.target
    ```
    Restart the Jupyter service:
    ```bash
    sudo systemctl restart jupyter
    ```

## Dataset

The dataset used in this project is the New York City Taxi Fare Prediction dataset, available on Kaggle:

[New York City Taxi Fare Prediction Dataset](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction/data?select=train.csv)

## Project Structure

- **avg_fare_by_passengers_count.py**: MapReduce job to calculate the average fare by passenger count.
- **total_fare_per_year.py**: MapReduce job to compute the total fare collected per year.
- **avg_fare_by_location.py**: MapReduce job to calculate the average fare by pickup location.
- **mrjob_visualization.py**: Script to visualize the results using Plotly.
- **cluster_analysis.py**: Spark job for clustering analysis using KMeans and BisectingKMeans.
- **README.md**: Project documentation and setup instructions.

## Usage

1. Ensure all setup instructions are completed on all VMs.
2. Run the Hadoop and Spark services as per the instructions.
3. Execute the Python scripts for data analysis and visualization.
4. Access the Jupyter Notebook interface to interactively work with the data.

## UI Access

- **Hadoop**: `http://external_ip:9870`
- **Spark**: `http://external_ip:8080`
- **Jupyter**: `http://external_ip:8888`

## Acknowledgements

This project is part of the Scalable Systems Programming course for the MSc in Data Analytics at the National College of Ireland.