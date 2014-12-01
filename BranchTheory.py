import mysql.connector


def main():
	running = True
	login = False
	while running== True:
		cnx = mysql.connector.connect(user = 'u459508', password = 'p459508', host = 'COMPDBS300', database = 'schema459508')
		cursor = cnx.cursor()
		username = input("Please enter your username\n")
		pword = input("Please enter your password\n")
		login = loginAttempt(username, pword, cursor, cnx)
		if login == True:
			print("Login Successful")
			while(login == True):
				login = interface(username, pword, cursor, cnx)
		else:
			print("Login Failed, would you like you like to try again? enter E to exit.")
			response = input()
			if response.upper() == "E":
				running = False
				print("Have a nice day")
			
			

def interface(username, pword, cursor, cnx): #I added a pass cursor and cnx so the functions can access them. It complained about cursor not being a global variable.
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
		changePass(username, cursor, cnx)
	elif(choice == 1):
		viewMyBid()
	elif(choice == 2):
		viewItems(username, cursor, cnx)
	elif(choice == 3):
		viewPurchases(username, cursor, cnx)
	elif(choice == 4):
		searchWord(cursor, cnx)
	elif(choice == 5):
		searchCata()
	elif(choice == 6):
		viewSellerRating(cursor, cnx)
	elif(choice == 7):
		viewNumBids()
	elif(choice == 8):
		viewPopItem(cursor, cnx)
	elif (choice == 9):
		newItemAuction()
	elif(choice == 10):
		shipItem(cursor, cnx)
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
	#print(cursor.UserID)
	for(UserID) in cursor:
		numrows += 1
	if numrows == 1:
		return True
	else:
		return False

def getID(username, cursor, cnx): #Doesn't throw errors now at least
	query = ("SELECT UserID from egccuser where username = '%s'") #had to add single quotes.  I don't know why. xD
	qdata = (username)
	cursor.execute(query,qdata)
	for (UserID) in cursor:
		return UserID
		
def changePass(username, cursor, cnx):
        print ("What do you want to change your password to?")
        password = input()
        query = ("UPDATE egccuser set password = %s where username = %s")
        qdata = (password, username)
        try:
                cursor.execute(query,qdata)
                numrows = int(cursor.rowcount)
                print(str(numrows) + " were updated")
                cnx.commit()
        except mysql.connector.Error as err:
                print("Update was not successful " + str(err))


def viewItems(username, cursor, cnx): #the query SHOULD be working.  There's a problem with %s.  :/ If I run it with a number for SellerID, it works perfectly.
        qdata = getID(username, cursor, cnx)
        query = ("SELECT ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category from item where SellerID = %s") 
        cursor.execute(query,qdata)
        for (ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category) in cursor:
                print(str(ItemID) + "\t" + str(title) + "\t"+str(description)+"\t"+str(startingBid)+"\t"+str(highestBid)+"\t"+str(endDate)+"\t"+str(SellerID)+"\t"+str(status)+"\t"+str(category))


def viewPurchases(username, cursor, cnx): #same problem.     oops... this was 3.  Sorry 
        qdata = getID(username, cursor, cnx)
        query = ("SELECT title, description, price, category, dateSold, dateShipped from (select * from Purchase natural join item) BuyerInfo where BuyerID = %s")
        cursor.execute(query,qdata)
        for (title, description, price, category, dateSold, dateShipped) in cursor:
                print(str(title)+"\t"+str(description)+"\t"+str(price)+"\t"+str(category)+"\t"+str(dateSold)+"\t"+str(dateShipped))

def searchWord(cursor, cnx): #Doesn't do the keyword search correctly.  Brings up the same 3 things no matter what??
        print ("What keyword do you want to search for?")
        qdata = input()
        query = ("select ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category from item where description like '%%s%'")
        cursor.execute(query,qdata)
        for (ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category) in cursor:
                print(str(ItemID) + "\t" + str(title) + "\t"+str(description)+"\t"+str(startingBid)+"\t"+str(highestBid)+"\t"+str(endDate)+"\t"+str(SellerID)+"\t"+str(status)+"\t"+str(category))


def viewSellerRating(cursor, cnx): #same problem
        print ("What is an Item ID of the seller?")
        qdata = input()
        query = ("select AVG(rating) from sellerRating where sellerID = (Select sellerID from item where itemID = %s) group by sellerID")
        cursor.execute(query,qdata)
        for rating in cursor:
               print(str(rating))


def viewPopItem(cursor, cnx): #Need to fix the SQL and possibly the output (but otherwise prints fine)
        query = ("select max(item), itemid from (select count(itemid) as item, ItemID from bid group by itemid) max")
        cursor.execute(query)
        for (item, itemid) in cursor:
                print(str(item)+"\t"+str(itemid))

def shipItem(cursor, cnx): #same problem
        print("What is the Item ID of the item you have shipped?")
        qdata = input()
        try:
                query = ("update item set status = 'shipped' where itemid = %s")
                cursor.execute(query,qdata)
                cnx.commit()
                query = ("update purchase set dateShipped = date(sysdate()) where itemid = %s")
                cursor.execute(query,qdata)
                cnx.commit()
        except mysql.connector.Error as err:
                print("Update was not successful " + str(err))
main()
