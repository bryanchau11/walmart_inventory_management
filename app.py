import flask
from flask_login.utils import login_required
import os
import json
import sqlite3
import requests
from dotenv import load_dotenv, find_dotenv
import json
import random
import sys
import csv
from csv import reader

load_dotenv(find_dotenv())
app = flask.Flask(__name__, static_folder="./build/static")
# This tells our Flask app to look at the results of `npm build` instead of the
# actual files in /templates when we're looking for the index page file. This allows
# us to load React code into a webpage. Look up create-react-app for more reading on
# why this is necessary.
app.secret_key = "hey"
bp = flask.Blueprint("bp", __name__, template_folder="./build")


@bp.route("/index")
def index():
    con = sqlite3.connect("walmart.db")
    cur = con.cursor()
    product_list_header = list(
        zip([header[0] for header in cur.execute("select * from product").description])
    )

    product_list = cur.execute("select * from product").fetchall()
    product_list.insert(0, tuple(product_list_header))
    #
    brand_list_header = list(
        zip([header[0] for header in cur.execute("select * from brand").description])
    )
    brand_list = cur.execute("select * from brand").fetchall()
    brand_list.insert(0, tuple(brand_list_header))
    #
    productType_list_header = list(
        zip(
            [
                header[0]
                for header in cur.execute("select * from productType").description
            ]
        )
    )
    productType_list = cur.execute("select * from productType").fetchall()
    productType_list.insert(0, tuple(productType_list_header))
    #
    store_list_header = list(
        zip([header[0] for header in cur.execute("select * from store").description])
    )
    store_list = cur.execute("select * from store").fetchall()
    store_list.insert(0, tuple(store_list_header))

    #
    vendor_list_header = list(
        zip([header[0] for header in cur.execute("select * from vendor").description])
    )
    vendor_list = cur.execute("select * from vendor").fetchall()
    vendor_list.insert(0, tuple(vendor_list_header))
    #
    customer_list_header = list(
        zip([header[0] for header in cur.execute("select * from customer").description])
    )
    customer_list = cur.execute("select * from customer").fetchall()
    customer_list.insert(0, tuple(customer_list_header))
    #
    is_visited_list_header = list(
        zip(
            [
                header[0]
                for header in cur.execute("select * from is_visited").description
            ]
        )
    )
    is_visited_list = cur.execute("select * from is_visited").fetchall()
    is_visited_list.insert(0, tuple(is_visited_list_header))
    #
    is_paid_list_header = list(
        zip([header[0] for header in cur.execute("select * from is_paid").description])
    )
    is_paid_list = cur.execute("select * from is_paid").fetchall()
    is_paid_list.insert(0, tuple(is_paid_list_header))
    #
    is_sold_V_B_list_header = list(
        zip(
            [
                header[0]
                for header in cur.execute("select * from is_sold_V_B").description
            ]
        )
    )
    is_sold_V_B_list = cur.execute("select * from is_sold_V_B").fetchall()
    is_sold_V_B_list.insert(0, tuple(is_sold_V_B_list_header))
    #
    has_type_list_header = list(
        zip([header[0] for header in cur.execute("select * from has_type").description])
    )
    has_type_list = cur.execute("select * from has_type").fetchall()
    has_type_list.insert(0, tuple(has_type_list_header))
    #
    is_under_list_header = list(
        zip([header[0] for header in cur.execute("select * from is_under").description])
    )
    is_under_list = cur.execute("select * from is_under").fetchall()
    is_under_list.insert(0, tuple(is_under_list_header))
    #
    is_sold_S_P_list_header = list(
        zip(
            [
                header[0]
                for header in cur.execute("select * from is_sold_S_P").description
            ]
        )
    )
    is_sold_S_P_list = cur.execute("select * from is_sold_S_P").fetchall()
    is_sold_S_P_list.insert(0, tuple(is_sold_S_P_list_header))
    #
    purchase_list_header = list(
        zip([header[0] for header in cur.execute("select * from purchase").description])
    )
    purchase_list = cur.execute("select * from purchase").fetchall()
    purchase_list.insert(0, tuple(purchase_list_header))
    DATA = {
        "product": product_list,
        "productType": productType_list,
        "brand": brand_list,
        "store": store_list,
        "vendor": vendor_list,
        "customer": customer_list,
        "is_visited": is_visited_list,
        "is_paid": is_paid_list,
        "is_sold_V_B": is_sold_V_B_list,
        "has_type": has_type_list,
        "is_under": is_under_list,
        "is_sold_S_P": is_sold_S_P_list,
        "purchase": purchase_list,
    }
    data = json.dumps(DATA)
    return flask.render_template(
        "index.html",
        data=data,
    )


