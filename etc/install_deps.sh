#!/bin/bash
#This script can be used to install all the required package dependencies on a clean system
 
PROJECT_PATH=$(pwd)
REQUIREMENTS_FILE="$(pwd)/requirements.txt"

# Install Python
sudo apt-get update
sudo apt-get install -y python3.5
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-pip

# Install venv, create a virtual environment and activate it
sudo apt-get install -y python3-venv
python3 -m venv .env
source .env/bin/activate


# Install Graph-Tool
sudo apt-get install -y expat
sudo apt-get install -y libsparsehash-dev
sudo apt-get install -y libboost-all-dev
sudo apt-get install -y libcairo2-dev
sudo apt-get install -y gfortran libopenblas-dev liblapack-dev
sudo apt-get install -y libcgal-dev
sudo apt-get install -y graphviz graphviz-dev libgraphviz-dev pkg-config
pip3 install wheel
pip3 install pycairo

echo 'deb http://downloads.skewed.de/apt/xenial xenial universe' | sudo tee -a  /etc/apt/sources.list
echo 'deb-src http://downloads.skewed.de/apt/xenial xenial universe' | sudo tee -a  /etc/apt/sources.list
sudo apt-get update
sudo apt-get install -y --allow-unauthenticated python3-graph-tool

# Update pip
pip3 install --upgrade pip
sudo -H pip3 install --upgrade pip


# Install igraph
sudo apt-get install -y build-essential libxml2-dev
sudo apt-get -y install libigraph-dev


# Install python packages
pip3 install -r "$REQUIREMENTS_FILE"

# Install Infomap Community Detection
sudo apt-get install -y swig
mkdir Infomap
cd Infomap
wget http://www.mapequation.org/downloads/Infomap.zip
unzip Infomap.zip
rm Infomap.zip
make
cd examples/python
make python3

# Install nltk corpus wordnet
python3 -m nltk.downloader wordnet

deactivate

cd $PROJECT_PATH
