from flask import Flask,render_template

from app.models import db


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "my-secret-key"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"),404

    return app

