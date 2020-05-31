from django.shortcuts import render, redirect
from django.contrib import auth
from django.template.context_processors import csrf
def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/testpage/calculations')
        else:
            data = 'User not found'

            ce = {'login_error': data,}
            return render(request,"auth.html")

    else:
        return render(request,"auth.html")

def logout(request):
    auth.logout(request)
    return redirect('/')


def checkauth(request):
    if request.user.is_authenticated:
        return redirect('/testpage/calculations')
    else:
        return redirect('/testpage/theory')
