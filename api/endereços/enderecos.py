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

@app.route('/enderecos', methods=['GET'])
@auth.login_required
def enderecos_ativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_ENDERECOS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/enderecos/inativos', methods=['GET'])
@auth.login_required
def enderecos_inativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_INATIVOS_ENDERECOS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/enderecos/<int:id>', methods=['GET'])
@auth.login_required
def visualizar_enderecos(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_ENDERECOS_ESPECIFICO, id)
		linhas = cursor.fetchone()

		if not linhas:
			return jsonify({'mensagem':'Endereco nao cadastrado!', 'status':'404'}), 404
		
		resposta = jsonify(linhas)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close()
		conn.close()

@app.route('/enderecos/cliente', methods=['GET'])
@auth.login_required
def visualizar_enderecos_clientes():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_ENDERECOS_CLIENTES_TODOS)
		linhas = cursor.fetchall()		
		resposta = jsonify(linhas)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close()
		conn.close()

@app.route('/enderecos/cliente/<string:nome>', methods=['GET'])
@auth.login_required
def visualizar_enderecos_cliente(nome):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_ENDERECOS_CLIENTES, (nome, "%"))
		linhas = cursor.fetchall()

		if not linhas:
			return jsonify({'mensagem':'Endereco nao cadastrado!', 'status':'404'}), 404
		
		resposta = jsonify(linhas)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close()
		conn.close()

@app.route('/enderecos', methods=['POST'])
@auth.login_required
def cadastro_enderecos():
	try:
		json = request.json
		rua = json['Rua']
		bairro = json['bairro']
		cep = json['cep']
		cidade = json['cidade']
		complemento = json ['complemento']
		estado = json ['estado']
		numero = json ['numero']
		id_cliente_FK = json ['ID cliente']
		if rua and bairro and cep and cidade and complemento and estado and numero and id_cliente_FK and request.method == 'POST':
			dados = (rua,numero, bairro, complemento, cep, cidade, estado, id_cliente_FK)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(SQL_POST_ENDERECOS, dados)
			cursor.execute(SQL_GET_CLIENTE, id_cliente_FK)
			cliente = cursor.fetchone()

			if not cliente:
				return jsonify({"mensagem":"Cliente não cadastrado.", "status":"404"}), 404
				
			conn.commit()
			mensagem = {
				'status': 200,
				'mensagem': 'Endereço adicionado com sucesso!'
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

@app.route('/enderecos', methods=['PUT'])
@auth.login_required
def atualizar_enderecos():
	try:
		json = request.json
		id = json['ID']
		rua = json['Rua']
		bairro = json['bairro']
		cep = json['cep']
		cidade = json['cidade']
		complemento = json['complemento']
		estado = json['estado']
		numero = json['numero']
		id_cliente = json['ID cliente']
		if rua and bairro and cep and cidade and complemento and estado and numero and id_cliente and request.method == 'PUT':
			dados = (rua, numero, bairro, complemento, cep, cidade, estado, id_cliente, id)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			
			endereco = cursor.execute(SQL_GET_ENDERECOS_PUT, id)
			cursor.execute(SQL_GET_CLIENTE, id_cliente)
			cliente = cursor.fetchone()
				
			if not endereco:
				return jsonify({"mensagem":"Endereço não cadastrado.", "status":"404"}), 404
			
			elif not cliente:
				return jsonify({"mensagem":"Cliente não cadastrado.", "status":"404"}), 404

			cursor.execute(SQL_PUT_ENDERECOS, dados)
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

@app.route('/enderecos/<int:id>', methods=['DELETE'])
@auth.login_required
def excluir_enderecos(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(SQL_GET_ENDERECOS_ESPECIFICO, id)
		linha = cursor.fetchone()
		
		if not linha:
			mensagem = {
				'status': 404,
				'mensagem': 'Endereço não cadastrado!'
				}
			return jsonify (mensagem)
		
		else:
			cursor.execute(SQL_DELETE_CLIENTES, id) 
			conn.commit()
			mensagem = {
					'status': 200,
					'mensagem': 'Endereço deletado com sucesso!'
				}
			return jsonify(mensagem)
	
	except Exception as e:
		return jsonify({'error':f'{e}'})
	finally:
		cursor.close() 
		conn.close()

SQL_GET_CLIENTE = "select * from clientes where id_clientes_PK = %s"
SQL_GET_ENDERECOS_PUT = "select * from enderecos where id_enderecos_PK = %s"
SQL_GET_ENDERECOS = "select id_enderecos_PK as ID,rua as Rua,numero_enderecos as numero,bairro as bairro,complemento as complemento,cep as cep,cidade as cidade,estado as estado from enderecos where status = '1' order by id_enderecos_PK"
SQL_GET_INATIVOS_ENDERECOS = "select id_enderecos_PK as ID,rua as Rua,numero_enderecos as numero,bairro as bairro,complemento as complemento,cep as cep, cidade as cidade,estado as estado from enderecos WHERE status = '0' order by id_enderecos_PK"
SQL_GET_ENDERECOS_ESPECIFICO = "select id_enderecos_PK as ID,rua as Rua,numero_enderecos as numero,bairro as bairro,complemento as complemento,cep as cep,cidade as cidade,estado as estado from enderecos WHERE status = 1 and id_enderecos_PK = %s order by id_enderecos_PK"
SQL_GET_ENDERECOS_CLIENTES = "select clientes.id_clientes_PK as ID,clientes.nome as Nome,enderecos.rua as Rua,enderecos.numero_enderecos as numero,enderecos.bairro as bairro, enderecos.complemento as complemento,enderecos.cep as cep,enderecos.cidade as cidade,enderecos.estado as estado from clientes join enderecos on clientes.id_clientes_PK = enderecos.id_clientes_FK where nome like %s %s and clientes.status = 1"
SQL_GET_ENDERECOS_CLIENTES_TODOS = "select clientes.id_clientes_PK as ID,clientes.nome as Nome,enderecos.rua as Rua,enderecos.numero_enderecos as numero,enderecos.bairro as bairro, enderecos.complemento as complemento,enderecos.cep as cep,enderecos.cidade as cidade,enderecos.estado as estado from clientes join enderecos on clientes.id_clientes_PK = enderecos.id_clientes_FK where clientes.status = 1"
SQL_POST_ENDERECOS = "insert enderecos values (default, %s, %s, %s, %s, %s, %s, %s, %s, 1)"
SQL_PUT_ENDERECOS = "UPDATE enderecos SET rua = %s, numero_enderecos = %s, bairro = %s, complemento = %s, cep = %s, cidade = %s, estado = %s, id_clientes_FK = %s WHERE id_enderecos_PK = %s;"
SQL_DELETE_CLIENTES = "update enderecos SET status='0' WHERE id_enderecos_PK=%s"

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
    app.run(debug=True, port=5002)