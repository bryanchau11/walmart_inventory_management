# walmart_inventory_management

## Heroku Link to test the app
- [http://walmart-inventory-management.herokuapp.com/index]

## Requirements
1. `npm install`
2. `pip install -r requirements.txt`
3. Make sure you have python 3, pip, sqlite3 installed. 

## Run Application
1. Run command in terminal (in your project directory): `npm run build`. This will update anything related to your `App.js` file (so `public/index.html`, any CSS you're pulling in, etc).
2. Run command in terminal (in your project directory): `python3 app.py`
3. Preview web page in browser 'localhost:8081/' (or whichever port you're using)


## Checking data stored in the walmart.db
1. Run command in the terminal (in your project directory): `sqlite3 walmart.db`
2. `.table` to view all the tables.
3. `.header on` to enable headers.
4. `.mode column` to split column for better view.
5. Now enter your SQL queries (anything you want).

## Project submission:
1. (20 points.) E-R diagram of the design of your system (you may draw this on paper and scan) 
- [https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&layers=1&nav=1&title=DATABASE%20FINAL%20DIAGRAM.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1LrFbkdq1EdvtV0OK49Pk1Qk1h6BBvsBL%26export%3Ddownload]
 
2. (20 points.) SQL DDL (create table) commands which define the structure of your database, with the appropriate constraints, e.g., primary key, foreign key, not null, check
- Please refer to `create_table()` function on line 179 in App.py

3. (10 points.) Brief detail on how the data were generated, e.g., the scripts which were used to generate the data (which do not have to be original, you could even have used or modified the instructor's python script, for example), or where the data were obtained (for example, the Walmart website)
- function `get_product_json()` on line 425: It fetches data from Walmart API, then store it in each variable and return if needed. Same with `get_store_info()`. Then I use python to write data to json file, and csv files which are `product_table.json`, `vendorlist.csv`, `customerlist.csv`. Those commands can be found in most commented out section in app.py (for instance, line 525 to 551)

4. (10 points.) The data itself, which were generated from (3.)
- `product_table.json` stores product information, store information and brand information.
- `vendorlist.csv` stores vendor information.
- `customerlist.csv` stores customer information.

5. (20 points.) At least five interesting queries on this database / data

a. `select distinct p.productName, pu.usItemID, sum(pu.quantity) from Product p, purchase pu where p.usItemID = pu.usItemID group by pu.usItemID Order by sum(pu.quantity) desc;`
=> This gives the total amount of sales for each product in the database

b. `SELECT distinct s.storeAddress, s.storeID, pu.usItemID, sum(pu.quantity)sold FROM Product p, purchase pu, Store s  where pu.usItemID = p.usItemID AND s.storeID = p.StoreID GROUP BY s.storeID  Order by sum(pu.quantity) desc;`
=> This gives the total amount of products a store has sold and ranks them

c. `select Store.storeAddress, Store.storePhone, Store.storeHour from Store, is_sold_S_P, purchase where Store.storeID = is_sold_S_P.storeID and is_sold_S_P.usItemID = purchase.usItemID and purchase.quantity = (select max(purchase.quantity) from purchase);`

=> Get the store address, phone # and hour of the store where it has an item that is a best-seller.

d. `select Customer.customerID, Customer.customerName from Customer, is_visited, is_sold_S_P, has_type where Customer.customerID = is_visited.customerID and is_visited.storeID = is_sold_S_P.storeID and is_sold_S_P.usItemID = has_type.usItemID and has_type.type = "Bed Sheets";`
=> Get customer ids and customer names of the customers who visited the store that has the item of type "Bed Sheets"

e. `select P.productName, P.price, T.type from Product as P LEFT JOIN has_type as T ON P.usItemID = T.usItemID LEFT JOIN productType as PT ON T.type = PT.type where P.price > 10 and PT.offerType = "ONLINE_ONLY" GROUP BY P.productName Order by P.price `
=> Get name, price and type of every product that is only sold online with a price greater than $10. 

f. `select Customer.customerID, Customer.customerName from Customer, is_visited, is_sold_S_P, has_type, productType where Customer.customerID = is_visited.customerID and is_visited.storeID = is_sold_S_P.storeID and is_sold_S_P.usItemID = has_type.usItemID and has_type.type = productType.type and productType.departmentName = "PERSONAL CARE" GROUP BY Customer.customerID;`

=> Get names and ids of customers who has visited stores and has bought products which are in PERSONAL CARE department.

6. (20 points.) A 5-10 minute video presentation of your system, outlining the idea of the organization, the E-R diagram, the data generation, and the running of the queries given in (5.)
- [https://youtu.be/8lK9j8aMPZA]