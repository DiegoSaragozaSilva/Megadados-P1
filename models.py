from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

Base = declarative_base()

class Produto(Base):
    __tablename__ = "Produto"
    idProduto = Column(Integer, primary_key = True, index = True, nullable = False, autoincrement = True)
    titulo = Column(String(40), nullable = False)
    descricao = Column(String(120), nullable = True)
    preco = Column(Float, nullable = False)
    
class Carrinho(Base):
    idCarrinho = Column(Integer, primary_key = True, index = True, nullable = False, autoincrement = True)

class ProdutoCarrinho(Base):
    idCarrinho = Column(Integer, ForeignKey("Carrinho.idCarrinho"), primary_key = True)
    idProduto = Column(Integer, ForeignKey("Produto.idProduto"), primary_key = True)
    quantidade = Column(Integer, nullable = False)