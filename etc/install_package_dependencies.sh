# This script can be used to install all the required package dependencies on a clean system

PROJECT_PATH=$(pwd)

# Install Python-PIP
sudo apt-get update
sudo apt-get install -y python-pip


# Install Graph-Tool
sudo apt-get install -y expat
sudo apt-get install -y libsparsehash-dev
sudo apt-get install -y gtk+3
sudo apt-get install -y libboost-all-dev
sudo apt-get install -y build-essential
sudo apt-get install -y libcairo2-dev
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-matplotlib
sudo apt-get install -y gfortran libopenblas-dev liblapack-dev
sudo apt-get install -y libcgal-dev
sudo apt-get install -y python3-numpy
sudo apt-get install -y python2.7-config
sudo apt-get install -y python3-cairo
sudo apt-get install -y python3-scipy
sudo apt-get install -y graphviz graphviz-dev libgraphviz-dev pkg-config
sudo apt-get install -y python3-pygraphviz

echo 'deb http://downloads.skewed.de/apt/xenial xenial universe' | sudo tee -a  /etc/apt/sources.list
echo 'deb-src http://downloads.skewed.de/apt/xenial xenial universe' | sudo tee -a  /etc/apt/sources.list
sudo apt-get update
sudo apt-get install -y --allow-unauthenticated python3-graph-tool

# Update pip
pip3 install --upgrade pip
sudo -H pip3 install --upgrade pip

# Install Infomap Community Detection
sudo apt-get install -y swig
mkdir Infomap
cd Infomap
wget http://www.mapequation.org/downloads/Infomap.zip
unzip Infomap.zip
make
cd examples/python
make python3
python3 example-networkx.py

# For installation(pip) of PyGraphViz
sudo apt-get install graphviz libgraphviz-dev pkg-config

# For installation(pip) Python-iGraph
sudo apt-get install -y libxml2-dev libigraph0-dev

# Install python packages
cd "$PROJECT_PATH"
cd ..
sudo -H pip3 install -r requirements.txt
