# This script can be used to install all the required package dependencies on a clean virtualenv
PROJECT_PATH=$(pwd)

# Install Python-PIP
pip2 install pip

# Install Graph-Tool
pip install expatriate
pip install sparsehash
pip install pycairo
pip install --upgrade pip
pip install dev
pip install matplotlib 
pip install numpy
pip2 install --pre config 
pip install scipy

echo 'deb http://downloads.skewed.de/apt/xenial xenial universe' | sudo tee -a  /etc/apt/sources.list 
echo 'deb-src http://downloads.skewed.de/apt/xenial xenial universe' | sudo tee -a  /etc/apt/sources.list 
sudo apt-get install -y --allow-unauthenticated python3-graph-tool


# Update pip
pip3 install --upgrade pip

# Install Infomap Community Detection
pip install swiglpk
mkdir Infomap
cd Infomap
wget http://www.mapequation.org/downloads/Infomap.zip
unzip Infomap.zip
make
cd examples/python
make python3
python3 example-networkx.py

# For installation(pip) of PyGraphViz
pip install pygraphviz

# For installation(pip) Python-iGraph
pip install igraph

# Install python packages
cd "$PROJECT_PATH"
cd ..
pip3 install -r requirements.txt
