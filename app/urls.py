from flask import Blueprint
from app.auth import view as auth_view
from app.posts import view as posts_view
from app.users import view as users_view


blueprint = Blueprint('bp', __name__)



# auth URLs
AUTH_PREFIX = '/auth'
blueprint.add_url_rule(AUTH_PREFIX + '/register', view_func=auth_view.RegisterUser.as_view('register_user'))
blueprint.add_url_rule(AUTH_PREFIX + '/login', view_func=auth_view.LoginUser.as_view('login_user'))
blueprint.add_url_rule(AUTH_PREFIX + '/update', view_func=auth_view.UpdateUser.as_view('update_user'))
blueprint.add_url_rule(AUTH_PREFIX + '/logout', view_func=auth_view.LogoutUser.as_view('logout_user'))
blueprint.add_url_rule(AUTH_PREFIX + '/reset', view_func=auth_view.ResetPassword.as_view('reset_password'))
blueprint.add_url_rule(AUTH_PREFIX + '/check_reset_token', view_func=auth_view.CheckResetToken.as_view('check_reset_token'))
blueprint.add_url_rule(AUTH_PREFIX + '/deactivate/<int:user_id>', view_func=auth_view.DeleteUser.as_view('deactivate_user'))

# posts URLs
POSTS_PREFIX = '/posts'
blueprint.add_url_rule(POSTS_PREFIX + '/home/<int:page>', view_func=posts_view.PostList.as_view('posts_list'))
blueprint.add_url_rule(POSTS_PREFIX + '/create',view_func=posts_view.CreatePost.as_view('create_post'))
blueprint.add_url_rule(POSTS_PREFIX + '/delete/<int:post_id>', view_func=posts_view.DeletePost.as_view('delete_post'))
blueprint.add_url_rule(POSTS_PREFIX + '/update/<int:post_id>', view_func=posts_view.UpdatePost.as_view('update_post'))
blueprint.add_url_rule(POSTS_PREFIX + '/detail/<int:post_id>', view_func=posts_view.PostDetail.as_view('post_detail'))
blueprint.add_url_rule(POSTS_PREFIX + '/react/', view_func=posts_view.ReactPost.as_view('react_post'))
blueprint.add_url_rule('/', view_func=posts_view.Home.as_view('start'))

#users URLs
USERS_PREFIX = '/users'
blueprint.add_url_rule(USERS_PREFIX + '/profile', view_func=users_view.Profile.as_view('profile'))