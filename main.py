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
    id: Optional[int] = Field(None, example="9")
    name: Optional[str] = Field(None, example = "Dragon Ball")
    description: Optional[str] = Field(None, example = "Dragon Ball é um mangá japonês criado por Akira Toriyama e publicado na revista Weekly Shounen Jump, a partir de 1986.")
    price: Optional[float] = Field(None, example = 9.90)

class ShopCart(BaseModel):
    id: Optional[int] = Field(..., example="9")

class ShopCart_Product(BaseModel):
    cart_id: Optional[int] = Field(..., example=3)
    product_id: Optional[int] = Field(..., example=9)
    quantity: int = Field(..., example=1)

#################################################
#                CRUD PRODUTOS                  #
#################################################

@app.get("/products/{product_id}/", tags=["products"])
async def get_product(product_id : int):
    for product in db["Products"]:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code = 404, detail = "Product not found")
	
@app.post("/products/", tags=["products"])
async def create_product(product : Product):
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
async def update_product(product_id : int, product : Product):
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
async def delete_product(product_id : int):
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
#                  CARRINHO                     #
#################################################

@app.get("/carts/{cart_id}/", tags=["carts"])
async def get_cart(cart_id : int):
    products_ids = list()
    for cart_product in db["ShopCarts_Products"]:
        if cart_product["cart_id"] == cart_id:
            products_ids.append(cart_product["product_id"])

    if(len(products_ids) > 0):
        return [product for product in db["Products"] if product["id"] in products_ids]
    else:
        raise HTTPException(status_code = 404, detail = "User doesn't exist or User has no carts")

@app.post("/carts/", tags=["carts"])
async def create_cart(cart_id : int):
    cart = {
        "id": cart_id
    }
    shopcart = ShopCart(**cart)
    db["ShopCarts"].append(jsonable_encoder(shopcart))
    
    with open("db.json", "w", encoding = "utf-8") as file:
        json.dump(db, file)
            
    return shopcart

@app.delete("/carts/{cart_id}/", tags=["carts"])
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

#################################################
#             TABELA RELACIONAMENTO             #
#################################################

@app.post("/carts/{cart_id}/", tags=["carts"])
async def add_product_on_cart(cart_id : int, product_id : int, quantity : int):
    cart_product = {
        "cart_id": cart_id,
        "product_id": product_id,
        "quantity": quantity
    }
    shopcart_product = ShopCart_Product(**cart_product)

    db["ShopCarts_Products"].append(jsonable_encoder(shopcart_product))
    
    with open("db.json", "w", encoding = "utf-8") as file:
        json.dump(db, file)
            
    return shopcart_product

@app.patch("/carts/{cart_id}/{product_id}/", tags=["carts"])
async def edit_item_quantity(cart_id : int, product_id : int, new_quantity : int):
    i = 0
    for cart_product in db["ShopCarts_Products"]:
        if(cart_product["cart_id"] == cart_id and cart_product["product_id"] == product_id):
    
            stored_cart_product = Product(**cart_product)
            update_data = {
                "quantity": new_quantity
            }
            update_cart_product = stored_cart_product.copy(update = update_data)
            db["ShopCarts_Products"][i] = jsonable_encoder(update_cart_product) 
    
            with open("db.json", "w", encoding = "utf-8") as file:
                json.dump(db, file)
    
            return db["ShopCarts_Products"][i]
        i += 1
            
    raise HTTPException(status_code = 404, detail = "Product not found")

