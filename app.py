from flask import Flask
from blueprints import blueprint


app = Flask(__name__)

app.register_blueprint(blueprint,url_prefix="/rating")

if __name__ == '__main__':
    app.run(debug = True)



@app.route('/')
def hello_world():
    return 'Home Page'
