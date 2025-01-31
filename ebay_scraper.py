import requests
import xmltodict
import json
from datetime import datetime

# eBay API Details
EBAY_API_URL = "https://open.api.ebay.com/shopping"
HEADERS = {
    "X-EBAY-API-IAF-TOKEN": "v^1.1#i^1#p^1#r^0#f^0#I^3#t^H4sIAAAAAAAAAOVYa2wUVRTe7e7WNlAwUQuWSpZBpYAze2dmd7s7dBeWlj6SPpZuW6Go6zzutAM7D+betd0awtoYjImP+EOIGEMJD0mMoiSExBiNJBKNhjYq8RENGhKDiPhDEROfM7tt2VbCq5vYxP2zmXPPPff7vnPOvXcGZEvLV+xo3nGpwnlLyUgWZEucTnoOKC/1rJznKqnyOECBg3Mke3fWPew6W4d4NWVwnRAZuoagd1BNaYjLGSNE2tQ4nUcK4jRehYjDIpeItbVyDAU4w9SxLuopwtvSECHC4VCABaGQnxF4VgbAsmoTMbv0CBEK02GJDgkCD/wAitAaRygNWzSEeQ1HCAYwARLQJEt30X4uwHA0TdFh0Et4e6CJFF2zXChARHNwudxcswDr1aHyCEETW0GIaEusMdERa2lY195V5yuIFR3XIYF5nEZTn+p1CXp7+FQaXn0ZlPPmEmlRhAgRvmh+halBudgEmJuAn5NaDDKMFGRYsbZW8gcEtihSNuqmyuOr47AtikTKOVcOaljBmWspaqkhbIYiHn9qt0K0NHjtv/VpPqXICjQjxLq1sY2xeJyINvOqMtRJqoqmGCIi450NJAgGmRAUgrLFBwphOcyMr5IPNa7xtGXqdU1SbMWQt13Ha6EFGU4Xxl8gjOXUoXWYMRnbcAr9ghMChtheO6P5FKZxv2YnFaqWCt7c47Xln5yNsakIaQwnI0wfyOkTIXjDUCRi+mCuEMdrZxBFiH6MDc7nGxgYoAZYSjf7fAwAtG9DW2tC7IcqT+R97V63/JVrTyCVHBW7Ry1/DmcMC8ugVagWAK2PiAZoP6AnsjAVVnS69V+GAs6+qe1QrPaQQ6LkBwIUWRiUWCgXoz2i4xXqs3FAgc+QKm9ugdhI8SIkRavO0io0FYljAzLDhmRISsGwTPrDskwKASlI0jKEAEJBEMOh/02XXG+dJ6BoQlysQi9SkQ8BOd4YZjZvDXWnNzavpTPagNLEmonaRB/amg42dAcYzDCi1r8ucr2tcEXy9SnFUqbLWr94Ati9XgwRmnWEoTQjeglRN2BcTyliZnYlmDWlOG/iTAKmUpZhRiRjhtFStI26OPRuZI+4OdJFPZ3+i5PpiqyQXa+zi5U9H1kBeEOh7LOHEnXVp/PWpcM22b2ezKGeEW/FurDOKtYWyTxbRcrfNKkcZQo9IlImRHratC7ZVId99+rSt0DNOsywqadS0OyhZ9zMqprGvJCCs62ri1DgCj/LTlq6lg2xbIBmZ5Y2MXeOJmfbllTUfdi96gZu076pL/ZRR+5HDzuPg2Hn2yVOJ6gD99BLwZJSV7fbNbcKKRhSCi9TSOnTrPdVE1JbYMbgFbPkNsfovFbpsebWi1khfez+X1aHHBUF3xVGHgQLJ78slLvoOQWfGUD15REPPX9BBRMAVqppf4Ch6V6w9PKom6503142tnk0srpzz+PtGU9Z086n7vxy9xlQMenkdHoc7mGng9q65MDJphOxs18n6pLB6ue77zp/qNL33mtH33eNlYmfVZKj9T+veadMcq8/8e6TZ07XXPx+wQKmetF9F/zo4Y/ply/sat/11/GTiweFO7qXw7G9hw+8rs7tXPzCA97yyu54+NK++DmjpmbZVwv/fPqTfXuPvepwbQMjK3/3JLPu37btOGS+UvXoysH9+101m7j4r6Vnf5j3xvLnPtoVP7zqm+SRpt1VP7ZvOrzkVM+9xufODd++dN6z7PSpsHr0oQvPMuXz3UdGdt5a1bXz0PajQy6yFR/sHYu9GE3+wdJk9Qejq/8mvlvxU8X2T2vbkns9TwxFiGfefOvgnic3bG9s3i0MfLimbd8i8tzxL/K5/AdWljhc8REAAA==",  # Replace with your eBay token
    "X-EBAY-API-SITE-ID": "0",
    "X-EBAY-API-CALL-NAME": "FindProducts",
    "X-EBAY-API-VERSION": "963",
    "X-EBAY-API-REQUEST-ENCODING": "xml",
    "Content-Type": "text/xml"
}

# XML Payload to fetch 100 Mini PC listings
XML_PAYLOAD = """<?xml version="1.0" encoding="utf-8"?>
<FindProductsRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <QueryKeywords>mini pc</QueryKeywords>
    <MaxEntries>100</MaxEntries>  
    <AvailableItemsOnly>true</AvailableItemsOnly>
</FindProductsRequest>
"""

# 🟢 Make the API Request
response = requests.post(EBAY_API_URL, headers=HEADERS, data=XML_PAYLOAD)

if response.status_code == 200:
    # Convert XML Response to Dictionary
    data_dict = xmltodict.parse(response.text)

    # Extract Relevant Data
    products = data_dict.get("FindProductsResponse", {}).get("Product", [])

    # Convert to JSON Format
    json_data = []
    for product in products:
        product_data = {
            "title": product.get("Title", "N/A"),
            "product_id": product.get("ProductID", {}).get("#text", "N/A"),
            "stock_photo_url": product.get("StockPhotoURL", ""),
            "details_url": product.get("DetailsURL", ""),
            "specifications": {
                nv["Name"]: nv["Value"] if isinstance(nv["Value"], list) else [nv["Value"]]
                for nv in product.get("ItemSpecifics", {}).get("NameValueList", [])
            }
        }

        json_data.append(product_data)

    # Save JSON Data to a File
    with open("data/mini_pcs.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print("✅ eBay Mini PCs data saved to 'data/mini_pcs.json'")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
