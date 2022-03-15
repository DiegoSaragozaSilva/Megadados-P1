# GET 		/products/
# GET 		/products/{product_id}/
# POST 		/products/
# PATCH 	/products/{product_id}/
# DELETE 	/products/{product_id}/

from fastapi import FastAPI, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional
import json

DB = None
with open("db.json", "r", encoding = "utf-8") as file:
	DB = json.load(file)
	
app = FastAPI()

class Product(BaseModel):
	id : Optional[int] = Field(None, example = 9)
	name : Optional[str] = Field(None, example = "Dragon Ball")
	description : Optional[str] = Field(None, example = "Dragon Ball é um mangá japonês criado por Akira Toriyama e publicado na revista Weekly Shounen Jump, a partir de 1986.")
	price : Optional[float] = Field(None, example = 9.90)
	

@app.get("/products/")
async def get_products():
	return DB["Products"]
	
@app.get("/products/{product_id}/")
async def get_products(product_id : int):
	for product in DB["Products"]:
		if product["id"] == product_id:
			return product
	raise HTTPException(status_code = 404, detail = "Product not found")
	
@app.post("/products/")
async def post_products(product : Product):
	max_id = 0
	for _product in DB["Products"]:
		if _product["id"] > max_id:
			max_id = _product["id"]
			
	product.id = max_id + 1
	DB["Products"].append(jsonable_encoder(product))
	
	with open("db.json", "w", encoding = "utf-8") as file:
		json.dump(DB, file)
		
	return product
		
@app.patch("/products/{product_id}/")
async def put_products(product_id : int, product : Product):
	i = 0
	for _product in DB["Products"]:
		if _product["id"] == product_id:
		
			stored_product = Product(**_product)
			update_data = product.dict(exclude_unset = True)
			update_product = stored_product.copy(update = update_data)
			DB["Products"][i] = jsonable_encoder(update_product) 
		
			with open("db.json", "w", encoding = "utf-8") as file:
				json.dump(DB, file)
		
			return DB["Products"][i]
		i += 1
		
	raise HTTPException(status_code = 404, detail = "Product not found")
