import mysql.connector


def main():
	running = True
	login = True
	global username #useful for using the username without reinput for command 0
	while running== True:
		username = raw_input("Please enter your username\n")
		password = raw_input("Please enter your password\n")
		database = raw_input("Please enter your schema\n")
		host = 'COMPDBS300'
		cnx = mysql.connector.connect(username, password, host, database)
		cursor = cnx.cursor()
		login = interface()
		print(login)

def interface():
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
