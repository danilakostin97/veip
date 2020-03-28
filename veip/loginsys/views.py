from django.shortcuts import render, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import loader, Context
from django.http import HttpResponse

def login(request):
    #c = {"login_error": "",}
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/testpage/test')
        else:
            data = 'User not found'

            ce = {'login_error': data,}
           # args['login_error'] = "User not found"
            return render(request,"auth.html")
           # HttpResponse(t.render(ce,request),content_type= 'text/html')
            #t.render(ce)

    else:
        return render(request,"auth.html")
        #HttpResponse(t.render(c,request),content_type= 'text/html')
        # t.render(c)

def logout(request):
    auth.logout(request)
    return redirect('/testpage')


def checkauth(request):
    if request.user.is_authenticated:
        return redirect('/testpage/test')
    else:
        return redirect('/auth/login')
