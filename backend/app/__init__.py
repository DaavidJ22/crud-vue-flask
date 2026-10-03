import os

from dotenv import load_dotenv
from flask import Flask

from . import models  # noqa: F401
from .api import api_bp
from .extensions import cors, db, migrate


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "cambiar-esta-clave"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///app.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
            }
        },
    )

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
