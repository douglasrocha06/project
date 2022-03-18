create database lavacar;

use lavacar;

CREATE TABLE clientes (
	id_clientes_PK int(50) NOT NULL AUTO_INCREMENT,
	nome varchar(50) NOT NULL,
	cpf varchar(50) NOT NULL UNIQUE,
	data_nascimento DATE NOT NULL,
	email varchar(50) NOT NULL,
	status int(50) NOT NULL,
	PRIMARY KEY (id_clientes_PK)
);
INSERT INTO clientes (nome, cpf, data_nascimento, email, status) 
VALUES ('Douglas', '10678256477', '1999-08-28', 'douglas.santos@gmail.com', '1');

INSERT INTO clientes (nome, cpf, data_nascimento, email, status) 
VALUES ('Matheus', '84672548766', '2000-10-07', 'matheus.silva@gmail.com', '1');

INSERT INTO clientes (nome, cpf, data_nascimento, email, status) 
VALUES ('Carlos', '67341987645', '1994-10-27', 'carlos.antonio@gmail.com', '1');

CREATE TABLE enderecos (
	id_enderecos_PK int(50) NOT NULL AUTO_INCREMENT,
	rua varchar(50) NOT NULL,
	numero_enderecos int(50) NOT NULL,
	bairro varchar(50) NOT NULL,
	complemento varchar(50) NOT NULL,
	cep varchar(50) NOT NULL,
	cidade varchar(50) NOT NULL,
	estado varchar(50) NOT NULL,
	id_clientes_FK varchar(50) NOT NULL,
	status int(50) NOT NULL,
	PRIMARY KEY (id_enderecos_PK)
);
INSERT INTO enderecos (rua, numero_enderecos, bairro, complemento, cep, cidade, estado, id_clientes_FK, status) 
VALUES ('Guarabira', '562', 'Jardim Maresias', 'Casa 2', '71563098', 'São Paulo', 'SP', '1', '1');

INSERT INTO enderecos (rua, numero_enderecos, bairro, complemento, cep, cidade, estado, id_clientes_FK, status) 
VALUES ('Ricardo de Souza', '75', 'Iracema', 'APTO 10', '25678255', 'São Paulo', 'SP', '2', '1');

CREATE TABLE agendamentos (
	id_agendamento_PK int(50) NOT NULL AUTO_INCREMENT,
	data_agendamento DATE NOT NULL,
	horario_agendamento varchar(50) NOT NULL,
	id_clientes_FK int(50) NOT NULL,
	id_veiculos_FK int(50) NOT NULL,
	status int(50) NOT NULL,
	concluido varchar(50) NOT NULL,
	PRIMARY KEY (id_agendamento_PK)
);
INSERT INTO agendamentos (data_agendamento, horario_agendamento, id_clientes_FK, id_veiculos_FK, status, concluido) 
VALUES ('2022-10-20', '11:30', '1', '2', '1', 'nao');

INSERT INTO agendamentos (data_agendamento, horario_agendamento, id_clientes_FK, id_veiculos_FK, status, concluido) 
VALUES ('2022-10-28', '15:30', '2', '2', '0', 'sim');

CREATE TABLE produtos (
	id_produtos_PK int(50) NOT NULL AUTO_INCREMENT,
	produto varchar(50) NOT NULL,
	descricao varchar(50) NOT NULL,
	status int(50) NOT NULL,
	PRIMARY KEY (id_produtos_PK)
);
INSERT INTO produtos (produto, descricao, status) VALUES ('Pretinho', 'Utilizado nos pneus dos veículos', '1');
INSERT INTO produtos (produto, descricao, status) VALUES ('Pano', 'Secagem dos veículos', '1');
INSERT INTO produtos (produto, descricao, status) VALUES ('Bucha', 'Utilizado lavagem', '1');
INSERT INTO produtos (produto, descricao, status) VALUES ('Aromatizador', 'Aroma nos veiculos', '1');

