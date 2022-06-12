from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from datetime import datetime


#Argumentos da requisicao para INSERCAO
agendamento_post_args = reqparse.RequestParser()
agendamento_post_args.add_argument("id_agendamento", type=int, help="Campo id_agendamento deve ser preenchido", required=True)
agendamento_post_args.add_argument("id_usuario", type=int, help="Campo id_usuario deve ser preenchido", required=True)
agendamento_post_args.add_argument("dt_envio", type=str, help="Campo dt_envio deve ser preenchido", required=True)
agendamento_post_args.add_argument("formato_comunicacao", type=str, help="Campo formato_comunicacao deve ser preenchido", required=True)

#Argumento da requisicao para UPDATE
agendamento_update_args = reqparse.RequestParser()
agendamento_update_args.add_argument("status_agendamento", type=str, help="Campo status_agendamento deve ser preenchido", required=True)


fields = {
	'id_agendamento': fields.Integer,
	'id_usuario': fields.Integer,
	'dt_envio': fields.DateTime,
	'formato_comunicacao': fields.String,
    'status_agendamento': fields.String,
    'dt_atualizacao': fields.DateTime
}

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

engine = create_engine("mysql+pymysql://root:@localhost/db")
if not database_exists(engine.url):
    create_database(engine.url)


'''Classe destinada a criacao da tabela agendamento no db com schema definido'''
class Agendamento(db.Model):
    id_agendamento = db.Column(db.Integer, primary_key=True, autoincrement=False)
    id_usuario = db.Column(db.Integer, nullable=False)
    dt_envio = db.Column(db.DateTime, nullable=False)
    formato_comunicacao = db.Column(db.String(255), nullable=False)
    status_agendamento = db.Column(db.String(255))
    dt_atualizacao = db.Column(db.DateTime)

db.create_all()


'''Classe destinada ao endpoint de envio da solicitacao de agendamento pelo metodo POST
Deve-se criar um ID unico para cada solicitacao de agendamento'''
class EnvioAgendamento(Resource):
    @marshal_with(fields)
    def post(self):
        args = agendamento_post_args.parse_args()
        query = Agendamento.query.filter_by(id_agendamento=args['id_agendamento']).first()
        if query:
            abort(409, message="ID_AGENDAMENTO JA EXISTENTE")
        envio = Agendamento(
            id_agendamento=args['id_agendamento'],
            id_usuario=args['id_usuario'], 
            dt_envio=args['dt_envio'], 
            formato_comunicacao=args['formato_comunicacao'].lower(), 
            status_agendamento='agendado',
            dt_atualizacao=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(envio)
        db.session.commit()
        return envio, 200
        
api.add_resource(EnvioAgendamento, "/agendamento")


'''Classe destinada ao endpoint para consulta do status da solicitacao de agendamento pelo metodo GET
A consulta deve ser feita utilizando o parametro ID'''
class Status(Resource):
    @marshal_with(fields)
    def get(self, id_agendamento):
        result = Agendamento.query.filter_by(id_agendamento=id_agendamento).first()
        if not result:
            abort(404, message="id_agendamento inexistente...")
        return result

api.add_resource(Status, "/status/<int:id_agendamento>")

'''Classe destinada ao endpoint para cancelamento de solicitacao de agendamento pelo metodo PATCH.
Deve-se considerar o id_agendamento criado no envio da solicitacao e passar no body um novo status de agendamento'''
class Cancelamento(Resource):
    @marshal_with(fields)
    def patch(self, id_agendamento):
        args = agendamento_update_args.parse_args()
        result = Agendamento.query.filter_by(id_agendamento=id_agendamento).first()
        if not result:
            abort(404, message="id_agendamento inexistente...")
        if result:
            if args['status_agendamento']:
                result.status_agendamento = args['status_agendamento']
                result.dt_atualizacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                db.session.commit()

        return result

api.add_resource(Cancelamento, "/cancelamento/<int:id_agendamento>")

if __name__ == "__main__":
    app.run(debug=True)