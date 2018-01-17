# This script can be used to install all the required package dependencies on a clean system
# Run this file as . install_package_dependencies_for_virtualenv.sh to retain the virtual environment after the execution of this file

PROJECT_PATH=$(pwd)

# Install Python-PIP
sudo pip3 install --upgrade pip

# Install virtualenv, create a virtual environment and activate it
sudo pip3 install virtualenv
virtualenv env
source env/bin/activate

# Install Graph-Tool
pip3 install pycairo
echo 'deb http://downloads.skewed.de/apt/xenial xenial universe' | sudo tee -a  /etc/apt/sources.list 
echo 'deb-src http://downloads.skewed.de/apt/xenial xenial universe' | sudo tee -a  /etc/apt/sources.list 
sudo apt-get update
sudo apt-get install -y --allow-unauthenticated python3-graph-tool

# Install Infomap Community Detection
pip3 install swiglpk
mkdir Infomap
cd Infomap
wget http://www.mapequation.org/downloads/Infomap.zip
unzip Infomap.zip
make
cd examples/python
make python3
python3 example-networkx.py

# For installation(pip) Python-iGraph
pip3 install igraph

# Install python packages
cd "$PROJECT_PATH"
cd ..
pip3 install -r requirements.txt
