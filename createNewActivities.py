'''
Name: createActivities.py
Contact: Pauline Arnoud (parnoud@stanford.edu)

This file creates a csv file to be imported into Omeka for new activities
for the deaths and births of the women in the MAIN table.
'''

# import libraries
import csv
from geopy.geocoders import Nominatim

# constants
DEFAULT_HEADER = ['Dublin Core:Title', 'Dublin Core:Description', 'Dublin Core:Creator', 'Dublin Core:Language', 'Tags', 'Collection', 'Dublin Core:Source', 'Dublin Core:Type']
EVENT_METADATA = ["Item Type Metadata:Duration", "Item Type Metadata:Event Type"]
GEOLOCATION_HEADER = ["geolocation:latitude", "geolocation:longitude", "geolocation:zoom_level"]
ACTIVITY_HEADER = DEFAULT_HEADER + EVENT_METADATA + GEOLOCATION_HEADER
ZOOM_LEVEL = 5


'''
NAME : getInputs
--------------------------
This function prompts the user for the information it needs to run the program. In particular, it
asks for the main file, output file, and creator. 
'''
def getInputs():
	inputs = {}
	inputs["main"] = input("What file contains the main table? ")
	inputs["outputFile"] = input("To what file do you want to write the converted csv file? ")
	inputs["creator"] = input("Who is creating this file? ")
	return inputs

'''
NAME : createSIDdict
--------------------------
This function creates a dictionary of the women's names associated with their S_IDs so that the program
can know which woman an activity, relationship, publication or source belongs to based on the S_ID.
'''
def createSIDdict(main):
	s_ids = {}
	for row in main:
		title = ((row["First"] + ' ' + row["Middle"] + ' ' + row["Surname"] + ' ' + row["Married Surname 1"] + ' ' + row["Married Surname 2"] + ' ' + row["Married Surname 3"]).replace("  ", " ").strip())
		s_ids[row["S_ID"]] = title
	return s_ids

'''
NAME : findLongLat
--------------------------
This function returns the corresponding longitude/latitude information for an inputted location using the
Nominatim library. 
'''
def findLatLong(location):
	address = location.split(";")
	address = address[-1]
	geolocator = Nominatim(user_agent="my_user_agent")
	loc = geolocator.geocode(address)
	if loc == None:
		print("didn't work for:", address)
		return {"Latitude":'', "Longitude":''}
	return {"Latitude":loc.latitude, "Longitude":loc.longitude}

'''
NAME : createBirth
--------------------------
This function creates an activity for a woman's birth for a given row from the MAIN table,
which corresponds to a woman.
'''
def createBirth(row, creator, s_ids):
	rowVals = []
	rowVals.append(s_ids[row["S_ID"]] + "'s Birth")
	rowVals.append("")
	rowVals.append(creator)
	rowVals.append("English")
	rowVals.append(row["S_ID"])
	rowVals.append("Activities")
	rowVals.append('+'.join(row["Sources"].split('/')))
	rowVals.append('Event')
	rowVals.append(row["Date of Birth"])
	rowVals.append("Birth")

	coordinates = findLatLong(row["Place of Birth"])
	rowVals.append(coordinates["Latitude"])
	rowVals.append(coordinates["Longitude"])
	rowVals.append(ZOOM_LEVEL)
	return rowVals

'''
NAME : createDeath
--------------------------
This function creates an activity for a woman's death for a given row from the MAIN table,
which corresponds to a woman.
'''
def createDeath(row, creator, s_ids):
	rowVals = []
	rowVals.append(s_ids[row["S_ID"]] + "'s Death")
	rowVals.append("")
	rowVals.append(creator)
	rowVals.append("English")
	rowVals.append(row["S_ID"])
	rowVals.append("Activities")
	rowVals.append('+'.join(row["Sources"].split('/')))
	rowVals.append('Event')
	rowVals.append(row["Date of Death"])
	rowVals.append("Death")

	coordinates = findLatLong(row["Place of Death"])
	rowVals.append(coordinates["Latitude"])
	rowVals.append(coordinates["Longitude"])
	rowVals.append(ZOOM_LEVEL)
	return rowVals

'''
NAME : main
--------------------------
This function prompts the user for the needed information and creates an output csv file ready for Omeka
import with activities for the births and deaths of the women in the MAIN table.
'''
def main():
	inputs = getInputs()
	with open(inputs["main"], "r") as file, open(inputs["main"], "r") as main_d, open(inputs["outputFile"], "w") as outFile:
		reader = csv.DictReader(file, delimiter = ',')
		main = csv.DictReader(main_d, delimiter = ",")
		writer = csv.writer(outFile, delimiter = ',')
		s_ids = createSIDdict(main)

		creator = inputs["creator"]

		newActivities = []
		newActivities.append(ACTIVITY_HEADER)
		for row in reader:
			newActivities.append(createBirth(row, creator, s_ids))
			newActivities.append(createDeath(row, creator, s_ids))

		for row in newActivities:
			writer.writerow(row)
			print(row)

if __name__ == '__main__':
    main()