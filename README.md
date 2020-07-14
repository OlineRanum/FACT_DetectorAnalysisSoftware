# Online tool for Live Plotting of FACT Data

_Description:_ The package reads the _raw data files_ (see below) coming from the FACT data acusition system. 

    


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

    settings: 




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
