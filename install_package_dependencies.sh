#This script can be used to install all the required package dependencies on a clean system

PROJECT_PATH=$(pwd)

# Install Python-PIP
sudo apt-get update
sudo apt-get install -y python-pip

# Install virtualenv, create a virtual environment and activate it
sudo -H pip3 install virtualenv
virtualenv env
source env/bin/activate


# Install Graph-Tool
sudo apt-get install -y expat
sudo apt-get install -y libsparsehash-dev
sudo apt-get install -y gtk+3
sudo apt-get install -y libboost-all-dev
sudo apt-get install -y build-essential
sudo apt-get install -y libcairo2-dev
sudo apt-get install -y gfortran libopenblas-dev liblapack-dev
sudo apt-get install -y libcgal-dev
sudo apt-get install -y graphviz graphviz-dev libgraphviz-dev pkg-config
pip3 install pycairo

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

# install nltk corpus wordnet
python3 -m nltk.downloader wordnet

# Install python packages
cd "$PROJECT_PATH"
cd ..
pip3 install -r requirements.txt
deactivate