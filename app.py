from flask import Flask
from flask_restful import Api
from config import Config
from models import db
from resources import InfrastructureResource, InfrastructureSearchResource

app = Flask(__name__)
app.json.ensure_ascii = False
app.json.mimetype = "application/json; charset=utf-8"
app.config.from_object(Config)
api = Api(app)

db.init_app(app)

with app.app_context():
    db.create_all()

api.add_resource(InfrastructureResource, '/infrastructure',
                 '/infrastructure/<int:id>')
api.add_resource(InfrastructureSearchResource,
                 '/infrastructure/search')

if __name__ == '__main__':
    app.run(debug=True)