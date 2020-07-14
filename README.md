# Online tool for Live Plotting of FACT Data

_Description:_ The package reads the _raw FACT data files_ (see below) coming in from the FACT data acusition system, and is processed from a local dir _/Data/_.
The package contains classes for setting up the detector environment, and for running analysis over singular or multiple datasets.
The package puts out several visualization modules for information stored in the FACT data, as describet further below. 

_Intention:_ The intention of this package is to provide easy acsess to the FACT data, as it is streamed directly from the detector into the _Data_ directory. 
This will make it easier to check that everything runs as it should, and to perform easy analysis on top of the data.

_Future Development:_ Future development consists of building a solid graphical user face and a simple installation mechanism for the package. A mechanism to easily add new analysis modules and adjust the detector parameters through settings.txt must come into place. 


### Installation

The package will in the future be installable and runnable through a GUI, as per early development stages the code is run through the main.py file.
Exec system to be built

### Usage
Current usage:

Run 1:

    python3 main.py

Run 2 in virtual shell (Not yet avilable from github - TODO: Setup a system for installing the virtual environment + packages):

    source venv/bin/activate
    python3 src/main.py
    
   

### Support 
Primary developer: Oline Ranum - olinear@uio.no

# Build of Program

## Main Folder Structure
    
    src:        
        The source code of the program. 
        
    settings: 
        settings.txt : This file contains all physical parameters of the detector. 
                       Note that the parameters are currently described in the src_SetUp/LoadData.py class
                       TODO: Write the stand alone description of the detector parameters.
        
    Data_Example:
        Contains one example file that can be run from /Data/
        
    venv: 
        Not currently avilable - Solution not yet placed for quickinstall virtualenv.
        Must be in place to ensure compatability with local versions and packages. 


# Flow

    Run through main.py.

*Main.py*: Performs three tasks. 1) Loads param = Sets detector parameters. 2) Makes a call to the RunAnalysis modules, and sets wheter to perform a single file or a multi file analysis. 3) Makes final call to plotting and visulaization.

*RunAnalysis*: Has two modules called RunSingleFileAnalysis and RunMultiFileAnalysis. RunSingleFileAnalysis builds a standard setup through the SetUp class and then to AnalysisToolBox [ATB]. When the ATB module Initiate_Standard_Analysis() is called a _standard_ analysis is performed, and a pandas DataFrame containing the vertex positions and weights are provided.

## Vertex Analysis 
The standard analysis packages entails a vertex reconstruction along the z-axis, returning the position of a vertex and the weight of the vertex. 
The weight of a vertex is defined as 1/(The number of potential particle origins). The combinatorics might yield several solutions for potential vertecies. 



# Main Information Holders
The Analysis is run with two primary information holders, as the system has two main sources of information. One being the raw data put out by FACT, the other being the external input of physical detector parameters. 

    param:
    
    MainFile:


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


# Future TODOs':
 -> Build the connection between the detector and the _/Data/_ folder. 
