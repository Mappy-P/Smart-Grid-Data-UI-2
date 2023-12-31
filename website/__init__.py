from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
# DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.secret_key="anystringhere_ZUIGMIJNLULRAFAEL"
    @app.errorhandler(404) 
    def not_found(e): 
        return render_template("404.html") 
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')
    #app.register_blueprint(auth, url_prefix='/')

    # from .models import User, Note

    # with app.app_context():
    #     db.create_all()

    return app
