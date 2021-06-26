
import string
import datetime
import dateutil.parser as parser

# ------------------------------------- #
#		FUNCTIONS TO VALIDATE IDs       # 													  
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


