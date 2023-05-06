from flask import render_template, Blueprint


bp = Blueprint('errors_routes', __name__, url_prefix='/error',
               template_folder='templates')


@bp.errorhandler(404)
def not_found(e):
    '''Хендлер 404 ошибки'''

    return render_template('errors/404.html')
