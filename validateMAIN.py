'''
Name: validateMain.py
Contact: Pauline Arnoud (parnoud@stanford.edu)

This file validates the data from the MAIN table by checking the SIDs,
IDs, dates, locations, nature of relationships, and sources. 
The functions called to validate the data can be found in the dataValidation.py file.

Please make sure to read the output message to check which mistakes you need to correct
yourself! While some mistakes are corrected automatically by the code, the code doesn't 
know how to deal with other issues.

See the following document for a breakdown of what exactly the program checks for:
https://docs.google.com/document/d/1a-uTqLAWqCMjqtUBQ5n-6QHgq8zuAgmIPpvZIGqLsXg/edit?usp=sharing 
'''

#import libraries
from dataValidation import *
import csv
import sys

def main():
	args = sys.argv[1:]
	inputFile = args[0]
	output = args[1]

	with open(inputFile, "r") as file, open(output, "w") as outFile:
		reader = csv.reader(file, delimiter = ',')
		writer = csv.writer(outFile, delimiter = ',')
		
		#Write header unchanged
		header = next(reader)
		writer.writerow(header)

		# transpose the data (columns become rows and rows become columns)
		data = zip(*reader)
		# create a dictionary by combining the headers with the data
		d = dict(zip(header, data))

		# validate S_IDs
		if checkIDs(d["S_ID"]):
		 	print("The S_IDs are valid!")

		# validate the names
		d["First"] = checkNames(d["First"])
		d["Married Surname 1"] = checkNames(d["Married Surname 1"])
		d["Married Surname 2"] = checkNames(d["Married Surname 2"])
		d["Married Surname 3"] = checkNames(d["Married Surname 3"])
		d["Middle"] = checkNames(d["Middle"])
		d["Surname"] = checkNames(d["Surname"])
		d["Nickname"] = checkNames(d["Nickname"])

		# valide inferred sex
		if checkSex(d["Inferred Sex"]):
			print("All the inferred sexes are valid!")

		# validate dates
		if checkDates(d["Date of Birth"]):
			print("All the dates of birth are valid!")

		if checkDates(d["Date of Death"]):
			print("All the dates of death are valid!")

		# validate sources
		checkSources(d["Sources"])

		# validate biographical notes
		checkURL(d["Biographical Note"])

		#validate professions -- TO DO: not working right now..
		#d["Profession"] = checkProfessions(d["Profession"])

		#validate locations
		checkLocations(d["Place of Birth"])
		checkLocations(d["Place of Death"])

		# transpose the data back
		num_of_women = len(d["S_ID"])
		rows = [ [] for i in range(num_of_women)]
		for col in d.values():
			for i in range(len(col)):
				rows[i].append(col[i])
		
		# write the new rows to the output file
		for row in rows:
			writer.writerow(row)


if __name__ == '__main__':
	main()