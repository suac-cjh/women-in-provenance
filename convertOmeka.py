'''
Name: convertOmeka.py
Contact: Pauline Arnoud (parnoud@stanford.edu)

This file contains the functions used by omeka.py to convert a csv file 
from the WiP data table to a corretly formatted csv file for Omeka import.
'''

# importing libraries
import csv
import sys
import datetime
from geopy.geocoders import Nominatim

# constants
TABLETYPES = ["main", "relationships", "activities", "publications", "objects", "collections", "sources"]
DEFAULT_HEADER = ['Dublin Core:Title', 'Dublin Core:Description', 'Dublin Core:Creator', 'Dublin Core:Language', 'Tags', 'Collection', 'Dublin Core:Source', 'Dublin Core:Type']
PERSON_METADATA = ["Item Type Metadata:Birth Date", "Item Type Metadata:Birthplace", "Item Type Metadata:Death Date", "Item Type Metadata:Occupation"]
EVENT_METADATA = ["Item Type Metadata:Duration", "Item Type Metadata:Event Type"]
HYPERLINK_METADATA = ["Item Type Metadata:URL", "Item Type Metadata:Publication Date", "Item Type Metadata:Citation"]
TEXT_METADATA = ["Item Type Metadata:Original Format"]
GEOLOCATION_HEADER = ["geolocation:latitude", "geolocation:longitude", "geolocation:zoom_level"]
ZOOM_LEVEL = 5

'''
NAME : getInputs
--------------------------
This function prompts the user for the information it needs to run the program. In particular, it
asks for the input file, output file, table type, and creator. 
'''
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
NAME : convertMAIN
--------------------------
This function converts the MAIN table from the WiP data table to an Omeka ready csv file
for each woman in main, the function builds the equivalent row in Omeka. The function then
returns a list of such rows to be written into the output file.
'''
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

'''
NAME : convertRelationships
--------------------------
This function converts the relationships table from the WiP data table to an Omeka ready csv file
for each relationship, the function builds the equivalent row in Omeka. The function then
returns a list of such rows to be written into the output file.
'''
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


'''
NAME : getActivityTitle
--------------------------
This function creates a title for the activity to be used in the Title field in Omeka. Based on which
kind the activity is, the title is composed of different information from the data table.
'''
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
		if location != "":
			print("Location conversion didn't work for:", location)
		return {"Latitude":'', "Longitude":''}
	return {"Latitude":loc.latitude, "Longitude":loc.longitude}


'''
NAME : convertActivities
--------------------------
This function converts the activities table from the WiP data table to an Omeka ready csv file
for each activity, the function builds the equivalent row in Omeka. The function then
returns a list of such rows to be written into the output file.
'''
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

'''
NAME : getSourceTitle
--------------------------
This function creates a title for the source to be used in the Title field in Omeka. Based on whether or
not the source has a Title on the original data table, the Omeka title is either the type of source or the
title.
'''
def getSourceTitle(row):
	if row["Title"] != '':
		title = row["Title"]
	else:
		title = row["Type of Source"]
	return title
	
'''
NAME : getSourceDescription
--------------------------
This function creates a description for the sourceto be used in the Description field in Omeka. Based on which
fields of the source has information, the description is composed of the type of source, author, and publication
if they exist.
'''
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

'''
NAME : convertSources
--------------------------
This function converts the sources table from the WiP data table to an Omeka ready csv file
for each source, the function builds the equivalent row in Omeka. The function then
returns a list of such rows to be written into the output file.
'''
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

'''
NAME : getPublicationDescription
--------------------------
This function creates a description for the publication to be used in the Description field in Omeka. Based on which
fields of the publication has information, the description is composed of the genre, type of publication, title, 
publication, publication house and publication location if they exist.
'''
def getPublicationDescription(row):
	description = ""
	if row["Genre"] != '':
		description += row["Genre"]
	description += " " + row["Type of Publication"]
	if row["Title"] != '':
		if description != '':
			description += " named " + row["Title"]
		else:
			description += row["Title"]
	if row["Publication"] != '':
		description += " published in " + row["Publication"]
	if row["Publication House"] != '':
		description += " by " + row["Publication House"]
	if row["Publication Location"] != '':
		description += " in " + row["Publication Location"]
	return description

'''
NAME : getPublicationTitle
--------------------------
This function creates a title for the publication to be used in the Title field in Omeka. Based on whether or
not the source has a Title on the original data table, the Omeka title is either the title, publication or
type of publication.
'''
def getPublicationTitle(row):
	if row["Title"] != '':
		return row["Title"]
	elif row["Publication"] != '':
		return row['Publication']
	else:
		return row["Type of Publication"]

'''
NAME : convertPublications
--------------------------
This function converts the publications table from the WiP data table to an Omeka ready csv file
for each publication, the function builds the equivalent row in Omeka. The function then
returns a list of such rows to be written into the output file.
'''
def convertPublications(reader, creator):
	publicationsHeader = DEFAULT_HEADER + TEXT_METADATA + GEOLOCATION_HEADER
	newRows = []
	newRows.append(publicationsHeader)
	for row in reader:
		rowVals = []
		rowVals.append(getPublicationTitle(row))
		rowVals.append(getPublicationDescription(row))
		rowVals.append(creator)
		rowVals.append("English")
		rowVals.append(row["S_ID"])
		rowVals.append("Publications")
		rowVals.append('+'.join(row["Sources"].split('/')))
		rowVals.append("Text")
		rowVals.append(row["Type of Publication"])

		coordinates = findLatLong(row["Publication Location"])
		rowVals.append(coordinates["Latitude"])
		rowVals.append(coordinates["Longitude"])
		rowVals.append(ZOOM_LEVEL)

		newRows.append(rowVals)
	return newRows