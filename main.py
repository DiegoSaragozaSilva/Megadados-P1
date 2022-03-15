# GET 		/products/
# GET 		/products/{product_id}/
# POST 		/products/
# PUT 		/products/{product_id}/
# DELETE 	/products/{product_id}/

from fastapi import FastAPI, HTTPException
import json

DB = None
with open("db.json", "r") as file:
	DB = json.load(file)
	
app = FastAPI()

@app.get("/products/")
async def get_products():
	return DB["Products"]
	
@app.get("/products/{product_id}/")
async def get_products(product_id : int):
	for product in DB["Products"]:
		if product["id"] == product_id:
			return product
	raise HTTPException(status_code = 404, detail = "Product not found")
