# GET 		/products/
# GET 		/products/{product_id}/
# POST 		/products/
# PUT 		/products/{product_id}/
# DELETE 	/products/{product_id}/

from fastapi import FastAPI
import json

DB = None
with open("db.json", "r") as file:
	DB = json.load(file)
	
app = FastAPI()

@app.get("/products/")
async def get_products():
	return DB["Products"]
