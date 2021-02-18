import sys
import string



# 							class declarations



class Token:
	def __init__(self, tok, tType):
		self.tok = tok
		self.tType = str(tType)

class Location:
	def __init__(self):
		self.start = 0
		self.current = 0



# 							helper functions



# function to create a token
def createTok(arg, loc, tokList, tType):
	loc.current += 1
	tok = Token(arg[loc.start:loc.current], tType)
	tokList.append(tok)
	loc.start = loc.current
	
	return

# function to create a keyword token
def createKeyTok(arg, loc, tokList):
	loc.current += 1
	tok = Token(arg[loc.start:loc.current], arg[loc.start:loc.current])
	tokList.append(tok)
	loc.start = loc.current
	
	return

# function to check if punctuation
def ispunct(char):
	if char in string.punctuation:
		return True
	else:
		return False
	
# function to check if hex
def ishex(char):
	if char in string.hexdigits:
		return True
	else:
		return False

# function to check if octal
def isoctal(char):
	octalDig = "01234567"
	
	if char in octalDig:
		return True
	else:
		return False



# 							logic functions



# function for punctuation tokens
def punctTok(arg, loc, tokList):
	createTok(arg, loc, tokList, "punc")
	
	return



# function for float tokens
def floatTok(arg, loc, tokList):
	while loc.current < len(arg):
		#print("	", loc.current)
		if loc.current < len(arg) - 1 and not str.isnumeric(arg[loc.current + 1]):
			#print("	" + arg[loc.current] + " - not numeric : " + str(loc.current + 1))
			
			# now we have two cases to cover: if it's not an integer, the float token ends
			createTok(arg, loc, tokList, "floating point")
			
			break
			
		elif loc.current == len(arg) - 1:
			#print("	" + arg[loc.current] + " - numeric : " + str(loc.current))
			createTok(arg, loc, tokList, "floating point")
			
			break
		
		loc.current += 1
	
	return



# function for decimal integers
def decTok(arg, loc, tokList):
	while loc.current < len(arg):
		#print("	", loc.current)
		if loc.current < len(arg) - 1 and not str.isnumeric(arg[loc.current + 1]):
			#print("	" + arg[loc.current] + " - not numeric : " + str(loc.current + 1))
			
			# now we have two cases to cover:
			#	1) it's not a decimal, but it's a float
			#	2) it's not any kind of integer, and the token ends
			
			if loc.current < len(arg) - 2 and arg[loc.current + 1] == '.' and str.isnumeric(arg[loc.current + 2]):
				#print("float found")
				
				loc.current += 2
				floatTok(arg, loc, tokList)
				
				break
			
			else:
				createTok(arg, loc, tokList, "decimal integer")
				
				break
			
		elif loc.current == len(arg) - 1:
			#print("	" + arg[loc.current] + " - numeric : " + str(loc.current))
			createTok(arg, loc, tokList, "decimal integer")
			
			break
		
		loc.current += 1
	
	return



# function for octal integers
def octTok(arg, loc, tokList):
	while loc.current < len(arg):
		#print("	", loc.current)
		if loc.current < len(arg) - 1 and not isoctal(arg[loc.current + 1]):
			#print("	" + arg[loc.current] + " - not octal : " + str(loc.current + 1))
			
			# now we have three cases to cover:
			#	1) it's not an octal, but it's a decimal
			#	2) it's not an octal, but it's a float
			#	3) it's not any kind of integer, and the token ends
			
			if str.isnumeric(arg[loc.current + 1]):
				decTok(arg, loc, tokList)
				
				break
			
			elif loc.current < len(arg) - 2 and arg[loc.current + 1] == '.' and str.isnumeric(arg[loc.current + 2]):
				#print("float found")
				
				loc.current += 2
				floatTok(arg, loc, tokList)
				
				break
			
			else:
				createTok(arg, loc, tokList, "octal integer")
				
				break
			
		elif loc.current == len(arg) - 1:
			#print("	" + arg[loc.current] + " - numeric : " + str(loc.current))
			createTok(arg, loc, tokList, "octal integer")
			
			break
		
		loc.current += 1
	
	return



# function for hex integers
def hexTok(arg, loc, tokList):
	while loc.current < len(arg):
		#print("	", loc.current)
		if loc.current < len(arg) - 1 and not ishex(arg[loc.current + 1]):
			#print("	" + arg[loc.current] + " - not numeric : " + str(loc.current + 1))
			createTok(arg, loc, tokList, "hexadecimal integer")
			
			break
			
		elif loc.current == len(arg) - 1:
			#print("	" + arg[loc.current] + " - numeric : " + str(loc.current))
			createTok(arg, loc, tokList, "hexadecimal integer")
			
			break
		
		loc.current += 1
	
	return
	



# function for determining how long a word token is
def wordTok(arg, loc, tokList):
	while loc.current < len(arg):
		#print("	", loc.current)
		if loc.current < len(arg) - 1 and not str.isalpha(arg[loc.current + 1]) and not str.isnumeric(arg[loc.current + 1]):
			#print("	" + arg[loc.current] + " - not alpha : " + str(loc.current + 1))
			createTok(arg, loc, tokList, "word")
			
			break
			
		elif loc.current == len(arg) - 1:
			#print("	" + arg[loc.current] + " - alpha : " + str(loc.current))
			createTok(arg, loc, tokList, "word")
			
			break
		
		loc.current += 1
	
	return




# function to tokenize the input
def tokenize(arg):
	tokList = []
	
	#create variables to hold both the current and the starting locations
	loc = Location()
	
	# we can't use a for loop, because we need to be able to manually set the index
	# so instead we use a while loop
	while loc.current < len(arg):
		#print(loc.current)
		
		if str.isspace(arg[loc.current]):
			loc.current += 1
			loc.start = loc.current
			
		elif str.isalpha(arg[loc.current]):
			#print("alpha found")
			wordTok(arg, loc, tokList)
			
		elif ispunct(arg[loc.current]):
			#print("punct found")
			punctTok(arg, loc, tokList)
			
		elif loc.current < len(arg) - 1 and arg[loc.current:loc.current + 2].lower() == "0x":
			#print("hex found")
			loc.current += 1
			hexTok(arg, loc, tokList)
			
		elif arg[loc.current] == '0':
			#print("octal found")
			octTok(arg, loc, tokList)
			
		elif str.isnumeric(arg[loc.current]):
			#print("decimal found")
			decTok(arg, loc, tokList)
			
		else:
			return None
	
	return tokList



def printList(tokList):
	if not tokList:
		print("The list is empty.")
	
	else:
		print("Tokens:")
		for x in range(len(tokList)):
			print("	" + str(tokList[x].tType) + ": " + str(tokList[x].tok))
	
	return




def main():
	if len(sys.argv) != 2:
		print("Expected usage: \"python main.py <input>\"")
		return
	
	print("Arg to tokenize: \"" + str(sys.argv[1]) + "\"")
	
	tokList = tokenize(sys.argv[1])
	
	printList(tokList)
	
if __name__ == "__main__":
	main()
