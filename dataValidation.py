'''
Name: dataValidation.py
Contact: Pauline Arnoud (parnoud@stanford.edu)

This file contains the functions called by validateACTIVITIES.py, validateMAIN.py and 
validateRELATIONSHIPS.py to check the data for mistakes.

See the following document for a breakdown of what exactly the program checks for:
https://docs.google.com/document/d/1a-uTqLAWqCMjqtUBQ5n-6QHgq8zuAgmIPpvZIGqLsXg/edit?usp=sharing 
'''

import csv
import datetime
from detect_delimiter import detect  #to detect the source delimiter used
import string
from urllib.request import urlopen, URLError	#to check validity of URLs

CONTINENTS = ["North America", "South America", "Europe", "Asia", "Africa","Oceania", "Antarctica"]
ABBREV_TO_STATE = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

# Make sure this is up to date, may need to be updated as needed
NATURE_OF_REL = ["Child", "Son", "Daughter", "Colleague", "Friend", "Mentor", "Parent", "Father", "Mother",
"Partner", "Sibling", "Brother", "Sister", "Wife", "Husband", "Spouse", "Grandchild", "Grandparent", "Nephew",
"Niece", "Aunt", "Uncle", "Relative"]

# Make sure this is up to date, may need to be updated as needed
TYPE_OF_ACTIVITY = ["Club", "Event", "Organization", "Job", "Exposition", "Fellowship", "Excavation", "Trip", 
"Project", "Honor Society", "Education"]


# ------------------------------------- #
#		  HELPER FUNCTIONS              #
# ------------------------------------- #

def removePunctuation(col):
	newNames = []
	for name in col:
		before = name
		after  = name.strip(string.punctuation + ' ')
		newNames.append(after)
	return newNames

def seperateWithSlashes(name):
	if ' ' in name:
		print("The name", name, "was seperated by slashes.")
		return '/'.join(name.split())
	return name

def findDelimiter(entry):
	delimiter = detect(entry)
	if delimiter == None:
		print("Couldn't find a delimiter for", entry)
	return delimiter

# ------------------------------------- #
#     FUNCTIONS TO VALIDATE IDs         #
# ------------------------------------- #

def checkIDs(col):
	valid = isUniqueIDs(col)
	for ID in col:
		if not ID.isnumeric() or len(ID) == 0:
			print(ID, "isn't a valid ID. Please change the ID.")
			valid = False
	return valid

def isUniqueIDs(col):
	seen = []
	valid = True
	for ID in col:
		if ID in seen:
			print(ID, "isn't unique... Please change the ID.")
			valid = False
		else:
			seen.append(ID)
	return valid

def inMain(col, sids):
	valid = True
	missing = []
	for ID in col:
		if ID not in sids and ID not in missing:
			missing.append(ID)
			print("The S_ID", ID, "isn't in the MAIN table.")
			valid = False
	return valid

def checkSIDs(col):
	valid = True
	for ID in col:
		if not ID.isnumeric() or len(ID) == 0:
			print(ID, "isn't a valid ID. Please change the ID.")
			valid = False
	return valid


# -------------------------------------- #
#      FUNCTIONS TO VALIDATE NAMES       #
# -------------------------------------- #

def checkNames(col):
	newNames = removePunctuation(col)
	for i in range (len(newNames)):
		if len(newNames[i]) == 1:
			newNames[i] += "."
			print("The name", newNames[i][:1], "changed to", newNames[i])
		elif len(newNames[i]) != 0 and not newNames[i][0].isupper():
			newNames[i] = newNames[i].capitalize()
			print(newNames[i], "was capitalized.")
		newNames[i] = seperateWithSlashes(newNames[i])
	return newNames

# -------------------------------------- #
#      FUNCTIONS TO VALIDATE SEX         #
# -------------------------------------- #

def checkSex(col):
	valid = True
	for entry in col:
		if entry not in "FM ":
			print(entry, "is not a valid inferred sex.")
			valid = False
	return valid

# -------------------------------------- #
#      FUNCTIONS TO VALIDATE DATES       #
# -------------------------------------- #

