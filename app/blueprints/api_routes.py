from flask import Blueprint

from app.services.user_services import search_users_by_username_part


bp = Blueprint('api_routes', __name__, url_prefix='/api')


@bp.route('/search/<string:username_part>')
def searching(username_part: str):
    '''Подбирает доступных пользователей по части их имени
    (поиск пользователя по имени на главной странице)'''

    return search_users_by_username_part(username_part=username_part)


