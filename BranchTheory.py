import mysql.connector


def main():
	running = True
	login = False
	global username #useful for using the username without reinput for command 0
	##Not sure how I feel about the above, do we really need globals or can we just keep passing, besides, the way this works if we want to relog we cant change this easily.

	while running== True:
		cnx = mysql.connector.connect(user = 'u249454', password = 'p249454', host = 'COMPDBS300', database = 'schema249454')
		cursor = cnx.cursor()
		username = input("Please enter your username\n")
		pword = input("Please enter your password\n")
		login = loginAttempt(username, pword, cursor, cnx)
		if login == True:
			print("Login Successful")
			while(login == true):
				login = interface(username, pword)
		else:
			print("Login Failed, would you like you like to try again? Y/N")
			response = input()
			if

def interface(username, pword):
	print("0 : Change my Password")
	print("1 : View Items I bid on")
	print("2 : View my items")
	print("3 : View my purchases")
	print("4 : Search by keyword")
	print("5 : Search by category")
	print("6 : View seller rating")
	print("7 : View number of bids")
	print("8 : View most popular item")
	print("9 : Put a new item up for auction")
	print("10 : Ship an item")
	print("11 : View highest bid")
	print("12 : Place a bid")
	print("13 : Rate a seller")
	print("14 : Close an auction")
	print("15 : View top sellers")
	print("16 : Logout")
	choice = input("Enter a number\n")
	choice = int(choice)
	if(choice == 0):
		changePass(username)
	elif(choice == 1):
		viewMyBid()
	elif(choice == 2):
		viewItems()
	elif(choice == 3):
		viewPurchases
	elif(choice == 4):
		searchWord()
	elif(choice == 5):
		searchCata()
	elif(choice == 6):
		viewSellerRating()
	elif(choice == 7):
		viewNumBids()
	elif(choice == 8):
		viewPopItem()
	elif (choice == 9):
		newItemAuction()
	elif(choice == 10):
		shipItem()
	elif(choice == 11):
		viewHighBid()
	elif(choice == 12):
		placeBid()
	elif(choice == 13):
		rateSeller()
	elif(choice == 14):
		closeAuction()
	elif(choice == 15):
		viewTopSellers()
	elif(choice == 16):
		return False
	else:
		print("Invalid entry")


def loginAttempt(username, password, cursor, cnx):
	numrows = 0
	query = ("SELECT UserID from egccuser where username = %s and password = %s")
	qdata = (username, password)
	cursor.execute(query, qdata)
	for(UserID) in cursor:
		numrows += 1
	if numrows == 1:
		return True
	else:
		return False
	
def changePass(username):
        print ("What do you want to change your password to?")
        password = raw_input() #using raw_input() instead of input() solved the issue of the name not being defined upon input of a string.

        query = ("update egccuser set password = %s where username = %s")
        qdata = (password, username)
        try:
                cursor.execute(query,qdata)
                numrows = int(cursor.rowcount)
                print(str(numrows) + " were updated")
                cnx.commit()
        except mysql.connector.Error as err:
                print("Update was not successful " + str(err))
        

main()