def isDate(date):
	format = ('%m/%d/%Y')
	try: 
		datetime.datetime.strptime(date, format)
		return True

	except ValueError:
		return False

def checkDates(col):
	valid = True
	for date in col:
		if date != "" and not isDate(date):
			valid = False
			print(date, "isn't a valid date.")
	return valid

# -------------------------------------- #
#    FUNCTIONS TO VALIDATE SOURCES       #
# -------------------------------------- #

def checkSources(col):
	newSources = []
	for entry in col:
		if entry == '':
			continue
		sources = splitSources(entry)
		newEntry = '/'.join(sources)
		checkIsNumbers(sources)
		if entry != newEntry:
			print('Source list', entry, "changed to", newEntry)
		newSources.append(newEntry)
	return newSources

def splitSources(entry):
	if entry.isdigit():
		return [entry]
	sources = entry.split(findDelimiter(entry))
	for i in range(len(sources)):
		sources[i] = sources[i].strip()
	# in case the delimiter in wrongly identified
	for i in sources:
		if len(i) == 1 and not i.isalnum():
			sources.remove(i)
	return sources

def checkIsNumbers(sourceList):
	for source in sourceList:
		if not source.isdigit() and source != '':
			print(source, "is an invalid source.")

# ------------------------------------- #
#	   FUNCTIONS TO VALIDATE            #
#	    BIOGRAPHICAL NOTES              #
# ------------------------------------- #

def checkURL(col):
	for url in col:
		if url == '':
			continue
		try:
			urlopen(url)
			return True
		except URLError:
			print(url, "is an invalid URL")
			return False

# -------------------------------------- #
#    FUNCTIONS TO VALIDATE PROFESSIONS   #
# -------------------------------------- #

# assumes that professions are correctly seperated by a delimiter,
# just not always the right one.
def checkProfessions(col):
	newProfessions = []
	for entry in col:
		delimiter = detect(entry, blacklist = ' ')
		print("delimiter:", delimiter)
		if delimiter == ' ':
			print("Invalid delimiter..")
		professions = splitSources(entry)
		newEntry = '/'.join(professions)
		if entry != newEntry:
			print('The professions', entry, "changed to", newEntry)
		newProfessions.append(newEntry)
	return newProfessions

# -------------------------------------- #
#    FUNCTIONS TO VALIDATE LOCATIONS     #
# -------------------------------------- #

def checkLocations(col):
	newLocations = []
	for location in col:
		if location == '':
			newLocations.append(location)
			continue
		valid = True
		#print("location:", location)
		for i in location:
			if i in string.punctuation and i != ";":
				print(location, "is an invalid location!", i, "is an unpermitted character..")
				valid = False
		if valid:
			split = removePunctuation(location.title().split(';'))
			# check first entry is a continent
			if split[0] not in CONTINENTS:
				print(location, "is invalid: locations need to start with a continent")
			if len(split) > 2 and split[1] == "United States":
				split[2] = convertState(split[2]).strip()
			newLocation = ';'.join(split)
			if newLocation != location:
				print(location, "changed to", newLocation)
			newLocations.append(newLocation)
		else:
			newLocations.append(location)
	return newLocations

def convertState(state):
	if state.upper() in ABBREV_TO_STATE.keys(): 
		state = ABBREV_TO_STATE[state.upper()]
		return state
	if state.title() not in ABBREV_TO_STATE.values():
		print("The state", state, "is invalid..")
	return state.title()

# ------------------------------------- #
#	   FUNCTIONS TO VALIDATE            #
#	      DROP-DOWN LISTS               #
# ------------------------------------- #

def checkNatureOfRel(col):
	newRelationships =  removePunctuation(col)
	for relationship in newRelationships:
		if relationship.title() not in NATURE_OF_REL:
			print("The relationship", relationship, "isn't an option in the drop-down list..")
	return newRelationships

def checkTypeOfActivity(col):
	newActivities =  removePunctuation(col)
	for activity in newActivities:
		if activity.title() not in TYPE_OF_ACTIVITY:
			print("The activity", activity, "isn't an option in the drop-down list..")
	return newActivities

