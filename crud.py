from sqlalchemy.orm import Session
from fastapi import Response
import models, schemas

def create_produto(db : Session, produto : schemas.ProdutoCreate):
    db_produto = models.Produto(titulo = produto.titulo, descricao = produto.descricao, preco = produto.preco)
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def get_produto(db : Session, idProduto : int):
    return db.query(models.Produto).filter(models.Produto.idProduto == idProduto).first()

def get_produtos(db : Session, skip : int = 0, limit : int = 10):
    return db.query(models.Produto).offset(skip).limit(limit).all()

def update_produto(db : Session, idProduto : int, update : schemas.ProdutoCreate):
    update_data = update.dict()
    update_data["idProduto"] = idProduto

    db.query(models.Produto).filter(models.Produto.idProduto == idProduto).update(update_data)
    db.commit()
    return update_data

def delete_produto(db : Session, idProduto : int):
    db_produto = get_produto(db, idProduto)
    if db_produto:
        db.delete(db_produto)
        db.commit()
        return Response(status_code=200, content = "Successfully deleted", media_type="application/json")

#########################################################################################################

def create_carrinho(db : Session):
    db_carrinho = models.Carrinho()
    db.add(db_carrinho)
    db.commit()
    db.refresh(db_carrinho)
    return db_carrinho

def get_carrinho(db : Session, idCarrinho : int, skip : int = 0, limit : int = 10):
    return db.query(models.ProdutoCarrinho).filter(models.ProdutoCarrinho.idCarrinho == idCarrinho).offset(skip).limit(limit).all()

def delete_carrinho(db : Session, idCarrinho : int):
    db_carrinho = db.query(models.Carrinho).filter(models.Carrinho.idCarrinho == idCarrinho).first()
    if db_carrinho:
        db.delete(db_carrinho)
        db.commit()
        return Response(status_code=200, content = "Successfully deleted", media_type="application/json")

#########################################################################################################

def insert_produto(db : Session, idProduto : int, idCarrinho : int, insert : schemas.ProdutoCarrinhoCreate):
    db_ProdutoCarrinho = models.ProdutoCarrinho(idProduto = idProduto, idCarrinho = idCarrinho, quantidade = insert.quantidade)
    db.add(db_ProdutoCarrinho)
    db.commit()
    db.refresh(db_ProdutoCarrinho)
    return db_ProdutoCarrinho

def get_produto_carrinho_relations(db : Session, skip : int = 0, limit : int = 10):
    return db.query(models.ProdutoCarrinho).offset(skip).limit(limit).all()

def update_quantidade(db : Session, idCarrinho : int, idProduto : int, update : schemas.ProdutoCarrinhoCreate):
    update_data = update.dict()
    update_data["idCarrinho"] = idCarrinho
    update_data["idProduto"] = idProduto

    db.query(models.ProdutoCarrinho).filter(models.ProdutoCarrinho.idCarrinho == idCarrinho and  models.ProdutoCarrinho.idProduto == idProduto).update(update_data)
    db.commit()
    return update_data

def remove_produto_from_carrinho(db : Session, idProduto : int, idCarrinho : int):
    db_produto = db.query(models.ProdutoCarrinho).filter(models.ProdutoCarrinho.idProduto == idProduto and models.ProdutoCarrinho.idCarrinho == idCarrinho).first()
    if db_produto:
        db.delete(db_produto)
        db.commit()
        return Response(status_code=200, content = "Successfully deleted", media_type="application/json")