app.register_blueprint(bp)

###
""" 
con = sqlite3.connect("walmart.db")
cur = con.cursor()
f = open(
    "product_table.json",
)
data = json.load(f)
storeID = []
for i in data["store"]:
    storeID.append(i["storeID"])


def checkDup(list):

    dict = {}
    for i in list:
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1
    print(dict)


checkDup(storeID)
"""


def create_table():
    con = sqlite3.connect("walmart.db")
    cur = con.cursor()
    f = open(
        "product_table.json",
    )
    usItemID = []
    upc = []
    storeID = []
    price = []
    productName = []
    brandName = []
    type = []
    offerType = []
    departmentName = []

    data = json.load(f)
    for i in data["product"]:

        # Brand table
        brandName.append(i["brandName"])

        # ProductType table

        type.append(i["type"])
        offerType.append(i["offerType"])
        departmentName.append(i["departmentName"])

    # Store table
    storeID = []
    storeAddress = []
    storePhone = []
    storeHour = []
    for i in data["store"]:
        storeID.append(i["storeID"])
        storeAddress.append(i["storeAddress"])
        storePhone.append(i["storePhone"])
        storeHour.append(i["storeHour"])

    # Vendor table
    sellerName = []
    sellerReviewCount = []
    for i in data["vendor"]:
        sellerName.append(i["sellerName"])
        sellerReviewCount.append(i["sellerReviewCount"])

    # Customer Table
    customerID = []
    customerName = []
    paidMemberShip = []
    for i in data["customer"]:
        customerID.append(i["customerID"])
        customerName.append(i["customerName"])
        paidMemberShip.append(i["paidMemberShip"])

    # Create table product
    # print(json.dumps(data["product"], indent=4, sort_keys=True))

    for i in data["product"]:
        # Product table
        usItemID.append(i["usItemID"])
        upc.append(i["upc"])
        storeID.append(i["storeID"])
        price.append(i["price"])
        productName.append(i["productName"])

    product = list(zip(usItemID, upc, storeID, price, productName))
    cur.execute(
        "create table if not exists product(usItemID INT PRIMARY KEY, UPC INT, storeID INT, price INT, productName VARCHAR(500))"
    )
    cur.executemany("INSERT INTO product VALUES(?,?,?,?,?)", product)

    # Create table brand
    cur.execute("create table if not exists brand(brandName VARCHAR(300) PRIMARY KEY)")
    brand = list(zip(set(brandName)))

    cur.executemany("INSERT INTO brand VALUES(?)", brand)

    # Create table productType
    productType = list(zip(type, offerType, departmentName))
    cur.execute(
        "create table if not exists productType(type VARCHAR(50), offerType VARCHAR(50), departmentName VARCHAR(100))"
    )
    cur.executemany("INSERT INTO productType VALUES(?,?,?)", productType)

    # Create table store

    store = list(zip(storeID, storeAddress, storePhone, storeHour))
    cur.execute(
        "create table if not exists store(storeID INT PRIMARY KEY, storeAddress VARCHAR(200), storePhone VARCHAR(20), storeHour VARCHAR(50))"
    )
    cur.executemany("INSERT INTO store VALUES(?,?,?,?)", store)

    # Create table vendor
    vendor = list(zip(sellerName, sellerReviewCount))
    cur.execute(
        "create table if not exists vendor(sellerName VARCHAR(100) PRIMARY KEY, sellerReviewCount INT)"
    )
    cur.executemany("INSERT INTO vendor VALUES(?,?)", vendor)

    # Create table customer
    customer = list(zip(customerID, customerName, paidMemberShip))
    cur.execute(
        "create table if not exists customer(customerID INT PRIMARY KEY, customerName VARCHAR(20), paidMemberShip VARCHAR(10))"
    )
    cur.executemany("INSERT INTO customer VALUES(?,?,?)", customer)

    # Create table purchase
    purchase = [
        [i, random.choice(usItemID), random.randint(3, 100)] for i in customerID
    ]
    cur.execute(
        "create table if not exists purchase(customerID INT PRIMARY KEY, usItemID INT, quantity INT, FOREIGN KEY(customerID) REFERENCES customer(customerID), FOREIGN KEY(usItemID) REFERENCES product(usItemID))"
    )
    cur.executemany("INSERT INTO purchase VALUES(?,?,?)", purchase)

    # Create table has_type
    has_type = list(zip(usItemID, type))
    cur.execute(
        "create table if not exists has_type(usItemID INT PRIMARY KEY, type VARCHAR(50),FOREIGN KEY(usItemID) REFERENCES product(usItemID), FOREIGN KEY(type) REFERENCES productType(type))"
    )
    cur.executemany("INSERT INTO has_type VALUES(?,?)", has_type)

    # Create table is_sold_S_P
    is_sold_S_P = list(zip(usItemID, brandName))
    cur.execute(
        "create table if not exists is_sold_S_P(usItemID INT PRIMARY KEY, brandName VARCHAR(300),FOREIGN KEY(usItemID) REFERENCES product(usItemID), FOREIGN KEY(brandName) REFERENCES brand(brandName))"
    )
    cur.executemany("INSERT INTO is_sold_S_P VALUES(?,?)", is_sold_S_P)

    # Create table is_visited
    is_visited = [[i, random.choice(storeID)] for i in customerID]
    cur.execute(
        "create table if not exists is_visited(customerID INT PRIMARY KEY, storeID INT, FOREIGN KEY(customerID) REFERENCES customer(customerID), FOREIGN KEY(storeID) REFERENCES store(storeID))"
    )
    cur.executemany("INSERT INTO is_visited VALUES(?,?)", is_visited)

    # Create table is_paid
    storeID = [2584, 3067, 3071, 1373, 2154, 3074, 3070, 1184, 3621, 2360]
    is_paid = [[i, random.choice(sellerName)] for i in storeID]
    cur.execute(
        "create table if not exists is_paid(storeID INT PRIMARY KEY, sellerName VARCHAR(100), FOREIGN KEY(sellerName) REFERENCES vendor(sellerName), FOREIGN KEY(storeID) REFERENCES store(storeID))"
    )
    cur.executemany("INSERT INTO is_paid VALUES(?,?)", is_paid)

    # Create table is_sold_V_P
    is_sold_V_B = [[i, random.choice(brandName)] for i in sellerName]
    cur.execute(
        "create table if not exists is_sold_V_B(sellerName VARCHAR(100) PRIMARY KEY, brandName VARCHAR(100), FOREIGN KEY(sellerName) REFERENCES vendor(sellerName), FOREIGN KEY(brandName) REFERENCES brand(brandName))"
    )
    cur.executemany("INSERT INTO is_sold_V_B VALUES(?,?)", is_sold_V_B)

    # Create table is_sold_S_P
    is_sold_S_P = [[i, random.choice(storeID), random.randint(5, 50)] for i in usItemID]
    cur.execute(
        "create table if not exists is_sold_S_P(usItemID INT PRIMARY KEY, storeID INT, availability INT,FOREIGN KEY(usItemID) REFERENCES product(usItemID), FOREIGN KEY(storeID) REFERENCES store(storeID))"
    )
    cur.executemany("INSERT INTO is_sold_S_P VALUES(?,?,?)", is_sold_S_P)
    con.commit()
    con.close()


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    """[summary]

    Args:
        path ([type]): [description]

    Returns:
        [type]: [description]
    """
    return flask.redirect(flask.url_for("bp.index"))


