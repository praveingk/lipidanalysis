# README #


Requirements :

1) Install Python 2.7 (also python-pip)

2) Install pip libraries : 

a) pipinstall numpy
b) pipinstall scipy
c) pipinstall plotly

Running the analyzer :

1) cd lipidanalyis/WT_MF_MA_analysis/src

2) python maAnalyze.py <inputfiles> <output directory> <command>

Choice of command : 

1) normal :

   Only normalization done for the input samples.

2) start :
   Normalization + Relative Abundance + Weight based Normalization + Quality Checks