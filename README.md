# README

Investigating the Behavior of Advanced Automated Systems in Vehicle-Platoons through Empirical Observations

Johannes S. Brunner

June 2021
__________________________________

The code used to investigate on empirical data is split into several python-files:


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
creates an aggregated data set with data slices from the original experimental campaigns -> all files assessing the properties read from the aggregated data set

- main.py:              
computes the number of slices and the platoon driving distance 

- methods.py:          
includes the three response time methods from Makridis et al. (2020b), Lanaud et al. (2021), and Li et al. (2021), includes plotting

- response_time.py:     
organizes the input and output for the response time methods, includes plotting

- headway.py:           
estimates the headway, includes plotting

- string_stability.py:  
evaluates the string stability, includes plotting

- energy_cons.py:       
compares energy consumption, includes plotting

- fund_diag.py:        
attempt to derive flow and density and create the fundamental diagram (no results for the work)

- plots.py:             
includes various plotting functions, was particularly used to examine the data


Data sets are directly loaded from the project's main folder.
Figures are saved into the subdirectories "plots" and either "ec", "hw", "rt", and "ss" depending on the property depicted
