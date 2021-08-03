import csv
from geopy.geocoders import Nominatim

DEFAULT_HEADER = ['Dublin Core:Title', 'Dublin Core:Description', 'Dublin Core:Creator', 'Dublin Core:Language', 'Tags', 'Collection', 'Dublin Core:Source', 'Dublin Core:Type']
EVENT_METADATA = ["Item Type Metadata:Duration", "Item Type Metadata:Event Type"]
GEOLOCATION_HEADER = ["geolocation:latitude", "geolocation:longitude", "geolocation:zoom_level"]
ACTIVITY_HEADER = DEFAULT_HEADER + EVENT_METADATA + GEOLOCATION_HEADER
ZOOM_LEVEL = 5

# create activities for deaths and births

def getInputs():
	inputs = {}
	inputs["main"] = input("What file contains the main table? ")
	inputs["outputFile"] = input("To what file do you want to write the converted csv file? ")
	inputs["creator"] = input("Who is creating this file? ")
	return inputs

def createSIDdict(main):
	s_ids = {}
	for row in main:
		title = ((row["First"] + ' ' + row["Middle"] + ' ' + row["Surname"] + ' ' + row["Married Surname 1"] + ' ' + row["Married Surname 2"] + ' ' + row["Married Surname 3"]).replace("  ", " ").strip())
		s_ids[row["S_ID"]] = title
	return s_ids

def findLatLong(location):
	address = location.split(";")
	address = address[-1]
	geolocator = Nominatim(user_agent="my_user_agent")
	loc = geolocator.geocode(address)
	if loc == None:
		print("didn't work for:", address)
		return {"Latitude":'', "Longitude":''}
	return {"Latitude":loc.latitude, "Longitude":loc.longitude}

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