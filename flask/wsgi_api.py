from main_api import app
from flask_restx import Api

if __name__ == "__main__":
    api = Api(app)
    app.run()
