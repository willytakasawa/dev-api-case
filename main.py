import os
from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

#app = os.getenv("DEV")

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/db"
db = SQLAlchemy(app)

engine = create_engine("mysql+pymysql://root:@localhost/db")
if not database_exists(engine.url):
    create_database(engine.url)


'''Classe destinada ao endpoint de envio da solicitacao de agendamento pelo metodo POST
Deve-se criar um ID unico para cada solicitacao de agendamento'''
class Agendamento(db.Model):
    id_agendamento = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer)
    dt_envio = db.Column(db.DateTime)
    formato_comunicacao = db.Column(db.String(255))
    status_agendamento = db.Column(db.String(255))
    dt_ingestao = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %s>' % self.id_usuario

class EnvioAgendamento(Resource):
    def post(self):
        try:
            envio = Agendamento(
                id_agendamento = request.json["id_agendamento"],
                id_usuario = request.json["id_usuario"],
                dt_envio = request.json["dt_envio"],
                formato_comunicacao = request.json["formato_comunicacao"],
                status_agendamento = request.json["status_agendamento"],
                dt_ingestao = datetime.now().strftime('%Y-%m-%d')
            )
            db.session.add(envio)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            return e

        
api.add_resource(EnvioAgendamento, "/envio")


'''Classe destinada ao endpoint para consulta do status da solicitacao de agendamento pelo metodo GET
A consulta deve ser feita passando o parametro ID'''
class Status(Resource):
    def get(self):
        return {}

api.add_resource(Status, "/status")

'''Classe destinada ao endpoint para cancelamento de solicitacao de agendamento pelo metodo POST.
Pode-se considerar o ID criado no envio da solicitacao'''
class Cancelamento(Resource):
    def post(self):
        return{}

api.add_resource(Cancelamento, "/cancelamento")

if __name__ == "__main__":
    app.run(debug=True)