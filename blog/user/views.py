import hmac
import json
import time

import jwt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
from user.models import UserProfile


def users(request,username=None):
    #注册接口:URL : http://127.0.0.1:8000/v1/users
    if request.method == 'POST':

        #接收请求
        # 请求形式:{‘username’: jack, ‘email’: ‘abc@qq.com’, ‘password1’: ‘abcdef’,
        # ‘password2’: ‘abcdef’}
        # 响应格式:{‘code’:200,‘username’:‘abc’,’data’:{‘token’:‘asdadasd.cvreijvd.dasdadad’}}
        json_str = request.body
        json_obj = json.loads(json_str.decode())
        # print(json_obj,type(json_obj))

        username = json_obj['username']
        # print(username)
        if not username:
            html = {'code':'101','error':'没有用户名'}
            return JsonResponse(html)


        email = json_obj['email']
        if not email:
            html = {'code':'102','error':'No email'}
            return JsonResponse(html)

        password1 = json_obj['password_1']
        if not password1:
            html = {'code':'103','error':'NO password'}
            return JsonResponse(html)

        password2 = json_obj['password_2']
        if not password2:
            html = {'code':'104','error':'NO password'}
            return JsonResponse(html)

        if password1 != password2:
            html = {'code':'105','error':'not the same password'}
            return JsonResponse(html)

        #加密密码
        password = make_secret(password1)
        # print(password)

        #入库操作
        user = UserProfile.objects.create(
            username = username,
            email= email,
            password = password
        )
        user.save()

        #制作响应token
        token = make_token(username)
        # print(token)
        # raise
        html = {'code':'200','username':username,
                'data':{
                    'token':token.decode()
                }}
        return JsonResponse(html)



    elif request.method == 'GET':
        #注册接口:http://127.0.0.1:8000/v1/users/<username>
        # 请求格式:http://127.0.0.1:8000/v1/users/<username>?nickname=1
        # 响应格式:
        print('收到请求了')
        print(username)
        if username:
            users = UserProfile.objects.filter(username=username)
            print(users)
        return JsonResponse({'code':200,'data':'这是get请求'})

# 密码加密
def make_secret(password):
    key = b'peezh'
    if not isinstance(password,bytes):
        password = password.encode()
    secret_password = hmac.new(key,password,digestmod='SHA1')
    return secret_password.hexdigest()

# 制作响应token
def make_token(username):
    key = b'peezh'
    payload = {'exp':int(time.time()+500)}
    payload['username'] = username
    return  jwt.encode(payload,key,algorithm='HS256')