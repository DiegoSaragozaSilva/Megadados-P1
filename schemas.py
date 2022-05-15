from typing import List, Union
from pydantic import BaseModel

class ProdutoBase(BaseModel):
    titulo : str

class ProdutoCreate(ProdutoBase):
    preco : float
    descricao : str = None

class Produto(ProdutoBase):
    idProduto : int

    class Config:
        orm_mode = True

class CarrinhoBase(BaseModel):
    pass

class CarrinhoCreate(CarrinhoBase):
    pass

class Carrinho(CarrinhoBase):
    idCarrinho : int

    class Config:
        orm_mode = True

class ProdutoCarrinhoBase(BaseModel):
    pass

class ProdutoCarrinhoCreate(ProdutoCarrinhoBase):
    quantidade : int

class ProdutoCarrinho(ProdutoCarrinhoBase):
    idCarrinho : int
    idProduto : int

    class Config:
        orm_mode = True