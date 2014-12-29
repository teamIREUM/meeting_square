from flask import Blueprint

def setup(app):
    global bp
    bp = Blueprint('user',__name__,
            template_folder='templates')

    import views
    app.register_blueprint(bp,url_prefix='/user')
