'''
Name: palladio.py
Contact: Pauline Arnoud (parnoud@stanford.edu)

This script converts a csv file from the WiP data table to a corretly
formatted csv file for Palladio.

1. Changes all dates from %m/%d/%Y format to %Y-%m-%d.
2. Changes locations to "Person's name + Location type: most precise location" 
						(ex: Hansen's Place of Birth: Palo-Alto hospital)

There is no data validation/check! This program assumes correct input file.
'''

import csv
import sys
import datetime


def isDate(col):
	format = ('%m/%d/%Y')
	try:
 		datetime.datetime.strptime(col, format)
		return True

	except ValueError:
		return False


def convertDate(col):
	d = datetime.datetime.strptime(col, '%m/%d/%Y')
	return d.strftime('%Y-%m-%d') 

def isLocation(col):
	# we assume that locations in input are correctly formatted to start with continent-- TO CHANGE
	continents = ["North America", "Europe", "Asia", "Africa", "South America", "Oceania", "Antarctica"]
	for continent in continents:
		if continent in col:
			return True
	return False

def convertLocation(row, header, colIdx):
	split = row[colIdx].split(";")
	newLocation = row[1] + "'s " + header[colIdx] + ": " + split[len(split) - 1]
	return newLocation

def main():
	args = sys.argv[1:]
	input = args[0]
	output = args[1]

	with open(input, "r") as file, open(output, "w") as outFile:
		reader = csv.reader(file, delimiter = ',')
		writer = csv.writer(outFile, delimiter = ',')

		#Write header unchanged
		header = next(reader)
		writer.writerow(header)

		for row in reader:
			colValues = []
			colIdx = 0
			for col in row:
				if isDate(col):
					newcol = convertDate(col)
					print(col, "was converted to", newcol)
					colValues.append(newcol)
				elif isLocation(col):
					newcol = convertLocation(row, header, colIdx)
					print(col, "was converted to", newcol)
					colValues.append(newcol)	
				else:
					colValues.append(col)
				colIdx += 1

			writer.writerow(colValues)


if __name__ == '__main__':
	main()
