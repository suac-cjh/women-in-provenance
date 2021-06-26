
import string

# --------------------------------------------------------------- #
#						  CONSTANTS		                          # 													  
# --------------------------------------------------------------- #
punc = string.punctuation 

# --------------------------------------------------------------- #
#						HELPER FUNCTIONS                          # 													  
# --------------------------------------------------------------- #

#def removePunctuation(word):
#	return word.strip(punc)	

# --------------------------------------------------------------- #
#					FUNCTIONS TO VALIDATE IDs                     # 													  
# --------------------------------------------------------------- #

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

# --------------------------------------------------------------- #
#					FUNCTIONS TO VALIDATE NAMES                   # 													  
# --------------------------------------------------------------- #

def validateNames(col):
	for name in col:
		name.strip(punc)
		