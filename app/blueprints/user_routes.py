from flask import render_template, Blueprint, redirect, url_for, g

from app.forms.forms import EditUsernameForm
from app.services.user_services import change_username


bp = Blueprint('user_routes', __name__, url_prefix='/me',
               template_folder='templates')


@bp.route('/account')
def user_account():
    '''Страница аккаунта пользователя'''

    return render_template('user/user_account.html')


@bp.route('/edit/username', methods=['GET', 'POST'])
def edit_username():
    '''Форма редактирования имени пользователя'''

    form = EditUsernameForm()

    if form.validate_on_submit():

        change_username(user_id=g.user.id,
                             new_username=form.new_username.data)
        
        return redirect(url_for('user_routes.user_account'))
    
    return render_template('user/edit_username_form.html', form=form)
