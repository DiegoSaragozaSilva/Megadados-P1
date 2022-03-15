# GET 		/products/
# GET 		/products/{product_id}/
# POST 		/products/
# PUT 		/products/{product_id}/
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
	id : int = Field(..., example = 9)
	name : str = Field(..., example = "Dragon Ball")
	description : Optional[str] = Field(..., example = "Dragon Ball é um mangá japonês criado por Akira Toriyama e publicado na revista Weekly Shounen Jump, a partir de 1986.")
	price : float = Field(..., example = 9.90)
	

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
