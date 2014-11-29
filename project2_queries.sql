#1.	Login: Find the user (all attributes) whose username is “bigJim” and password is “IRock1”. 

select * from egccuser where username = "bigJim" and password = "IRock1";

#2.	Change password: Change the password of the user whose username is “bigJim” to “NoBiggie1234”

set SQL_SAFE_UPDATES = 0;
update egccuser set password = "NoBiggie1234" where username = "bigJim";

#3.	View Items I bid on: List all the items (all attributes) that user whose ID is 112 has bid on. 

select * from bid where BuyerID = 112;

#4.	View my items: List all the items (all attributes) that user whose ID is 111 has put up for auction. 

select * from item where SellerID = 111;

#5.	View my purchases: list all the items (title, description, price, category, dateSold and dateShipped) that user whose ID is 112 has purchased.
select title, description, price, category, dateSold, dateShipped from (select * from Purchase natural join item) BuyerInfo where BuyerID = 112; 

#6.	Search by keyword: Display all the items (all attributes) whose description contains the keyword “Service”

select * from item where description like '%Service%';

#7.	Search by category: Display all the items (all attributes) that belong to the category “Textbook”. 

select * from item where category = "Textbook";

#8.	View seller rating: Find the average rating of the seller who is selling item with itemID=2213
	select AVG(rating) from sellerRating where sellerID = (Select sellerID from item where itemID = 2213) group by sellerID;
#9.	View number of bids: Find the number of bids on the item whose ID is 2213
	select count(currentbid) from bid where itemid = 2213 group by itemid;
#10.	View most popular item: Find the item with the most number of bids.

select max(item), itemid from (select count(itemid) as item, ItemID from bid group by itemid) max;

#11.	Put a new item up for auction: itemID is 2215, title is " Android Cookbook”, description is “Problems and Solutions for Android Developers”, startingbid is 5, enddate is October 30th, 2014, category is “reference”, sellerID is 111.
	insert into item values (2215, "Android Cookbook", "Problems and Solutions for Android Developers", 5, 5, 20141030,  111, "open","Reference");

#12.	Ship an item: Change the status of item whose ID is 2212 to “shipped”. Also update the purchase table to indicate that the item was shipped today.

update item set status = "shipped" where itemid = 2212; 
update purchase set dateShipped = date(sysdate()) where itemid = 2212;

#13.	View highest bid: Find the highest bid on the item whose ID is 2211.
	select max(currentbid) from bid where itemid = 2211 group by itemid;
#14.	Place a bid: Place a bid on item whose ID is 2211: the buyerID is 114, the bid is $20 and the bid is placed on October 17th,2014 at 11:25AM. 
	insert into bid values( 114, 2211, 20141017, "11:25:00", 20);
#15.	Rate a seller: Place a rating where buyer whose ID is 113, sellerID is 111 and the rating is 1. Use today’s date as the date for the rating. Do not specify a description.

insert into sellerRating values (111, 113, 1,'', date(sysdate()));

#16.	Close an auction: Close the auction for item whose ID is 2211 by setting the highest bid as the price and today’s date as the purchase date. Note that for this query, you need to do multiple insert/update statements. 

insert into purchase values ((select buyerid from (select max(currentbid), buyerid from bid where itemid = 2211 group by itemid) FinalBidder), 2211, (select highestbid from item where itemid = 2211), date(sysdate()), null); 

#17.	View top sellers: Display the sellers in descending order of their average rating.

select sellerid, avg(rating) from sellerrating group by sellerid order by avg(rating) desc;
