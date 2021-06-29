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
		d["Nature of Relationship"] = checkNatureOfRel(d["Nature of Relationship"])

		# validate the names
		d["Married Surname"] = checkNames(d["Married Surname"])
		d["Suffix"] = checkNames(d["Suffix"])
		d["Middle"] = checkNames(d["Middle"])
		d["Surname"] = checkNames(d["Surname"])
		d["Nickname"] = checkNames(d["Nickname"])

		# validate inferred sex
		if checkSex(d["Inferred Sex"]):
			print("All the inferred sexes are valid!")

		# validate dates
		if checkDates(d["Date of Birth"]):
			print("All the dates of birth are valid!")

		if checkDates(d["Date of Death"]):
			print("All the dates of death are valid!")

		if checkDates(d["Date of Marriage"]):
			print("All the dates of marriage are valid!")

		#validate locations
		checkLocations(d["Place of Birth"])
		checkLocations(d["Place of Death"])
		checkLocations(d["Place of Marriage"])

		# validate sources
		checkSources(d["Sources"])

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