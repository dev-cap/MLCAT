# Mailing List Community Analysis Tool (MLCAT)

[![Build Status](https://travis-ci.org/DeveloperCAP/MLCAT.svg?branch=development)](https://travis-ci.org/DeveloperCAP/MLCAT)
[![Maintainability](https://api.codeclimate.com/v1/badges/f1d7947c8a62338544dd/maintainability)](https://codeclimate.com/github/DeveloperCAP/MLCAT/maintainability)
[![codecov](https://codecov.io/gh/DeveloperCAP/MLCAT/branch/master/graph/badge.svg)](https://codecov.io/gh/DeveloperCAP/MLCAT)
[![Dependency Status](https://www.versioneye.com/user/projects/5a57a7d70fb24f382f102324/badge.svg?style=flat-square)](https://www.versioneye.com/user/projects/5a57a7d70fb24f382f102324)


> Parsing mailing lists to detect communication patterns.

Welcome to the Mailing List Community Analysis Tool! The main objective of this project is to develop a mailing list parser to extract information from a mailing list such as senders,receivers, time stamps etc and then use this to construct an organizational (or communication) structure like conversation thread hypergraphs for further analysis. We utilize social network analysis techniques to examine the relationships between authors on common mailing lists like LKML, Sakai etc. Study of these interactions on different levels helps us in deriving the local and global communication patterns between users on different threads. This project draws its inspiration from various fields such as data mining, graph theory, information retrieval and inferential modelling in order to form predictive models that help in understanding certain intricate characteristics of a social network. This involves analyzing graphs with, say, authors as nodes and their correspondences as edges, to study the details about various network graph properties such as density, size, node centrality, degree, connectedness etc.

![Vertex Clustering](https://raw.githubusercontent.com/DeveloperCAP/MLCAT/master/data/lkml/graphs/vertex_clustering_infomap.png)

## Usage

The library's working has been modularised into many modules namely input, analysis and util. The [driver file](main_driver.py) presents a brief overview of how one can use the Mailing List Community Analysis Tool for parsing and analysis.

Some of the visualisable sample outputs can be seen [here](https://github.com/DeveloperCAP/MLCAT/tree/development/data), categorized into various datasets, giving an idea about this project's capabilites and as to what kind of insights we can and we plan to derive from the datasets.

## Documentation

Mailing List Community Analysis Tool uses [Sphinx Python Documentation Generator](http://www.sphinx-doc.org/en/stable/) for generating documentation of the library. The documentation is setup to work with [Google Style Docstrings](http://www.sphinx-doc.org/en/stable/ext/example_google.html) which eases the documentation writing process.

The documentation can be found under 'docs/' whose updation has been made automatic by the a bash script which otherwise requires to run `make html` in the 'docs/' directory after every commit.

You can view the documentation hosted on `gh-pages` [here](http://developercap.github.io/MLCAT/).

## Testing Framework

Presently, Mailing List Community Analysis Tool has various end-to-end tests implemented which reside in the [test directory](https://github.com/DeveloperCAP/MLCAT/tree/development/test/). We use py.test as the unit test framework and you can get a comprehensive idea of the various use cases of each of the modules from the corresponding tests.

![Conversation Characteristics](https://raw.githubusercontent.com/achyudhk/Mailing-List-Network-Analyzer/development/data/sakai-devel/plots/conversation_chars.png)

## Installation

Mailing List Community Analysis Tool depends on various third-party libraries which are listed in [requirements.txt](https://github.com/DeveloperCAP/MLCAT/blob/development/requirements.txt).
The libraries in `requirements.txt` along with other dependencies are installed using [install_package_dependencies.sh](https://github.com/DeveloperCAP/MLCAT/blob/development/etc/install_package_dependencies.sh) 
Run `cd etc && bash install_package_dependencies.sh` in the project root directory to install these dependencies.

## License

Mailing List Community Analysis Tool is available under the [GPL 3.0 License](https://github.com/DeveloperCAP/MLCAT/blob/master/LICENSE.md)
