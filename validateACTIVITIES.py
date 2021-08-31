'''
Name: validateActivities.py
Contact: Pauline Arnoud (parnoud@stanford.edu)

This file validates the data from the activities table by checking the SIDs,
IDs, dates, locations, nature of relationships, and sources. 
The functions called to validate the data can be found in the dataValidation.py file.

Please make sure to read the output message to check which mistakes you need to correct
yourself! While some mistakes are corrected automatically by the code, the code doesn't 
know how to deal with other issues.

See the following document for a breakdown of what exactly the program checks for:
https://docs.google.com/document/d/1a-uTqLAWqCMjqtUBQ5n-6QHgq8zuAgmIPpvZIGqLsXg/edit?usp=sharing 
'''

# import libraries
from dataValidation import *
import csv
import sys

def main():
	args = sys.argv[1:]
	inputFile = args[0]
	output = args[1]
	main = args[2]

	with open(inputFile, "r") as file, open(main, "r") as main_d, open(output, "w") as outFile:
		reader = csv.reader(file, delimiter = ',')
		writer = csv.writer(outFile, delimiter = ',')
		main = csv.DictReader(main_d, delimiter = ",")
		
		#Write header unchanged
		header = next(reader)
		writer.writerow(header)

		# Make the list of SIDs in the MAIN table
		sids = []
		for row in main:
			sids.append(row["S_ID"])

		# transpose the data (columns become rows and rows become columns)
		data = zip(*reader)
		# create a dictionary by combining the headers with the data
		d = dict(zip(header, data))

		# validate the IDs
		if checkIDs(d["ID"]):
		 	print("The IDs are valid!")

		# validate SIDs
		if checkSIDs(d["S_ID"]) and inMain(d["S_ID"], sids):
		 	print("The S_IDs are valid!")

		# validate Nature of Relationships
		d["Type of Activity"] = checkTypeOfActivity(d["Type of Activity"])

		# validate dates
		if checkDates(d["Start Date"]):
			print("All of the start dates are valid!")

		if checkDates(d["End Date"]):
			print("All of the end dates are valid!")

		#validate locations
		d["Location"] = checkLocations(d["Location"])

		# validate sources
		d["Sources"] = checkSources(d["Sources"])

		# transpose the data back
		num_of_entries = len(d["S_ID"])
		rows = [ [] for i in range(num_of_entries)]
		for col in d.values():
			for i in range(len(col)):
				rows[i].append(col[i])
		
		# write the new rows to the output file
		for row in rows:
			writer.writerow(row)

if __name__ == '__main__':
	main()