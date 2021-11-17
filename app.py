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

load_dotenv(find_dotenv())
app = flask.Flask(__name__, static_folder="./build/static")
# This tells our Flask app to look at the results of `npm build` instead of the
# actual files in /templates when we're looking for the index page file. This allows
# us to load React code into a webpage. Look up create-react-app for more reading on
# why this is necessary.
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
    brand_list = cur.execute("select * from brand").fetchall()
    productType_list = cur.execute("select * from productType").fetchall()
    store_list = cur.execute("select * from store").fetchall()

    DATA = {
        "product": product_list,
        "productType": productType_list,
        "brand": brand_list,
        "store": store_list,
    }
    data = json.dumps(DATA)
    return flask.render_template(
        "index.html",
        data=data,
    )


app.register_blueprint(bp)

###
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

    # Create table product

    print(json.dumps(data["product"], indent=4, sort_keys=True))

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
    con.commit()
    con.close()


"""
con = sqlite3.connect("walmart.db")
cur = con.cursor()
product_list_header = list(
    [header[0] for header in cur.execute("select * from product").description]
)
product_list = cur.execute("select * from product").fetchall()
product_list.insert(0, tuple(product_list_header))
print(product_list)
"""


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


@app.route("/")
def main():
    return flask.redirect(flask.url_for("bp.index"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8081)),
    )
