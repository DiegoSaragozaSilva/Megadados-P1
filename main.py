from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import json

#################################################
#             LENDO BANCO DE DADOS              #
#################################################

with open("db.json", "r", encoding = "utf-8") as file:
    db = json.load(file)

app = FastAPI()

#################################################
#             SCHEMAS BANCO DE DADOS            #
#################################################

class Product(BaseModel):
    name: Optional[str] = Field(None, example = "Dragon Ball")
    description: Optional[str] = Field(None, example = "Dragon Ball é um mangá japonês criado por Akira Toriyama e publicado na revista Weekly Shounen Jump, a partir de 1986.")
    price: Optional[float] = Field(None, example = 9.90)

class ShopCart(BaseModel):
    owner_id: Optional[int] = Field(None, example=1)

class ShopCart_Product(BaseModel):
    cart_id: Optional[int] = Field(..., example=3)
    product_id: Optional[int] = Field(..., example=9)
    quantity: int = Field(..., example=1)

#################################################
#                CRUD PRODUTOS                  #
#################################################

@app.get("/products/", tags=["products"])
async def get_products():
    return db["Products"]
	
@app.get("/products/{product_id}/", tags=["products"])
async def get_products(product_id : int):
    for product in db["Products"]:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code = 404, detail = "Product not found")
	
@app.post("/products/", tags=["products"])
async def post_products(product : Product):
    max_id = 0
    for _product in db["Products"]:
        if _product["id"] > max_id:
            max_id = _product["id"]
                
    product_data = product.dict()
    product_data["id"] = max_id + 1
    db["Products"].append(jsonable_encoder(product_data))
    
    with open("db.json", "w", encoding = "utf-8") as file:
        json.dump(db, file)
            
    return product
		
@app.patch("/products/{product_id}/", tags=["products"])
async def put_products(product_id : int, product : Product):
    i = 0
    for _product in db["Products"]:
        if _product["id"] == product_id:
    
            stored_product = Product(**_product)
            update_data = product.dict(exclude_unset = True)
            update_product = stored_product.copy(update = update_data)
            db["Products"][i] = jsonable_encoder(update_product) 
    
            with open("db.json", "w", encoding = "utf-8") as file:
                json.dump(db, file)
    
            return db["Products"][i]
        i += 1
            
    raise HTTPException(status_code = 404, detail = "Product not found")

@app.delete("/products/{product_id}/", tags=["products"])
async def delete_products(product_id : int):
    for _product in db["Products"]:
        if _product["id"] == product_id:
            db["Products"].remove(_product)

            for relation in db["ShopCarts_Products"]:
                if relation["product_id"] == product_id:
                    db["ShopCarts_Products"].remove(relation)

                    still_has_cart_id = False
                    for _relation in db["ShopCarts_Products"]:
                        if _relation["cart_id"] == relation["cart_id"]:
                            still_has_cart_id = True
                            break

                    if not still_has_cart_id:
                        for cart in db["ShopCarts"]:
                            if cart["id"] == relation["cart_id"]:
                                db["ShopCarts"].remove(cart)
            
            with open("db.json", "w", encoding = "utf-8") as file:
                json.dump(db, file)
            
            return JSONResponse(status_code = 200, content={ "detail": "Product deleted" })
                
    raise HTTPException(status_code = 404, detail = "Product not found")

#################################################
#                CRUD CARRINHO                  #
#################################################

@app.get("/carts/", tags=["carts"])
async def get_carts():
    return db["ShopCarts"]

@app.get("/carts/{cart_id}", tags=["carts"])
async def get_cart(cart_id : int):
    for cart in db["ShopCarts"]:
        if cart["id"] == cart_id:
            return cart

    raise HTTPException(status_code = 404, detail = "User doesn't exist or User has no carts")

@app.delete("/carts/{cart_id}", tags=["carts"])
async def delete_cart(cart_id : int):
    for cart in db["ShopCarts"]:
        if cart["id"] == cart_id:
            db["ShopCarts"].remove(cart)

            for shopcart_product in db["ShopCarts_Products"]:
                if shopcart_product["cart_id"] == cart_id:
                    db["ShopCarts_Products"].remove(shopcart_product)

            with open("db.json", "w", encoding = "utf-8") as file:
                json.dump(db, file)
            
            return JSONResponse(status_code = 200, content={ "detail": "Cart deleted" })

    raise HTTPException(status_code = 404, detail = "Cart not found")
