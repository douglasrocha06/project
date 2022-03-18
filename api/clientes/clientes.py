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

@app.route('/clientes', methods=['GET'])
@auth.login_required
def clientes_ativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_CLIENTES)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/clientes/inativos', methods=['GET'])
@auth.login_required
def clientes_inativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_INATIVOS_CLIENTES)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/clientes/<string:nome>')
@auth.login_required
def visualizar_clientes(nome):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_CLIENTES_ESPECIFICO, (nome, "%"))
		linhas = cursor.fetchall()

		if not linhas:
			return jsonify({'status':'Cliente nao cadastrado!'}), 404
		
		resposta = jsonify(linhas)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close()
		conn.close()

@app.route('/clientes', methods=['POST'])
@auth.login_required
def cadastro_clientes():
	try:
		json = request.json
		nome = json['Nome']
		cpf = json['cpf']
		data_nascimento = json['data de Nascimento']
		email = json['email']
		if nome and cpf and data_nascimento and email and request.method == 'POST':
			dados = (nome, cpf, data_nascimento, email)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(SQL_POST_CLIENTES, dados)
			conn.commit()
			mensagem = {
				'status': 200,
				'mensagem': 'Cliente adicionado com sucesso!'
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

@app.route('/clientes', methods=['PUT'])
@auth.login_required
def atualizar_clientes():
	try:
		json = request.json
		id = json['ID']
		nome = json['Nome']
		cpf = json['cpf']
		data_nascimento = json['data de Nascimento']
		email = json['email']
		if nome and cpf and data_nascimento and email and id and request.method == 'PUT':
			dados = (nome, cpf, data_nascimento, email, id)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cliente = cursor.execute(SQL_GET_CLIENTES_PUT, id)

			if not cliente:
				return jsonify({"mensagem":"Cliente não encontrado.", "status":"404"}), 404

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

@app.route('/clientes/<int:id>', methods=['DELETE'])
@auth.login_required
def excluir_clientes(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(SQL_GET_CLIENTES_ESPECIFICO_DELETE, id)
		linha = cursor.fetchone()
		
		if not linha:
			mensagem = {
				'status': 404,
				'mensagem': 'Cliente não cadastrado!'
				}
			return jsonify (mensagem)
		
		else:
			cursor.execute(SQL_DELETE_CLIENTES, id) 
			conn.commit()
			mensagem = {
					'status': 200,
					'mensagem': 'Cliente deletado com sucesso!'
				}
			return jsonify(mensagem)
	
	except Exception as e:
		return jsonify({'error':f'{e}'})
	finally:
		cursor.close() 
		conn.close()

SQL_GET_CLIENTES_PUT = "select * from clientes where id_clientes_PK = %s"
SQL_GET_CLIENTES = "select id_clientes_PK as ID,nome as Nome,cpf as cpf,date_format(data_nascimento, GET_FORMAT(DATE,'EUR')) as 'data de Nascimento',email as email from clientes where status='1' order by id_clientes_PK"
SQL_GET_INATIVOS_CLIENTES = "select id_clientes_PK as ID,nome as Nome,cpf as cpf,date_format(data_nascimento, GET_FORMAT(DATE,'EUR')) as 'data de Nascimento',email as email from clientes where status = '0' order by id_clientes_PK"
SQL_GET_CLIENTES_ESPECIFICO = "select id_clientes_PK as ID,nome as Nome,cpf as cpf,date_format(data_nascimento, GET_FORMAT(DATE,'EUR')) as 'data de Nascimento',email as email from clientes where nome like %s %s and status='1' order by id_clientes_PK"
SQL_POST_CLIENTES = "insert clientes (id_clientes_PK, nome, cpf, data_nascimento, email, status) values (default, %s, %s, %s, %s, 1)"
SQL_PUT_CLIENTES = "update clientes SET nome=%s, cpf=%s, data_nascimento=%s, email=%s WHERE id_clientes_PK=%s"
SQL_GET_CLIENTES_ESPECIFICO_DELETE = "select id_clientes_PK as ID,nome as Nome,cpf as cpf,date_format(data_nascimento, GET_FORMAT(DATE,'EUR')) as 'data de Nascimento',email as email from clientes where id_clientes_PK = %s order by id_clientes_PK"
SQL_DELETE_CLIENTES = "update clientes SET status= '0' WHERE id_clientes_PK=%s"

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
    app.run(debug=True, port=5001)