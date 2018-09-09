from flask import Flask
from gene.gene import gene_bp
from disease.disease import disease_bp
from symptom.symptom import symptom_bp
from common.common import common_bp
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(gene_bp, url_prefix='/gene')
app.register_blueprint(symptom_bp, url_prefix='/symptom')
app.register_blueprint(disease_bp, url_prefix='/disease')
app.register_blueprint(common_bp, url_prefix='/common')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
