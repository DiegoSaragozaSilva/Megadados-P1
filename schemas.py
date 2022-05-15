from typing import List, Union
from pydantic import BaseModel, Field
from typing import Optional

class ProdutoBase(BaseModel):
    titulo : str = Field(..., example = "Urânio 235")

class ProdutoCreate(ProdutoBase):
    preco : float = Field(..., example = 70000)
    descricao : Optional[str] = Field(None, example = "Eficiente no combate a mosquitos")

class Produto(ProdutoBase):
    idProduto : int
    preco : float = Field(..., example = 70000)
    descricao : Optional[str] = Field(None, example = "Eficiente no combate a mosquitos")

    class Config:
        orm_mode = True

class Carrinho(BaseModel):
    idCarrinho : int

    class Config:
        orm_mode = True

class ProdutoCarrinhoCreate(BaseModel):
    quantidade : int = Field(..., example = 2)

class ProdutoCarrinho(ProdutoCarrinhoCreate):
    idCarrinho : int
    idProduto : int

    class Config:
        orm_mode = True