@app.route("/execute_command", methods=["POST"])
def execute_command():
    command = flask.request.json.get("command")

    con = sqlite3.connect("walmart.db")
    cur = con.cursor()
    if command[:6].lower() != "select":
        cur.execute(command)
        con.commit()
        con.close()
    else:
        result = []
        header = list(zip([header[0] for header in cur.execute(command).description]))
        try:
            result = cur.execute(command).fetchall()
            result.insert(0, tuple(header))
            return flask.jsonify({"result": result, "error": None})
        except:
            e = sys.exc_info()[0]
            result.insert(0, tuple(header))
            return flask.jsonify({"result": result, "error": e})


""" 
category = [
    4044,
    4171,
    1115193,
    1005862,
    976759,
    1229749,
    3944,
    5438,
    5428,
    4125,
    5427,
    5440,
]
usItemID = [
    407378056,
    55500001,
    596140033,
    363845482,
    515619521,
    475271390,
    109930925,
    675140113,
    42424706,
    795925903,
    14898365,
    34720573,
    2304198,
    908197301,
    16940601,
    38773089,
    35520771,
    650545386,
    17808715,
    306203294,
    706203065,
    834343104,
    383634749,
    45825256,
    698410145,
    489882644,
    14940220,
]


def get_product_json(id):
    url = "https://walmart.p.rapidapi.com/products/v3/get-details"

    querystring = {"usItemId": f"{id}"}

    headers = {
        "x-rapidapi-host": "walmart.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RapidAPI"),
    }
    # test
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    usItemID = response["data"]["product"]["usItemId"]
    upc = response["data"]["product"]["upc"]
    # storeID = response["data"]["product"]["location"]["storeIds"][0]
    price = response["data"]["product"]["priceInfo"]["currentPrice"]["price"]
    productName = response["data"]["product"]["name"]
    brand = response["data"]["product"]["brand"]
    type = response["data"]["product"]["type"]
    offerType = response["data"]["product"]["offerType"]
    departmentName = response["data"]["product"]["departmentName"]
    return (usItemID, upc, price, productName, brand, type, offerType, departmentName)


productData = {}
productData["product"] = []
storeID = [2584, 3067, 3071, 1373, 2154, 3074, 3070, 1184, 3621, 2360]

productData = {}
productData["product"] = []
 
for i in usItemID:
    (
        itemID,
        upc,
        price,
        productName,
        brand,
        type,
        offerType,
        departmentName,
    ) = get_product_json(i)
    productData["product"].append(
        {
            "usItemID": itemID,
            "upc": upc,
            "storeID": random.choice(storeID),
            "price": price,
            "productName": productName,
            "brand": brand,
            "type": type,
            "offerType": offerType,
            "departmentName": departmentName,
        }
    )


def get_store_info(id):
    url = "https://walmart.p.rapidapi.com/stores/list-preferred"

    querystring = {"postalCode": "30093", "preferredStoreId": f"{id}"}

    headers = {
        "x-rapidapi-host": "walmart.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RapidAPI"),
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    storeID = id
    address = response["preferredStore"]["address"]
    storeAddress = (
        address["address1"]
        + ", "
        + address["city"]
        + ", "
        + address["state"]
        + ", "
        + address["postalCode"]
    )
    storePhone = response["preferredStore"]["phone"]
    storeHour = "Mon-Sun: 6 am to 11 pm"
    return (storeID, storeAddress, storePhone, storeHour)


productData["Store"] = []

for i in storeID:
    storeID, storeAddress, storePhone, storeHour = get_store_info(i)
    productData["Store"].append(
        {
            "storeID": storeID,
            "storeAddress": storeAddress,
            "storePhone": storePhone,
            "storeHour": storeHour,
        }
    )

with open("product_table.json", "w") as fp:
    json.dump(productData, fp)
"""
""" 
# VENDOR
vendor = []
with open("vendorlist.csv", "r") as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
        # Iterate over each row after the header in the csv
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            vendor.append({"sellerName": row[0], "sellerReviewCount": row[1]})
print(vendor)
"""

"""customer 
customer = []
with open("customerlist.csv", "r") as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
        # Iterate over each row after the header in the csv
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            customer.append(
                {"customerID": row[0], "customerName": row[1], "paidMemberShip": row[2]}
            )
print(customer)

"""


@app.route("/")
def main():
    return flask.redirect(flask.url_for("bp.index"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8081)),
    )
