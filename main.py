from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=schemas.Produto, tags=["Product"])
async def create_product(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.create_produto(db = db, produto = produto)

@app.get("/products/{product_id}/", response_model=schemas.Produto, tags=["Product"])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_produto(db = db, idProduto = product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/products/", response_model=List[schemas.Produto], tags=["Product"])
async def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_products = crud.get_produtos(db = db, skip = skip, limit = limit)
    return db_products

@app.patch("/products/{product_id}/", response_model=schemas.Produto, tags=["Product"])
async def update_product(product_id: int, update: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    updated_product = crud.update_produto(db = db, idProduto = product_id, update = update)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/products/{product_id}/", tags=["Product"])
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted_product = crud.delete_produto(db = db, idProduto = product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product

@app.post("/shopcart/", response_model=schemas.Carrinho, tags=["ShopCart"])
async def create_shopcart(db: Session = Depends(get_db)):
    return crud.create_carrinho(db = db)

@app.get("/shopcart/{shopcart_id}/", response_model=List[schemas.ProdutoCarrinho], tags=["ShopCart"])
async def get_shopcart(shopcart_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    db_products = crud.get_carrinho(db = db, idCarrinho = shopcart_id, skip = skip, limit = limit)
    if not db_products:
        raise HTTPException(status_code=404, detail="ShopCart not found")
    return db_products

@app.delete("/shopcart/{shopcart_id}/", tags=["ShopCart"])
async def delete_shopcart(shopcart_id: int, db: Session = Depends(get_db)):
    deleted_shopcart = crud.delete_carrinho(db = db, idCarrinho = shopcart_id)
    if deleted_shopcart is None:
        raise   HTTPException(status_code=404, detail="ShopCart not found")
    return deleted_shopcart

@app.post("/shopcart/{shopcart_id}/product/{product_id}", response_model=schemas.ProdutoCarrinho, tags=["ShopCart"])
async def insert_product(shopcart_id: int, product_id: int, quantidade: schemas.ProdutoCarrinhoCreate, db: Session = Depends(get_db)):
    return crud.insert_produto(db = db, idCarrinho = shopcart_id, idProduto = product_id, insert = quantidade)

@app.get("/shopcart/", response_model=List[schemas.ProdutoCarrinho], tags=["ShopCart"])
async def get_shopcarts(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_produto_carrinho_relations(db = db,  skip = skip, limit = limit)

@app.patch("/shopcart/{shopcart_id}/product/{product_id}", response_model=schemas.ProdutoCarrinho, tags=["ShopCart"])
async def update_quantity(shopcart_id: int, product_id: int, update: schemas.ProdutoCarrinhoCreate, db: Session = Depends(get_db)):
    updated_quantity = crud.update_quantidade(db = db, idProduto = product_id, idCarrinho = shopcart_id, update = update)
    if updated_quantity is None:
        raise HTTPException(status_code=404, detail="Product or Shopcart not found")
    return updated_quantity

@app.delete("/shopcart/{shopcart_id}/product/{product_id}", tags=["ShopCart"])
async def remove_product(shopcart_id: int, product_id: int, db: Session = Depends(get_db)):
    deleted_product = crud.remove_produto_from_carrinho(db = db, idCarrinho = shopcart_id, idProduto = product_id)
    if deleted_product is None:
        raise   HTTPException(status_code=404, detail="ShopCart or Product not found")
    return deleted_product
