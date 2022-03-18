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

@app.route('/produtos', methods=['GET'])
@auth.login_required
def produtos_ativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_PRODUTOS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/produtos/inativos', methods=['GET'])
@auth.login_required
def produtos_inativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_INATIVOS_PRODUTOS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/produtos/<string:nome>')
@auth.login_required
def visualizar_produtos(nome):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_PRODUTOS_ESPECIFICO, (nome, "%"))
		linhas = cursor.fetchall()

		if not linhas:
			return jsonify({'mensagem':'Produto nao cadastrado!', 'status':'404'}), 404
		
		resposta = jsonify(linhas)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close()
		conn.close()

@app.route('/produtos', methods=['POST'])
@auth.login_required
def cadastro_produtos():
	try:
		json = request.json
		descricao = json['descricao']
		produto = json['produto']
		if descricao and produto and request.method == 'POST':
			dados = (produto, descricao)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(SQL_POST_PRODUTOS, dados)
			conn.commit()
			mensagem = {
				'status': 200,
				'mensagem': 'Produto adicionado com sucesso!'
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

@app.route('/produtos', methods=['PUT'])
@auth.login_required
def atualizar_clientes():
	try:
		json = request.json
		id = json['ID']
		descricao = json['descricao']
		produto = json['Produto']
		if id and descricao and produto and request.method == 'PUT':
			dados = (descricao, produto, id)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			linha = cursor.execute(SQL_GET_PRODUTOS_PUT, id)

			if not linha:
				return jsonify({"mensagem":"Produto não cadastrado.", "status":"404"}), 404

			cursor.execute(SQL_PUT_PRODUTOS, dados)
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

@app.route('/produtos/<int:id>', methods=['DELETE'])
@auth.login_required
def excluir_produtos(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(SQL_GET_PRODUTOS_ESPECIFICO_DELETE, id)
		linha = cursor.fetchone()
		
		if not linha:
			mensagem = {
				'status': 404,
				'mensagem': 'Produto não cadastrado!'
				}
			return jsonify (mensagem)
		
		else:
			cursor.execute(SQL_DELETE_PRODUTOS, id) 
			conn.commit()
			mensagem = {
					'status': 200,
					'mensagem': 'Produto deletado com sucesso!'
				}
			return jsonify(mensagem)
	
	except Exception as e:
		return jsonify({'error':f'{e}'})
	finally:
		cursor.close() 
		conn.close()

SQL_GET_PRODUTOS_PUT = "select * from produtos where id_produtos_PK = %s"
SQL_GET_PRODUTOS = "select id_produtos_PK as ID, produto as Produto, descricao as descricao from produtos  where status = 1 order by id_produtos_PK"
SQL_GET_INATIVOS_PRODUTOS = "select id_produtos_PK as ID, descricao as descricao, produto as Produto from produtos where status = 0 order by id_produtos_PK"
SQL_GET_PRODUTOS_ESPECIFICO = "select id_produtos_PK as ID, descricao as descricao, produto as Produto from produtos where status = 1 and produto like %s %s order by id_produtos_PK"
SQL_POST_PRODUTOS = "insert produtos(id_produtos_PK, produto, descricao, status) values (default, %s, %s, 1)"
SQL_PUT_PRODUTOS = "update produtos SET produto = %s, descricao = %s WHERE id_produtos_PK = %s"
SQL_GET_PRODUTOS_ESPECIFICO_DELETE = "select * from produtos where id_produtos_PK = %s"
SQL_DELETE_PRODUTOS = "update produtos SET status= '0' WHERE id_produtos_PK=%s"

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
    app.run(debug=True, port=5004)