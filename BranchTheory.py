import mysql.connector
import datetime
import time


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
	userID = getID(username, pword, cursor, cnx)
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
		return True
	elif(choice == 1):
		viewMyBid(userID, cursor)
		return True
	elif(choice == 2):
		viewItems(userID, cursor)
		return True
	elif(choice == 3):
		viewPurchases(userID, cursor) #Error global id userid not defined pass it
		return True
	elif(choice == 4):
		searchWord(cursor, cnx)
		return True
	elif(choice == 5):
		searchCata(cursor)
		return True
	elif(choice == 6):
		viewSellerRating(cursor, cnx)
		return True
	elif(choice == 7):
		viewNumBids(cursor)
		return True
	elif(choice == 8):
		viewPopItem(cursor, cnx)  #Some Kinda error gives a rand num and then 2211 but the most pop item is 2214
		return True
	elif (choice == 9):
		newItemAuction(userID, cursor, cnx)
		return True
	elif(choice == 10):
		shipItem(cursor, cnx)
		return True
	elif(choice == 11):
		viewHighBid(cursor)
		return True
	elif(choice == 12):
		placeBid(userID, cursor, cnx)
		return True
	elif(choice == 13):
		rateSeller(userID, cursor, cnx)
		return True
	elif(choice == 14):
		closeAuction()
		return True
	elif(choice == 15):
		viewTopSellers()
		return True
	elif(choice == 16):
		return False
	else:
		print("Invalid entry")
		return True


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

def getID(username, password, cursor, cnx): 
	query = ("SELECT UserID from egccuser where username = %s and password = %s") 
	qdata = (username, password)
	cursor.execute(query, qdata)
	for (UserID) in cursor:
		return int(UserID[0])
		
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


def viewItems(UserID, cursor): 
        query = ("SELECT ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category from item where SellerID = %s") 
        cursor.execute(query, (UserID,))
        for (ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category) in cursor:
                print(str(ItemID) + "\t" + str(title) + "\t"+str(description)+"\t"+str(startingBid)+"\t"+str(highestBid)+"\t"+str(endDate)+"\t"+str(SellerID)+"\t"+str(status)+"\t"+str(category) +"\n")


def viewPurchases(UserID, cursor): #It says UserID isn't defined and that it needs to be passed.  Obviously it's being passed.
        query = ("SELECT title, description, price, category, dateSold, dateShipped from (select * from Purchase natural join item) BuyerInfo where BuyerID = %s")
        cursor.execute(query, (UserID,))
        for (title, description, price, category, dateSold, dateShipped) in cursor:
                print(str(title)+"\t"+str(description)+"\t"+str(price)+"\t"+str(category)+"\t"+str(dateSold)+"\t"+str(dateShipped))

def searchWord(cursor, cnx): 
        print ("What keyword do you want to search for?")
        qdata = input()
        qdata = '%' + qdata + '%'
        query = ("SELECT ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category from item where description like %s")
        cursor.execute(query,(qdata,))
        for (ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category) in cursor:
                print(str(ItemID) + "\t" + str(title) + "\t"+str(description)+"\t"+str(startingBid)+"\t"+str(highestBid)+"\t"+str(endDate)+"\t"+str(SellerID)+"\t"+str(status)+"\t"+str(category))


def viewSellerRating(cursor, cnx): 
        print ("What is an Item ID of the seller?")
        qdata = input()
        query = ("select AVG(rating) from sellerRating where sellerID = (Select sellerID from item where itemID = %s) group by sellerID")
        cursor.execute(query,(qdata,))
        for rating in cursor:
               print(str(rating[0]))


def viewPopItem(cursor, cnx): #Need to fix the SQL and possibly the output (but otherwise prints fine)
        query = ("select max(item), itemid from (select count(itemid) as item, ItemID from bid group by itemid) max")
        cursor.execute(query)
        for (item, itemid) in cursor:
                print(str(item)+"\t"+str(itemid))

