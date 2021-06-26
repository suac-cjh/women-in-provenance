
import string

# --------------------------------------- #
#		FUNCTIONS TO VALIDATE IDs         # 													  
# --------------------------------------- #

def checkIDs(col):
	if not isUniqueIDs(col):
		return False
	for ID in col:
		if not ID.isdigit():
			print(ID, "isn't a digit. Please change the ID.")
			return False
	return True

def isUniqueIDs(col):
	seen = []
	for ID in col:
		if ID in seen:
			print(ID, "isn't unique... Please change the ID.")
			return False
		else:
			seen.append(ID)
	return True

# -------------------------------------- #
#      FUNCTIONS TO VALIDATE NAMES       # 													  
# -------------------------------------- #

def validateNames(col):
	newNames = 

def removePunctuation(col):
	newNames = []
	for name in col:
		before = name
		after  = name.strip(string.punctuation)
		if before != after:
			print(before, " changed to ", after)
		newNames.append(after)
	return newNames
		