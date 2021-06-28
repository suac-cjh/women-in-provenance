import csv
import datetime
from detect_delimiter import detect  #to detect the source delimiter used
import string
from urllib.request import urlopen, URLError	#to check validity of URLs

# ------------------------------------- #
#		  HELPER FUNCTIONS              #
# ------------------------------------- #

def removePunctuation(col):
	newNames = []
	for name in col:
		before = name
		after  = name.strip(string.punctuation + ' ')
		if before != after:
			print("The name", before, "changed to", after)
		newNames.append(after)
	return newNames

def seperateWithSlashes(name):
	if ' ' in name:
		print(name, "was seperated by slashes.")
		return '/'.join(name.split())
	return name

def findDelimiter(entry):
	delimiter = detect(entry)
	if delimiter == None:
		print("Couldn't find a delimiter for", entry)
		return '/'
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
	return sources

def checkIsNumbers(sourceList):
	for source in sourceList:
		if not source.isdigit() and source is not '':
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


