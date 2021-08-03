import csv
import sys
import datetime
from geopy.geocoders import Nominatim

TABLETYPES = ["main", "relationships", "activities", "publications", "objects", "collections", "sources"]
DEFAULT_HEADER = ['Dublin Core:Title', 'Dublin Core:Description', 'Dublin Core:Creator', 'Dublin Core:Language', 'Tags', 'Collection', 'Dublin Core:Source', 'Dublin Core:Type']
PERSON_METADATA = ["Item Type Metadata:Birth Date", "Item Type Metadata:Birthplace", "Item Type Metadata:Death Date", "Item Type Metadata:Occupation"]
EVENT_METADATA = ["Item Type Metadata:Duration", "Item Type Metadata:Event Type"]
HYPERLINK_METADATA = ["Item Type Metadata:URL", "Item Type Metadata:Publication Date", "Item Type Metadata:Citation"]
GEOLOCATION_HEADER = ["geolocation:latitude", "geolocation:longitude", "geolocation:zoom_level"]

ZOOM_LEVEL = 5

# global variables so that all functions can access this information

def getInputs():
	inputs = {}
	inputs["inputFile"] = input("What file do you want to convert? ")
	inputs["outputFile"] = input("To what file do you want to write the converted csv file? ")
	inputs["main"] = input("File with the SUN_ID and the women associated with them: ")
	tableType = input("What table type is this? (Options:" + ' '.join(TABLETYPES) + "): ")
	while (str(tableType) not in TABLETYPES):
		tableType = input("Wrong input. Here are the options:" + ' '.join(TABLETYPES) + ": ")
	inputs["tableType"] = tableType
	inputs["creator"] = input("Who is creating this file? ")
	return inputs

def createSIDdict(main):
	s_ids = {}
	for row in main:
		title = ((row["First"] + ' ' + row["Middle"] + ' ' + row["Surname"] + ' ' + row["Married Surname 1"] + ' ' + row["Married Surname 2"] + ' ' + row["Married Surname 3"]).replace("  ", " ").strip())
		s_ids[row["S_ID"]] = title
	return s_ids

def convertMain(reader, s_ids, creator):
	mainHeader = DEFAULT_HEADER + PERSON_METADATA
	newRows = []
	newRows.append(mainHeader)
	for row in reader:
		rowVals = []
		rowVals.append(s_ids[row["S_ID"]])
		rowVals.append(row["Biographical Note"])
		rowVals.append(creator)
		rowVals.append("English")
		rowVals.append(row["S_ID"])
		rowVals.append('Main')
		rowVals.append('+'.join(row["Sources"].split('/')))
		rowVals.append('Person')
		rowVals.append(row["Date of Birth"])
		rowVals.append(row["Place of Birth"])
		rowVals.append(row["Date of Death"])
		rowVals.append(row["Profession"].replace("/", "+"))
		newRows.append(rowVals)
	return newRows

def convertRelationships(reader, s_ids, creator):
	relationshipsHeader = DEFAULT_HEADER + PERSON_METADATA
	newRows = []
	newRows.append(relationshipsHeader)
	for row in reader:
		rowVals = []
		rowVals.append(((row["First"] + ' ' + row["Middle"] + ' ' + row["Last"]).replace("  ", " ").strip()))
		rowVals.append(s_ids[row["S_ID"]] + "'s " + row["Nature of Relationship"])
		rowVals.append(creator)
		rowVals.append("English")
		rowVals.append(row["S_ID"])
		rowVals.append('+'.join(row["Sources"].split('/')))
		rowVals.append('Person')
		rowVals.append(row["Date of Birth"])
		rowVals.append(row["Place of Birth"])
		rowVals.append(row["Date of Death"])
		rowVals.append(row["Profession"].replace("/", "+"))
		newRows.append(rowVals)
	return newRows

