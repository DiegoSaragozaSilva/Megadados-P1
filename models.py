from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Produto(Base):
    __tablename__ = "Produto"

    idProduto = Column(Integer, primary_key = True, index = True, nullable = False, autoincrement = True)
    titulo = Column(String(40), nullable = False)
    descricao = Column(String(120), nullable = True)
    preco = Column(Float, nullable = False)
    
class Carrinho(Base):
    __tablename__ = "Carrinho"
    
    idCarrinho = Column(Integer, primary_key = True, index = True, nullable = False, autoincrement = True)

class ProdutoCarrinho(Base):
    __tablename__ = "ProdutoCarrinho"

    idCarrinho = Column(Integer, ForeignKey("Carrinho.idCarrinho", ondelete="CASCADE", onupdate="CASCADE"), primary_key = True)
    idProduto = Column(Integer, ForeignKey("Produto.idProduto", ondelete="CASCADE", onupdate="CASCADE"), primary_key = True)
    quantidade = Column(Integer, nullable = False)

    produto = relationship("Produto", back_populates="ProdutoCarrinho",  cascade="all, delete-orphan")
    carrinho = relationship("Carrinho", back_populates="ProdutoCarrinho",  cascade="all, delete-orphan")
