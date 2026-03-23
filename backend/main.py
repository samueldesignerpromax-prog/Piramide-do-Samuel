import os
import sys

from flask import Flask
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api import api_bp, webhook_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False
    CORS(app)

    app.register_blueprint(api_bp)
    app.register_blueprint(webhook_bp)

    @app.get("/")
    def root():
        return {
            "ok": True,
            "message": "API Afiliados Vendas online"
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
