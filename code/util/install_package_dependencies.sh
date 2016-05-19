# This script can be used to install all the required package dependencies on a clean system

# Install Python-PIP
sudo apt-get install python-pip

# Install NetworkX
pip3 install networkx

# Install Python-iGraph
sudo apt-get install libxml2-dev
pip3 install python-igraph

# Install Graph-Tool
sudo apt-get install expat
sudo apt-get install libsparsehash-dev
sudo apt-get install gtk+3
sudo apt-get install libboost-all-dev
sudo apt-get install graphviz
sudo apt-get install build-essential
sudo apt-get install libcairo2-dev
sudo apt-get install python3-pip
sudo apt-get install python3-dev
sudo apt-get install python3-matplotlib
sudo apt-get install gfortran libopenblas-dev liblapack-dev
sudo apt-get install libcgal-dev
sudo apt-get install python3-numpy
sudo apt-get install python2.7-config
sudo apt-get install python3-cairo
sudo apt-get install python3-scipy
echo 'deb http://downloads.skewed.de/apt/wily wily universe' | sudo tee -a  /etc/apt/sources.list
echo 'deb-src http://downloads.skewed.de/apt/wily wily universe' | sudo tee -a  /etc/apt/sources.list
sudo apt-get update
sudo apt-get install python3-graph-tool

# Install GraphViz
wget "http://www.graphviz.org/pub/graphviz/stable/ubuntu/ub13.10/x86_64/graphviz_2.38.0-1~saucy_amd64.deb"
wget "http://www.graphviz.org/pub/graphviz/stable/ubuntu/ub13.10/x86_64/libgraphviz-dev_2.38.0-1~saucy_amd64.deb"
wget "http://www.graphviz.org/pub/graphviz/stable/ubuntu/ub13.10/x86_64/graphviz-dev_2.38.0-1~saucy_all.deb"
wget "http://www.graphviz.org/pub/graphviz/stable/ubuntu/ub13.10/x86_64/libgraphviz4_2.38.0-1~saucy_amd64.deb"

# Install PyGraphViz
pip3 install pygraphviz
