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

@app.route('/vendas', methods=['GET'])
@auth.login_required
def vendas_ativos():
	try:
		conn = mysql.connect() 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_VENDAS)
		linha = cursor.fetchall()
		resposta = jsonify(linha)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close() 
		conn.close()

@app.route('/vendas/<string:nome>')
@auth.login_required
def vendas_clientes(nome):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL_GET_VENDAS_ESPECIFICO_NOME, (nome, "%"))
		linhas = cursor.fetchall()

		if not linhas:
			return jsonify({'mensagem':'Nao existe cliente cadastrado com lavagens', 'status':'404'}), 404
		
		resposta = jsonify(linhas)
		resposta.status_code = 200
		return resposta
	except Exception as e:
		return jsonify({"error":f"{e}"})
	finally:
		cursor.close()
		conn.close()

@app.route('/vendas', methods=['POST'])
@auth.login_required
def cadastro_vendas():
	try:
		json = request.json
		venda = json['Venda']
		preco = json['preco']
		id_cliente = json['ID cliente']
		id_veiculo = json['ID veiculo']
		id_agendamento = json['ID agendamento']
		if venda and preco and id_cliente and id_veiculo and id_agendamento and request.method == 'POST':
			dados = (venda, preco, id_cliente, id_veiculo, id_agendamento)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)

			cursor.execute(SQL_GET_CLIENTE_ESPECIFICO, id_cliente)
			cliente = cursor.fetchone()

			cursor.execute(SQL_GET_VEICULO_ESPECIFICO, id_veiculo)
			veiculo = cursor.fetchone()

			cursor.execute(SQL_GET_AGENDAMENTO_ESPECIFICO, id_agendamento)
			agendamento = cursor.fetchone()

			if not cliente:
				mensagem = {
					'status': 404,
					'mensagem': 'Cliente não cadastrado!'
					}
				return jsonify(mensagem), 404
			
			elif not veiculo:
				conn.commit()
				mensagem = {
						'status': 404,
						'mensagem': 'Veiculo não cadastrado!'
					}
				return jsonify(mensagem), 404

			elif not agendamento:
				conn.commit()
				mensagem = {
						'status': 404,
						'mensagem': 'Não existe agendamento cadastrado!'
					}
				return jsonify(mensagem), 404

			cursor.execute(SQL_POST_VENDAS, dados)
			cursor.execute(SQL_UPDATE_AGENDAMENTO_CONCLUSAO, id_agendamento)
			conn.commit()
			mensagem = {
				'status': 200,
				'mensagem': 'Venda realizada com sucesso!'
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

@app.route('/vendas', methods=['PUT'])
@auth.login_required
def atualizar_vendas():
	try:
		json = request.json
		id_venda = json['ID']
		venda = json['Venda']
		preco = json['preco']
		id_cliente = json['ID cliente']
		id_veiculo = json['ID veiculo']
		id_agendamento = json['ID agendamento']
		if venda and preco and id_cliente and id_veiculo and id_agendamento and request.method == 'PUT':
			dados = (venda, preco, id_cliente, id_veiculo, id_agendamento, id_venda)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)

			cursor.execute(SQL_GET_VENDA_PUT, id_venda)
			venda = cursor.fetchone()

			cursor.execute(SQL_GET_CLIENTE_ESPECIFICO, id_cliente)
			cliente = cursor.fetchone()

			cursor.execute(SQL_GET_VEICULO_ESPECIFICO, id_veiculo)
			veiculo = cursor.fetchone()

			cursor.execute(SQL_GET_AGENDAMENTO_ESPECIFICO, id_agendamento)
			agendamento = cursor.fetchone()

			if not cliente:
				mensagem = {
					'status': 404,
					'mensagem': 'Cliente não cadastrado!'
					}
				return jsonify(mensagem), 404
			
			elif not venda:
				conn.commit()
				mensagem = {
						'status': 404,
						'mensagem': 'Venda não cadastrado!'
					}
				return jsonify(mensagem), 404

			elif not veiculo:
				conn.commit()
				mensagem = {
						'status': 404,
						'mensagem': 'Veiculo não cadastrado!'
					}
				return jsonify(mensagem), 404

			elif not agendamento:
				conn.commit()
				mensagem = {
						'status': 404,
						'mensagem': 'Não existe agendamento cadastrado!'
					}
				return jsonify(mensagem), 404

			cursor.execute(SQL_PUT_VENDAS, dados)
			conn.commit()
			mensagem = {
				'status': 200,
				'mensagem': 'Venda atualizada com sucesso!'
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

SQL_PUT_VENDAS = "UPDATE vendas SET data_venda = %s, preco = %s, id_clientes_FK = %s, id_veiculo_FK = %s, id_agendamento_FK = %s WHERE id_vendas_PK = %s"
SQL_GET_VENDAS = "select vendas.id_vendas_PK as ID,date_format(vendas.data_venda, GET_FORMAT(DATE,'EUR')) as 'Venda',vendas.preco as preco,veiculos.tipo as tipo,veiculos.veiculo as veiculo,veiculos.cor as cor,horario_agendamento as 'horario',clientes.nome as cliente from vendas inner join clientes on id_vendas_PK = id_clientes_PK inner join veiculos on id_veiculos_PK = id_clientes_PK inner join agendamentos on agendamentos.id_agendamento_PK = clientes.id_clientes_PK order by id_vendas_PK"
SQL_GET_VENDA_PUT = "select * from vendas where id_vendas_PK = %s"
SQL_GET_VENDAS_ESPECIFICO_NOME = "select vendas.id_vendas_PK as ID,date_format( vendas.data_venda, GET_FORMAT(DATE,'EUR')) as 'Venda',vendas.preco as preco,veiculos.tipo as tipo,veiculos.veiculo as veiculo,veiculos.cor as cor,horario_agendamento as 'horario',clientes.nome as cliente from vendas inner join clientes on id_vendas_PK = id_clientes_PK inner join veiculos on id_veiculos_PK = id_clientes_PK inner join agendamentos on agendamentos.id_agendamento_PK = clientes.id_clientes_PK where clientes.nome like %s %s order by id_vendas_PK"
SQL_GET_CLIENTE_ESPECIFICO = "select * from clientes where id_clientes_PK = %s"
SQL_GET_VEICULO_ESPECIFICO = "select * from veiculos where id_veiculos_PK = %s"
SQL_GET_AGENDAMENTO_ESPECIFICO = "select * from agendamentos where id_agendamento_PK = %s"
SQL_UPDATE_AGENDAMENTO_CONCLUSAO = "UPDATE agendamentos SET concluido = 'sim' WHERE id_agendamento_PK = %s"
SQL_POST_VENDAS = "insert into vendas (id_vendas_PK,data_venda, preco, id_clientes_FK, id_veiculo_FK, id_agendamento_FK) VALUES (default, %s, %s, %s, %s, %s)"

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
    app.run(debug=True, port=5006)