from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.views import View

'''
django内置的登录验证必须让开发者使用django内置的User模块，这会让开发者再某些方面被限制住
下面的模块是我自己自定义实现的django验证，使用方式和django的一样
'''


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


def login(request, user):
    request.session['login'] = user.id


def logout(request):
    request.session.flush()


def login_required(func):
    """
    对需要登录的视图函数进行验证
    @login_required
    def your_view(request, *args, **kwargs):
        ''''''
    """

    def wrapper(*args, **kwargs):
        request = args[0]
        is_login = request.session.get('login')

        if not is_login:
            redirect_url = '%s?next=%s' % (settings.LOGIN_URL, request.path)
            return redirect(redirect_url)
        else:
            result = func(*args, **kwargs)
            return result

    return wrapper


class LoginRequired(View):
    """
    对需要登录的类视图进行验证
    class YouView(LoginRequired):
        ''''''
    """

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequired, cls).as_view()
        return login_required(view)
