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

@app.route('/veiculos', methods=['GET'])
@auth.login_required
def veiculos_ativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_VEICULOS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/veiculos/inativos', methods=['GET'])
@auth.login_required
def veiculos_inativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_INATIVOS_VEICULOS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/veiculos/inativo/<int:id>', methods=['GET'])
@auth.login_required
def veiculos_inativos_especifico(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_VEICULOS_ESPECIFICO_INATIVO, id)
		linhas = cursor.fetchall()

		if not linhas:
			return jsonify({'mensagem':'Veiculo nao cadastrado!', 'status':'404'}), 404
		
		resposta = jsonify(linhas)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close()
		conn.close()

@app.route('/veiculos/<int:id>', methods=['GET'])
@auth.login_required
def visualizar_veiculos(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_VEICULOS_ESPECIFICO, id)
		linhas = cursor.fetchall()

		if not linhas:
			return jsonify({'mensagem':'Veiculo nao cadastrado!', 'status':'404'}), 404
		
		resposta = jsonify(linhas)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close()
		conn.close()

@app.route('/veiculos', methods=['POST'])
@auth.login_required
def cadastro_veiculos():
	try:
		json = request.json
		tipo = json['tipo']
		placa = json['placa']
		veiculo = json['veiculo']
		cor = json['cor']
		ano = json['ano']
		id_cliente = json['ID cliente']
		if ano and cor and placa and tipo and veiculo and id_cliente and request.method == 'POST':
			dados = (tipo, placa, veiculo, cor, ano, id_cliente)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(SQL_POST_VEICULO, dados)
			conn.commit()
			mensagem = {
				'status': 200,
				'mensagem': 'Veículo adicionado com sucesso!'
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

@app.route('/veiculos', methods=['PUT'])
@auth.login_required
def atualizar_veiculoss():
	try:
		json = request.json
		id = json['ID']
		tipo = json['tipo']
		placa = json['placa']
		veiculo = json['veiculo']
		cor = json['cor']
		ano = json['ano']
		id_cliente = json['ID cliente']
		if ano and cor and placa and tipo and veiculo and id_cliente and id and request.method == 'PUT':
			dados = (tipo, placa, veiculo, cor, ano, id_cliente, id)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)

			veiculo = cursor.execute(SQL_GET_VEICULOS_PUT, id)
			cursor.execute(SQL_GET_CLIENTE, id_cliente)
			cliente = cursor.fetchone()
				
			if not veiculo:
				return jsonify({"mensagem":"Veiculo não cadastrado.", "status":"404"}), 404
			
			elif not cliente:
				return jsonify({"mensagem":"Cliente não cadastrado.", "status":"404"}), 404

			cursor.execute(SQL_PUT_VEICULOS, dados)
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

@app.route('/veiculos/<int:id>', methods=['DELETE'])
@auth.login_required
def excluir_veiculos(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(SQL_GET_VEICULOS_ESPECIFICO, id)
		linha = cursor.fetchone()
		
		if not linha:
			mensagem = {
				'status': 404,
				'mensagem': 'Veículo não cadastrado!'
				}
			return jsonify (mensagem)
		
		else:
			cursor.execute(SQL_DELETE_CLIENTES, id) 
			conn.commit()
			mensagem = {
					'status': 200,
					'mensagem': 'Veículo deletado com sucesso!'
				}
			return jsonify(mensagem)
	
	except Exception as e:
		return jsonify({'error':f'{e}'})
	finally:
		cursor.close() 
		conn.close()

SQL_GET_CLIENTE = "select * from clientes where id_clientes_PK = %s"
SQL_GET_VEICULOS_PUT = "select * from veiculos where id_veiculos_PK = %s"
SQL_GET_VEICULOS = "select id_veiculos_PK as ID, tipo as tipo, placa as placa, veiculo as veiculo, cor as cor, ano as ano from veiculos where status = 1"
SQL_GET_INATIVOS_VEICULOS = "select id_veiculos_PK as ID, tipo as tipo, placa as placa, veiculo as veiculo, cor as cor, ano as ano from veiculos where status = 0"
SQL_GET_VEICULOS_ESPECIFICO = "select id_veiculos_PK as ID, tipo as tipo, placa as placa, veiculo as veiculo, cor as cor, ano as ano from veiculos where status = 1 and id_veiculos_PK = %s"
SQL_GET_VEICULOS_ESPECIFICO_INATIVO = "select id_veiculos_PK as ID, tipo as tipo, placa as placa, veiculo as veiculo, cor as cor, ano as ano from veiculos where status = 0 and id_veiculos_PK = %s"
SQL_POST_VEICULO = "insert veiculos (id_veiculos_PK, tipo, placa, veiculo, cor, ano, id_clientes_FK, status) values (default, %s, %s, %s, %s, %s, %s, 1)"
SQL_PUT_VEICULOS = "update veiculos SET tipo=%s, placa=%s, veiculo=%s, cor=%s, ano=%s, id_clientes_FK=%s WHERE id_veiculos_PK=%s"
SQL_GET_CLIENTES_ESPECIFICO_DELETE = "select id_clientes_PK as ID,nome as Nome,cpf as cpf,date_format(data_nascimento, GET_FORMAT(DATE,'EUR')) as 'data de Nascimento',email as email from clientes where id_clientes_PK = %s order by id_clientes_PK"
SQL_DELETE_CLIENTES = "update veiculos SET status='0' WHERE id_veiculos_PK=%s"

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
    app.run(debug=True, port=5005)