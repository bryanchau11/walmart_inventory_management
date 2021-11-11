import flask
from flask_login.utils import login_required
import os
import json
import sqlite3
import requests
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())
app = flask.Flask(__name__, static_folder="./build/static")
# This tells our Flask app to look at the results of `npm build` instead of the
# actual files in /templates when we're looking for the index page file. This allows
# us to load React code into a webpage. Look up create-react-app for more reading on
# why this is necessary.
bp = flask.Blueprint("bp", __name__, template_folder="./build")


@bp.route("/index")
def index():
    # TODO: insert the data fetched by your app main page here as a JSON
    DATA = {"list": test()}
    data = json.dumps(DATA)
    return flask.render_template(
        "index.html",
        data=data,
    )


app.register_blueprint(bp)


def test():
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
    data = json.load(f)
    for i in data["product"]:
        usItemID.append(i["usItemID"])
        upc.append(i["upc"])
        storeID.append(i["storeID"])
        price.append(i["price"])
        productName.append(i["productName"])
    product = list(zip(usItemID, upc, storeID, price, productName))
    cur.execute(
        "create table if not exists product(usItemID INT PRIMARY KEY, UPC INT, storeID INT, price VARCHAR(20), productName VARCHAR(300))"
    )
    cur.executemany("INSERT INTO product VALUES(?,?,?,?,?)", product)
    con.commit()
    con.close()


test()

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
    45825256,
    109930925,
    675140113,
    42424706,
    795925903,
    14898365,
    34720573,
    38773089,
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
    storeID = response["data"]["product"]["location"]["storeIds"][0]
    price = response["data"]["product"]["priceInfo"]["currentPrice"]["priceString"]
    productName = response["data"]["product"]["name"]
    # brand = response["data"]["product"]["brand"]
    return (usItemID, upc, storeID, price, productName)


""" 
productData = {}
productData["product"] = []

for i in usItemID:
    itemID, upc, storeID, price, productName = get_product_json(i)
    productData["product"].append(
        {
            "usItemID": itemID,
            "upc": upc,
            "storeID": storeID,
            "price": price,
            "productName": productName,
        }
    )
with open("product_table.json", "w") as fp:
    json.dump(productData, fp)
"""


@app.route("/")
def main():
    return flask.redirect(flask.url_for("bp.index"))


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