CREATE TABLE veiculos (
	id_veiculos_PK int(50) NOT NULL AUTO_INCREMENT,
	tipo varchar(50) NOT NULL,
	placa varchar(50) NOT NULL,
	veiculo varchar(50) NOT NULL,
	cor varchar(50) NOT NULL,
	ano varchar(50) NOT NULL,
	status int(50) NOT NULL,
	id_clientes_FK int(50) NOT NULL,
	PRIMARY KEY (id_veiculos_PK)
);
INSERT INTO veiculos (tipo, placa, veiculo, cor, ano, status, id_clientes_FK) 
VALUES ('carro', 'ESF-9362', 'Onix 1.0', 'Vermelho', '2014', '1', '1');

INSERT INTO veiculos (tipo, placa, veiculo, cor, ano, status, id_clientes_FK) 
VALUES ('moto', 'IRH-5254', 'Fan 125', 'Preta', '2022', '1', '2');

INSERT INTO veiculos (tipo, placa, veiculo, cor, ano, status, id_clientes_FK) 
VALUES ('Onibus', 'IEY-7652', 'Vw', 'Branca', '2012', '1', '3');


CREATE TABLE vendas (
	id_vendas_PK int(50) NOT NULL AUTO_INCREMENT,
	data_venda DATE NOT NULL,
	preco real NOT NULL,
	id_clientes_FK int(50) NOT NULL,
	id_veiculo_FK int(50) NOT NULL,
	id_agendamento_FK int(50) NOT NULL,
	PRIMARY KEY (id_vendas_PK)
);
INSERT INTO vendas (data_venda, preco, id_clientes_FK, id_veiculo_FK, id_agendamento_FK)
 VALUES ('2022-10-20', '89.90', '1', '1', '1');
 
INSERT INTO vendas (data_venda, preco, id_clientes_FK, id_veiculo_FK, id_agendamento_FK) 
VALUES ('2022-04-05', '59.90', '2', '1', '1');

CREATE TABLE funcionarios (
	id_colaborador_PK int(50) NOT NULL AUTO_INCREMENT,
	nome varchar(50) NOT NULL,
	contato varchar(50) NOT NULL,
	data_nascimento DATE NOT NULL,
	data_admissao DATE NOT NULL,
	status varchar(50) NOT NULL,
	PRIMARY KEY (id_colaborador_PK)
);
INSERT INTO funcionarios (nome, contato, data_nascimento, data_admissao, status) 
VALUES ('Lucas Souza Pereira', '11 978789567', '2012-10-12', '1998-12-10', '1');

INSERT INTO funcionarios (nome, contato, data_nascimento, data_admissao, status) 
VALUES ('Rafael', '11 956452187', '1998-10-02', '2016-09-07', '1');

INSERT INTO funcionarios (nome, contato, data_nascimento, data_admissao, status) 
VALUES ('Jonathan', '11 956432982', '2001-11-12', '2014-12-12', '1');

ALTER TABLE agendamentos ADD CONSTRAINT agendamentos_fk0 FOREIGN KEY (id_clientes_FK) REFERENCES clientes(id_clientes_PK);
ALTER TABLE agendamentos ADD CONSTRAINT agendamentos_fk1 FOREIGN KEY (id_veiculos_FK) REFERENCES veiculos(id_veiculos_PK);
ALTER TABLE veiculos ADD CONSTRAINT veiculos_fk0 FOREIGN KEY (id_clientes_FK) REFERENCES clientes(id_clientes_PK);
ALTER TABLE vendas ADD CONSTRAINT vendas_fk0 FOREIGN KEY (id_clientes_FK) REFERENCES clientes(id_clientes_PK);
ALTER TABLE vendas ADD CONSTRAINT vendas_fk1 FOREIGN KEY (id_veiculo_FK) REFERENCES veiculos(id_veiculos_PK);
ALTER TABLE vendas ADD CONSTRAINT vendas_fk2 FOREIGN KEY (id_agendamento_FK) REFERENCES agendamentos(id_agendamento_PK);
