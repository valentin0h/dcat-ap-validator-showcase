# dcat-ap-validator-showcase
A simple skeleton for a DCAT-AP validator in Python (2.7). 

# What it does
The validator obtains an RDF graph from a remote source and runs few validation checks to determine
if the graph is valid with respect to the DCAT-AP v1.1 .

**Note**: At the current state the validator only checks for the occurrence of two mandatory classes and 
their respective mandatory properties as specified in DCAT-AP v.1.1. For each absence of such a class or property
an message is printed.

# How to run
To run the validator you simply run the validator with a parameter denoting the graph URI to be validated. 

    python validator.py https://data.gov.ie/catalog.ttl

# Future steps
This will eventually be a CKAN plugin.