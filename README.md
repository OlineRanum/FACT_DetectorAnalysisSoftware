# Online tool for Live Plotting of FACT Data

_Description:_ The package reads the _raw data files_ (see below) coming from the FACT data acusition system, read from a local dir _Data_.
The package contains classes for setting up the detector environment, and for running analysis on the data. 
The output is several visualization tools of the FACT data analysis, as described further below. 

_Intention:_ The intention of this package is to provide easy acsess to the information, as it comes in to the _Data_ directory from the acquisition systems. This will make it easier to check that everything runs as it should, and to perform easy analysis on top of the data.


# Installation
None - you just run it with main.py
Exec system to be built

# Usage
Run 1:

    python3 main.py

Run 2 in virtual shell (Not yet avilable from github - TODO: Setup a system for installing the virtual environment + packages):

    source venv/bin/activate
    python3 src/main.py
    
   

# Support 
Contact: olinear@uio.no

# Folder Structure
    
    src:        
        The source code of the program. 
        
    settings: 
        settings.txt : This file contains all physical parameters of the ditector.
                       Note that the parameters are currently described
        
    Data_Example:
        Contains one example file that can be run from /Data/
        
    venv: 
        Not currently avilable - Solution not yet placed for quickinstall virtualenv




# Main Data Holders

    param:
    
    src


# Native Information

## Raw Data Files
The FACT system produces raw datafiles on the format of

    | N   | t | tot |
    |-----|---|-----|
    | 412 | 0 | 5   |
    | 5   | 5 | 15  |
    | 200 | 5 | 10  |
    -----
    | 645 | 35| 10  |

These are the basic information which all analysis is based upon, as well as the detector settings. 


# Roadmap
Ideas for future development

# Authors and acknowledgment

## Contributors 
    | Name   | Contact |
    |-----|---|
    | Oline A. Ranum | olinear@uio.no | 
    
    
## How to start with getting to know the project 

# Project status
Early stages of development 
Working on building cornerstones of the system 
