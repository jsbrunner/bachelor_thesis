# README

Investigating the Behavior of Advanced Automated Systems in Vehicle-Platoons through Empirical Observations

Johannes S. Brunner

June 2021
__________________________________

The code used to investigate on empirical data is split into several python-files:

All six files reading data from the experimental campaigns (first six) need the filename and the desired start and end time within the individual file. They return the preprocessed data in a standardized strucure as a Pandas dataframe.

- Laval.py:             
reads data sets from the human car-following campaign conducted by Laval et al. in 2014

- Napoli.py:            
reads data sets from the human car-following campaign conducted by Punzo and Simonelli in 2005

- OpenACC.py:           
reads data sets from the AstaZero platooning-campaign conducted in 2019

- ZalaZone.py:          
reads data sets from the ZalaZone platooning-campaign conducted in 2019

- CARMA1.py:            
reads individual runs from the CARMA1 proof-of-concept CACC platooning-campaign conducted in 2016

- CARMA2.py:            
reads individual runs from the CARMA2 CACC platooning-campaign conducted in 2018

- create_dataset.py:    
creates an aggregated data set with data slices from the original experimental campaigns -> all files assessing the properties read from the aggregated data set; directly calls methods that read the data and saves the aggregated data set as csv-file into the main project folder

- main.py:              
computes the number of slices and the platoon driving distance included in the aggregated data set which is suitable for the assessment of each of the four properties; reads the aggregated data set and prints the corresponding numbers 

- methods.py:          
includes the three response time methods from Makridis et al. (2020b), Lanaud et al. (2021), and Li et al. (2021), includes plotting; each method needs the data frame, the names of a preceding and a following vehicle and depending on the response time method additional parameters; the methods return a list with the estimated response time and either the cross-correlation coefficient or the the detected speed change instants

- response_time.py:     
organizes the input and output for the response time methods, includes plotting; reads perturbation events from the aggregated data set and saves the response time plots into the /plots/rt project folder

- headway.py:           
estimates the headway, includes plotting; reads suitable slices from the aggregated data set file and saves the headway plots into the /plots/hw project folder

- string_stability.py:  
evaluates the string stability, includes plotting; reads perturbation events from the aggregated data set file and saves the string stability plots into the /plots/ss project folder

- energy_cons.py:       
compares energy consumption, includes plotting; reads suitable slices from the aggregated data set file and saves the energy consumption plots into the /plots/ec project folder

- fund_diag.py:        
attempt to derive flow and density and create the fundamental diagram (no results for the work); Pandas dataframe as input, shows fundamental diagram

- plots.py:             
includes various plotting functions, was particularly used to examine the data; the included methods need a single or several Pandas dataframe(s) and directly show a plot


Data sets are directly loaded from the project's main folder.
Figures are saved into the subdirectories "plots" and either "ec", "hw", "rt", and "ss" depending on the property depicted.
