import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from user.views import make_secret
from user.views import make_token

# Create your views here.
from user.models import UserProfile


def tokens(request):
    # http://127.0.0.1:8000/v1/tokens
    if request.method == 'POST':
        # 请求示例: {‘username’: ‘xxx’, ‘password’: ‘yyy’}
        # 响应示例:{‘code’: 200,‘username’: ‘asc’, ‘data’: {‘token’: ‘zdsadasd’}}

        json_str = request.body
        json_obj = json.loads(json_str.decode())
        # print(json_obj)

        username = json_obj['username']
        if not username:
            html = {'code':201,'error':'NO username'}
            return JsonResponse(html)

        password = json_obj['password']
        if not password:
            html = {'code':202,'error':'NO password'}
            return JsonResponse(html)

        user = UserProfile.objects.filter(username=username)
        # print(user[0].username,user[0].email,user[0].password)
        if user.count() == 0:
            html = {'code':203,'error':'用户名或密码错误'}
            return JsonResponse(html)

        password = make_secret(password)
        if user[0].password != password or user[0].username != username:
            html = {'code':203,'error':'用户名或密码错误'}
            return JsonResponse(html)

        # print(username,password)
        # 制作响应token
        token = make_token(username)

        return JsonResponse({'code': 200, 'username': username, 'data': {'token': str(token)}})