def getActivityTitle(row):
	if row["Type of Activity"] == "Trip":
		location = row["Location"].split(";")[-1]
		title = ((row["Type of Activity"] + " as a " + row["Position"] + " to " + location).replace("  ", " ").strip())
	elif row["Type of Activity"] == "Job":
		title = ((row["Type of Activity"] + " as " + row["Position"] + " at the " + row["Activity/Organization Name"]).replace("  ", " ").strip())
	elif row["Type of Activity"] == "Project":
		title = ((row["Position"] + " for the " + row["Activity/Organization Name"] + ' ' + row["Type of Activity"]).replace("  ", " ").strip())
	elif row["Type of Activity"] == "Education":
		title = ((row["Position"] + " at " + row["Activity/Organization Name"] + ' ' + row["Type of Activity"]).replace("  ", " ").strip())
	else:
		title = ((row["Position"] + " of the " + row["Activity/Organization Name"]).replace("  ", " ").strip())
	return title

def findLatLong(location):
	address = location.split(";")
	address = address[-1]
	geolocator = Nominatim(user_agent="my_user_agent")
	loc = geolocator.geocode(address)
	if loc == None:
		print("didn't work for:", address)
		return {"Latitude":'', "Longitude":''}
	return {"Latitude":loc.latitude, "Longitude":loc.longitude}

def convertActivities(reader, creator):
	activitiesHeader = DEFAULT_HEADER + EVENT_METADATA + GEOLOCATION_HEADER
	newRows = []
	newRows.append(activitiesHeader)
	for row in reader:
		rowVals = []
		rowVals.append(getActivityTitle(row))
		rowVals.append("")
		rowVals.append(creator)
		rowVals.append("English")
		rowVals.append(row["S_ID"])
		rowVals.append("Activities")
		rowVals.append('+'.join(row["Sources"].split('/')))
		rowVals.append('Event')
		duration = row["Start Date"] + "-" + row["End Date"]
		if (duration == "-"):
			duration = ""
		rowVals.append(duration)
		eventType = row["Position"] + " of " + row["Activity/Organization Name"] + " (in " + row["Location"] + ")."
		rowVals.append(eventType)

		coordinates = findLatLong(row["Location"])
		rowVals.append(coordinates["Latitude"])
		rowVals.append(coordinates["Longitude"])
		rowVals.append(ZOOM_LEVEL)

		newRows.append(rowVals)
	return newRows

def getSourceTitle(row):
	if row["Title"] != '':
		title = row["Title"]
	else:
		title = row["Type of Source"]
	return title
	
def getSourceDescription(row):
	if row["Type of Source"] != '' and row["Author"] != '' and row["Publication"] != '':
		description = row["Type of Source"] + " by " + row["Author"] + " (" + row["Publication"] + ")"
	elif row["Type of Source"] == '':
		if row["Author"] != '' and row["Publication"] != '':
			description = "by " + row["Author"] + " (" + row["Publication"] + ")"
		elif row["Author"] == '':
			description = "by " + row["Publication"]
		else:
			description = "by " + row["Author"]
	elif row["Author"] == '' and row["Publication"] != '':
		description = row["Type of Source"] + " by " + row["Publication"]
	else:
		description = row["Type of Source"]
	return description

def convertSources(reader, s_ids, creator):
	sourcesHeader = DEFAULT_HEADER + HYPERLINK_METADATA
	newRows = []
	newRows.append(sourcesHeader)
	for row in reader:
		rowVals = []
		rowVals.append(getSourceTitle(row))
		rowVals.append(getSourceDescription(row))
		rowVals.append(creator)
		rowVals.append("English")
		rowVals.append(row["S_ID"] + "," + row["ID"])
		rowVals.append('')
		rowVals.append('Hyperlink')
		URL = row["Link"]
		rowVals.append(URL)
		rowVals.append(row["Publication Date"])
		rowVals.append(row["Citations"])
		newRows.append(rowVals)
	return newRows

