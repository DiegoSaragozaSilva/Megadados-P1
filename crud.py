from sqlalchemy.orm import Session
from . import models, schemas

def createProduto(db : Session, produto : schemas.ProdutoCreate):
    db_produto = models.Produto(titulo = produto.titulo, descricao = produto.descricao, preco = produto.preco)
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def getProduto(db : Session, idProduto : int):
    return db.query(models.Produto).filter(models.Produto.idProduto == idProduto).first()

def getProdutos(db : Session, skip : int = 0, limit : int = 10):
    return db.query(models.Produto).offset(skip).limit(limit).all()

def updateProduto(db : Session, idProduto : int, produto : dict):
    db_produto = db.query(models.Produto).filter(models.Produto.idProduto == idProduto)
    db_produto.update(produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def deleteProduto(db : Session, idProduto : int):
    db_produto = db.query(models.Produto).filter(models.Produto.idProduto == idProduto)
    db_produto.delete()
    db.commit()
    return db_produto

#########################################################################################################

def createCarrinho(db : Session, carrinho : schemas.CarrinhoCreate):
    db_carrinho = models.Carrinho()
    db.add(db_carrinho)
    db.commit()
    db.refresh(db_carrinho)
    return db_carrinho

def getCarrinho(db : Session, idCarrinho : int):
    return db.query(models.Carrinho).filter(models.Carrinho.idCarrinho == idCarrinho).first()

def getCarrinhos(db : Session, skip : int = 0, limit : int = 10):
    return db.query(models.Carrinho).offset(skip).limit(limit).all()

def updateCarrinho(db : Session, idProduto : int, carrinho : dict):
    db_carrinho = db.query(models.Carrinho).filter(models.Carrinho.idCarrinho == idCarrinho)
    db_carrinho.update(carrinho)
    db.commit()
    db.refresh(db_carrinho)
    return db_carrinho

def deleteCarrinho(db : Session, idCarrinho : int):
    db_carrinho = db.query(models.Carrinho).filter(models.Carrinho.idCarrinho == idCarrinho)
    db_carrinho.delete()
    db.commit()
    return db_carrinho

#########################################################################################################

def createProdutoCarrinho(db : Session, idProduto : int, idCarrinho : int, quantidade : int):
    db_ProdutoCarrinho = models.ProdutoCarrinho(idProduto = idProduto, idCarrinho = idCarrinho, quantitade = quantidade)
    db.add(db_ProdutoCarrinho)
    db.commit()
    db.refresh(db_ProdutoCarrinho)
    return db_ProdutoCarrinho

def getProdutosFromCarrinho(db : Session, idCarrinho : int, skip : int = 0, limit : int = 10):
    return db.query(models.ProdutoCarrinho).filter(models.ProdutoCarrinho.idCarrinho == idCarrinho).offset(skip).limit(limit).all()

def getProdutoCarrinhos(db : Session, skip : int = 0, limit : int = 10):
    return db.query(models.ProdutoCarrinho).offset(skip).limit(limit).all()

def updateProdutoCarrinho(db : Session, idProduto : int, idCarrinho : int, ProdutoCarrinho : dict):
    db_ProdutoCarrinho = db.query(models.ProdutoCarrinho).filter(models.ProdutoCarrinho.idProduto == idProduto and models.ProdutoCarrinho.idCarrinho == idCarrinho)
    db_ProdutoCarrinho.update(ProdutoCarrinho)
    db.commit()
    db.refresh(db_ProdutoCarrinho)
    return db_ProdutoCarrinho

def deleteProdutoCarrinho(db : Session, idProduto : int, idCarrinho : int):
    db_ProdutoCarrinho = db.query(models.ProdutoCarrinho).filter(models.ProdutoCarrinho.idProduto == idProduto and models.ProdutoCarrinho.idCarrinho == idCarrinho)
    db_ProdutoCarrinho.delete()
    db.commit()
    return db_ProdutoCarrinho
