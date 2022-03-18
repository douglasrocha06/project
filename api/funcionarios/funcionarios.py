from flask import Flask
from flask_httpauth import HTTPBasicAuth
from pymysql import cursors
from config import mysql
from flask import jsonify
from flask import request
import pymysql

app = Flask(__name__)
auth = HTTPBasicAuth()

@app.route("/")
@auth.login_required
def index():
    return "Bem vindo ao sistema Lavacar."

@app.route('/funcionarios', methods=['GET'])
@auth.login_required
def funcionario_ativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_ATIVOS_FUNCIONARIOS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/funcionarios/inativos', methods=['GET'])
@auth.login_required
def funcionarios_inativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_INATIVOS_FUNIONARIOS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/funcionarios/<string:nome>')
@auth.login_required
def visualizar_funcionarios(nome):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_FUNCIONARIOS_ESPECIFICO, (nome, "%"))
		linhas = cursor.fetchall()

		if not linhas:
			return jsonify({'mensagem':'Funcionario nao cadastrado!', 'status':"404"}), 404
		
		resposta = jsonify(linhas)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close()
		conn.close()

@app.route('/funcionarios', methods=['POST'])
@auth.login_required
def cadastro_funcionario():
	try:
		json = request.json
		nome = json['Nome']
		contato = json['contato']
		data_admissao = json['data de admissao']
		data_nascimento = json['data de nascimento']
		if nome and contato and data_admissao and data_nascimento and request.method == 'POST':
			dados = (nome, contato, data_admissao, data_nascimento)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(SQL_POST_FUNCIONARIOS, dados)
			conn.commit()
			mensagem = {
				'status': 200,
				'mensagem': 'Colaborador cadastrado com sucesso!'
			}
			resposta = jsonify(mensagem)
			resposta.status_code = 200
			return resposta
		else:
			return not_found()
	except Exception as e:
		return jsonify({'error':f'{e}'})
	finally:
		cursor.close() 
		conn.close()

@app.route('/funcionarios', methods=['PUT'])
@auth.login_required
def atualizar_funcionarios():
	try:
		json = request.json
		id = json['ID']
		nome = json['Nome']
		contato = json['contato']
		data_admissao = json['data de admissao']
		data_nascimento = json['data de nascimento']
		if nome and contato and data_admissao and data_nascimento and id and request.method == 'PUT':
			dados = (nome, contato, data_admissao, data_nascimento, id)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			colaborador = cursor.execute(SQL_GET_FUNCIONARIO_PUT, id)

			if not colaborador:
				return jsonify({"mensagem":"Colaborador não cadastrado.", 'status':"404"}), 404

			cursor.execute(SQL_PUT_CLIENTES, dados)
			conn.commit()
			mensagem = {
				'status': 200,
				'mensagem': 'Dados atualizados com sucesso!'
			}
			resposta = jsonify(mensagem)
			resposta.status_code = 200
			return resposta
		else:
			return not_found()
	except Exception as e:
		return jsonify({'error':f'{e}'})
	finally:
		cursor.close() 
		conn.close()

@app.route('/funcionarios/<int:id>', methods=['DELETE'])
@auth.login_required
def excluir_funcionarios(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(SQL_GET_FUNCIONARIOS_ESPECIFICO_DELETE, id)
		linha = cursor.fetchone()
		
		if not linha:
			mensagem = {
				'status': 404,
				'mensagem': 'Funcionario não cadastrado!'
				}
			return jsonify (mensagem)
		
		else:
			cursor.execute(SQL_DELETE_CLIENTES, id) 
			conn.commit()
			mensagem = {
					'status': 200,
					'mensagem': 'Funcionario deletado com sucesso!'
				}
			return jsonify(mensagem)
	
	except Exception as e:
		return jsonify({'error':f'{e}'})
	finally:
		cursor.close() 
		conn.close()

SQL_GET_FUNCIONARIO_PUT = "select * from funcionarios where id_colaborador_PK = %s"
SQL_GET_ATIVOS_FUNCIONARIOS = "select id_colaborador_PK as ID,nome as Nome, contato as contato, date_format(data_nascimento, GET_FORMAT(DATE,'EUR')) as 'data de nascimento',date_format(data_admissao, GET_FORMAT(DATE,'EUR')) as 'data de admissao' from funcionarios where status = 1 order by id_colaborador_PK"
SQL_GET_INATIVOS_FUNIONARIOS = "select id_colaborador_PK as ID,nome as Nome, contato as contato, date_format(data_nascimento, GET_FORMAT(DATE,'EUR')) as 'data de nascimento',date_format(data_admissao, GET_FORMAT(DATE,'EUR')) as 'data de admissao' from funcionarios where status = 0 order by id_colaborador_PK"
SQL_GET_FUNCIONARIOS_ESPECIFICO = "select id_colaborador_PK as ID,nome as Nome, contato as contato, date_format(data_nascimento, GET_FORMAT(DATE,'EUR')) as 'data de nascimento',date_format(data_admissao, GET_FORMAT(DATE,'EUR')) as 'data de admissao' from funcionarios where nome like %s %s and funcionarios.status = 1 order by id_colaborador_PK"
SQL_POST_FUNCIONARIOS = "insert into funcionarios (id_colaborador_PK, nome, contato, data_nascimento, data_admissao, status) values (default, %s, %s, %s, %s, 1)"
SQL_PUT_CLIENTES = "update funcionarios set nome = %s, contato = %s, data_nascimento = %s, data_admissao = %s where id_colaborador_PK = %s"
SQL_GET_FUNCIONARIOS_ESPECIFICO_DELETE = "select * from funcionarios where id_colaborador_PK = %s"
SQL_DELETE_CLIENTES = "update funcionarios SET status = '0' WHERE id_colaborador_PK = %s"

#Caso não encontre o caminho
@app.errorhandler(404)
def not_found(error=None):
    messagem = {
        'status': 404,
        'mensagem': 'Pagina nao encontrada: ' + request.url,
    }
    respone = jsonify(messagem)
    respone.status_code = 404
    return respone

#Método do Basic Authentication
@auth.verify_password
def verificacao(login, senha):
	usuarios= {
			'douglas':'123',
	}
	if not (login, senha):
		return False
	return usuarios.get(login) == senha

if __name__ == "__main__":
    app.run(debug=True, port=5003)