def shipItem(cursor, cnx): 
        print("What is the Item ID of the item you have shipped?")
        qdata = input()
        try:
                query = ("update item set status = 'shipped' where itemid = %s")
                cursor.execute(query,(qdata,))
                cnx.commit()
                query = ("update purchase set dateShipped = date(sysdate()) where itemid = %s")
                cursor.execute(query,(qdata,))
                cnx.commit()
                print("Item status changed to shipped successfully!")
        except mysql.connector.Error as err:
                print("Update was not successful " + str(err))



def viewMyBid(UserID, cursor):
		query = ("Select distinct ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category from item natural join(select itemID from bid where BuyerID = %s)as temp")
		cursor.execute(query, (UserID,))
		for (ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category) in cursor:
			print(str(ItemID) + "\t" + str(title) + "\t"+str(description)+"\t"+str(startingBid)+"\t"+str(highestBid)+"\t"+str(endDate)+"\t"+str(SellerID)+"\t"+str(status)+"\t"+str(category) +"\n")

def searchCata(cursor):
	query = ("Select ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category from item where category = %s")
	word = input("Enter the category you would like to search\n")
	cursor.execute(query, (word,))
	for (ItemID, title, description, startingBid, highestBid, endDate, SellerID, status, category) in cursor:
		print(str(ItemID) + "\t" + str(title) + "\t"+str(description)+"\t"+str(startingBid)+"\t"+str(highestBid)+"\t"+str(endDate)+"\t"+str(SellerID)+"\t"+str(status)+"\t"+str(category) +"\n")
	
def viewNumBids(cursor):
	query = ("select count(currentbid) itemNum from bid where itemid = %s group by itemid")
	itemID = input("Enter the ID of the item of which you wish to know the current number of bids\n")
	cursor.execute(query,(itemID,))
	for itemNum in cursor:
		print(str(itemNum[0]))

def newItemAuction(userID, cursor, cnx):
	query = ("Select max(ItemID) maxNum from item")
	cursor.execute(query)
	HighID = 0
	for maxNum in cursor:
		HighID = int(maxNum[0])
	HighID += 1
	query = ("insert into item(title, startingBid, endDate, category, SellerID, ItemID) values(%s, %s, %s, %s, %s, %s)")
	title = input("What is the name of your item?\n")
	sBid = input("What is the starting bid?\n")
	eD = input("What is the end date? please enter in the form YYYYMMDD.\n")
	now = time.strftime("%Y%m%d")
	if int(eD) < int(now):
		print("You can now have an end date before the current date")
		return
	cate = input("Enter the category for your item\n")
	qdata = (title, sBid, eD, cate, userID, HighID)
	cursor.execute(query, qdata)
	cnx.commit()
	print("Item listed successfully!")

def viewHighBid(cursor):
	query = ("select max(currentbid) num from bid where itemid = %s group by itemid")
	itemID = input("Enter the id of the item for which you wish to know the highest current bid\n")
	try:
		cursor.execute(query, (itemID,))
		for num in cursor:
			print(num[0])
	except:
		print("Invalid item ID")
		
def placeBid(userID, cursor, cnx):
        print("What is the Item ID of the item you want to bid on?")
        itemID = input()
        print("How much would you like to bid?")
        amount = input()
        query = ("insert into bid values( %s, %s, date(sysdate()), time(sysdate()), %s)")
        qdata = (userID, itemID, amount)
        try:
                cursor.execute(query,qdata)
                cnx.commit()
                print("You have bid successfully!")
        except mysql.connector.Error as err:
                print("Bid was not successful " + str(err))        

def rateSeller(userID, cursor, cnx): #I think this works.  It makes sense for it to be limited so that the buyer can only rate the seller once we need time added for flexibility
        print("What is the seller ID?")
        seller = input()
        print("What rating do you want to give the seller?")
        rating = input()
        query = ("insert into sellerRating values ( %s, %s, %s, null, date(sysdate()))")
        qdata = (seller, userID, int(rating))
        try:
                cursor.execute(query, qdata)
                cnx.commit()
                print("Rating submitted successfully!")
        except mysql.connector.Error as err:
                print("Rating was not successful " + str(err))        

	
main()
