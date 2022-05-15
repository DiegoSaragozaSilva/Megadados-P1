DROP DATABASE IF EXISTS ecommerce;
CREATE DATABASE ecommerce;
USE ecommerce;

CREATE TABLE Produto (
	idProduto INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(40) NOT NULL,
    descricao VARCHAR(120),
    preco FLOAT NOT NULL,
    
    PRIMARY KEY (idProduto)
);

CREATE TABLE Carrinho (
	idCarrinho INT NOT NULL AUTO_INCREMENT,
    
    PRIMARY KEY (idCarrinho)
);

CREATE TABLE ProdutoCarrinho (
	idProduto INT NOT NULL,
    idCarrinho INT NOT NULL,
    quantidade INT NOT NULL,
    
    PRIMARY KEY (idProduto, idCarrinho),
    FOREIGN KEY (idProduto) REFERENCES Produto(idProduto) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idCarrinho) REFERENCES Carrinho(idCarrinho) ON DELETE CASCADE ON UPDATE NO ACTION
);