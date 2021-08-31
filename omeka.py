'''
Name: omeka.py
Contact: Pauline Arnoud (parnoud@stanford.edu)
This script converts a csv file from the WiP data table to a corretly
formatted csv file for Omeka import.
All the functions called can be found in the convertOmeka.py file

There is no data validation/check! This program assumes correct input file.
'''

# importing libraries
from convertOmeka import *
import csv

def main():
    inputs = getInputs()
    with open(inputs["inputFile"], "r") as file, open(inputs["main"], "r") as main_d, open(inputs["outputFile"], "w") as outFile:
        reader = csv.DictReader(file, delimiter = ',')
        main = csv.DictReader(main_d, delimiter = ",")
        writer = csv.writer(outFile, delimiter = ',')
    
        #setting up the dictionary with the S_ID and their associated women
        s_ids = createSIDdict(main)
        creator = inputs["creator"]

        #calling the appropriate function based on the table type.
        tableType = inputs["tableType"]
        if tableType == "main":
            rowVals = convertMain(reader, s_ids, creator)
        elif tableType == "relationships":
            rowVals = convertRelationships(reader, s_ids, creator)
        elif tableType == "activities":
            rowVals = convertActivities(reader, creator)
        elif tableType == "publications":
            rowVals = convertPublications(reader, creator)
        elif tableType == "objects":
            print("We unfortunately can't convert", tableType, "yet...")
        elif tableType == "collections":
            print("We unfortunately can't convert", tableType, "yet...")
        elif tableType == "sources":
            rowVals = convertSources(reader, s_ids, creator)
        else:
            rowVals = []

        # writing the returned rows to the output file
        for row in rowVals:
            writer.writerow(row)
            print(row)

if __name__ == '__main__':
    main()