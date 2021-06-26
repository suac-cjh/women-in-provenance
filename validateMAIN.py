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




if __name__ == '__main__':
	main()