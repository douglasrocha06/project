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

@app.route('/agenda', methods=['GET'])
@auth.login_required
def agenda():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_AGENDA)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/agenda/concluidos', methods=['GET'])
@auth.login_required
def agenda_concluido():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_AGENDA_CONCLUIDA)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/agenda/<string:nome>', methods=['GET'])
@auth.login_required
def agenda_especifico(nome):
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_AGENDA_ESPECIFICO, (nome, "%"))
		linha = cursor.fetchall()

		if not linha:
			mensagem = {
				'status': 404,
				'mensagem': 'Cliente não encontrado.'
				}	
			return jsonify(mensagem), 404
		
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

#AGENDA CARROS
@app.route('/agenda/carros', methods=['GET'])
@auth.login_required
def agenda_carro():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_CARROS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

#AGENDA MOTOS
@app.route('/agenda/motos', methods=['GET'])
@auth.login_required
def agenda_moto():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_MOTOS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

#AGENDA OUTROS
@app.route('/agenda/outros', methods=['GET'])
@auth.login_required
def agenda_outros():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_OUTROS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/agenda', methods=['POST'])
@auth.login_required
def cadastro_agenda():
	try:
		json = request.json
		data_agendamento = json['data agendada']
		horario_agendamento = json['horario agendado']
		id_cliente = json['ID cliente']
		id_veiculo = json['ID veiculo']
		if data_agendamento and horario_agendamento and id_cliente and id_veiculo and request.method == 'POST':
			dados = (data_agendamento, horario_agendamento, id_cliente, id_veiculo)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)

			cursor.execute(SQL_POST_AGENDA, dados)
			conn.commit()
			mensagem = {
				'status': 200,
				'mensagem': 'Agendamento realizado com sucesso!'
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

@app.route('/agenda', methods=['PUT'])
@auth.login_required
def atualizar_agenda():
	try:
		json = request.json
		id_agendamento = json['ID agendamento']
		data_agendamento = json['data agendada']
		horario_agendamento = json['horario agendado']
		id_cliente = json['ID cliente']
		id_veiculo = json['ID veiculo']
		if id_agendamento and data_agendamento and horario_agendamento and id_cliente and id_veiculo and request.method == 'PUT':
			dados = (data_agendamento, horario_agendamento, id_cliente, id_veiculo, id_agendamento)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)

			cursor.execute(SQL_GET_AGENDA_PUT, id_agendamento)
			agenda = cursor.fetchone()
			
			cursor.execute(SQL_GET_CLIENTE_PUT, id_cliente)
			cliente = cursor.fetchone()

			cursor.execute(SQL_GET_VEICULO_PUT, id_veiculo)
			veiculo = cursor.fetchone()

			if not agenda:
				return jsonify({"status":"Agendamento inexistente"}), 404
			
			elif not cliente:
				return jsonify({"status":"Cliente não cadastrado."}), 404

			elif not veiculo:
				return jsonify({"status":"Veiculo não cadastrado."}), 404

			cursor.execute(SQL_PUT_AGENDA, dados)
			conn.commit()
			mensagem = {
				'status': 200,
				'mensagem': 'Agendamento atualizados com sucesso!'
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

@app.route('/agenda/<int:id>', methods=['DELETE'])
@auth.login_required
def excluir_agendamento(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(SQL_GET_AGENDA_ESPECIFICO_DELETE, id)
		linha = cursor.fetchone()
		
		if not linha:
			mensagem = {
				'status': 404,
				'mensagem': 'Agendamento não cadastrado!'
				}
			return jsonify (mensagem), 404
		
		else:
			cursor.execute(SQL_DELETE_AGENDA, id) 
			conn.commit()
			mensagem = {
					'status': 200,
					'mensagem': 'Agendamento deletado com sucesso!'
				}
			return jsonify(mensagem)
	
	except Exception as e:
		return jsonify({'error':f'{e}'})
	finally:
		cursor.close() 
		conn.close()

SQL_GET_AGENDA_PUT = "select * from agendamentos where id_agendamento_PK = %s"
SQL_GET_CLIENTE_PUT = "select * from clientes where id_clientes_PK = %s"
SQL_GET_VEICULO_PUT = "select * from veiculos where id_veiculos_PK = %s"
SQL_GET_AGENDA = "select clientes.nome as Nome,veiculos.tipo as tipo,veiculos.veiculo as Veiculo,veiculos.placa as placa,veiculos.cor as cor,veiculos.ano as ano,date_format(data_agendamento, GET_FORMAT(DATE,'EUR')) as 'Data agendada', agendamentos.horario_agendamento as 'horario agendado' from clientes inner join agendamentos on clientes.id_clientes_PK = agendamentos.id_clientes_FK inner join veiculos on veiculos.id_veiculos_PK = agendamentos.id_veiculos_FK where agendamentos.concluido = 'nao' order by data_agendamento, id_agendamento_PK"
SQL_GET_AGENDA_CONCLUIDA = "select clientes.nome as Nome,veiculos.tipo as tipo,veiculos.veiculo as Veiculo,veiculos.placa as placa,veiculos.cor as cor,veiculos.ano as ano,date_format(data_agendamento, GET_FORMAT(DATE,'EUR')) as 'Data agendada', agendamentos.horario_agendamento as 'horario agendado' from clientes inner join agendamentos on clientes.id_clientes_PK = agendamentos.id_clientes_FK inner join veiculos on veiculos.id_veiculos_PK = agendamentos.id_veiculos_FK where agendamentos.concluido = 'sim' order by data_agendamento"
SQL_GET_AGENDA_ESPECIFICO = "select agendamentos.id_agendamento_PK as 'ID', clientes.nome as Nome,veiculos.veiculo as Veiculo,veiculos.placa as placa,veiculos.cor as cor,veiculos.ano as ano,date_format(data_agendamento, GET_FORMAT(DATE,'EUR')) as 'Data agendada',  agendamentos.horario_agendamento as 'horario agendado' from clientes inner join agendamentos on clientes.id_clientes_PK = agendamentos.id_clientes_FK inner join veiculos on veiculos.id_veiculos_PK = agendamentos.id_veiculos_FK where agendamentos.concluido = 'nao' and clientes.nome like %s %s order by data_agendamento, id_agendamento_PK"
SQL_GET_CARROS = "select clientes.nome as Nome,veiculos.tipo as tipo,veiculos.veiculo as Veiculo,veiculos.placa as placa,veiculos.cor as cor,veiculos.ano as ano,date_format(data_agendamento, GET_FORMAT(DATE,'EUR')) as 'Data agendada',agendamentos.horario_agendamento as 'horario agendado' from clientes inner join agendamentos on clientes.id_clientes_PK = agendamentos.id_clientes_FK inner join veiculos on veiculos.id_veiculos_PK = agendamentos.id_veiculos_FK where tipo = 'carro' and agendamentos.concluido = 'nao' order by data_agendamento, id_agendamento_PK"
SQL_GET_MOTOS = "select clientes.nome as Nome,veiculos.tipo as tipo,veiculos.veiculo as Veiculo,veiculos.placa as placa,veiculos.cor as cor,veiculos.ano as ano,date_format(data_agendamento, GET_FORMAT(DATE,'EUR')) as 'Data agendada',agendamentos.horario_agendamento as 'horario agendado' from clientes inner join agendamentos on clientes.id_clientes_PK = agendamentos.id_clientes_FK inner join veiculos on veiculos.id_veiculos_PK = agendamentos.id_veiculos_FK where tipo = 'moto' and agendamentos.concluido = 'nao' order by data_agendamento, id_agendamento_PK"
SQL_GET_OUTROS = "select clientes.nome as Nome,veiculos.tipo as tipo,veiculos.veiculo as Veiculo,veiculos.placa as placa,veiculos.cor as cor,veiculos.ano as ano,date_format(data_agendamento, GET_FORMAT(DATE,'EUR')) as 'Data agendada',agendamentos.horario_agendamento as 'horario agendado' from clientes inner join agendamentos on clientes.id_clientes_PK = agendamentos.id_clientes_FK inner join veiculos on veiculos.id_veiculos_PK = agendamentos.id_veiculos_FK where tipo <> 'moto' and tipo <> 'carro' and agendamentos.concluido = 'nao' order by data_agendamento, id_agendamento_PK"
SQL_POST_AGENDA = "insert into agendamentos (id_agendamento_PK, data_agendamento, horario_agendamento, id_clientes_FK, id_veiculos_FK, status, concluido) values (default, %s, %s, %s, %s, 1, 'nao')"
SQL_PUT_AGENDA = "UPDATE agendamentos SET data_agendamento = %s, horario_agendamento = %s, id_clientes_FK = %s, id_veiculos_FK = %s WHERE id_agendamento_PK = %s"
SQL_GET_AGENDA_ESPECIFICO_DELETE = "select agendamentos.id_agendamento_PK as 'ID', clientes.nome as Nome,veiculos.veiculo as Veiculo,veiculos.placa as placa,veiculos.cor as cor,veiculos.ano as ano,date_format(data_agendamento, GET_FORMAT(DATE,'EUR')) as 'Data agendada',  agendamentos.horario_agendamento as 'horario agendado' from clientes inner join agendamentos on clientes.id_clientes_PK = agendamentos.id_clientes_FK inner join veiculos on veiculos.id_veiculos_PK = agendamentos.id_veiculos_FK where agendamentos.id_agendamento_PK = %s order by data_agendamento, id_agendamento_PK"
SQL_DELETE_AGENDA = "UPDATE agendamentos SET status = '0', concluido = 'sim' WHERE id_agendamento_PK = %s"

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
    app.run(debug=True, port=5000)