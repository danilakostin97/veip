import os
import datetime
import time
import json
from django.conf import settings
from django.shortcuts import render, redirect
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa
from django.template.context_processors import csrf
from django.contrib import auth

def index(request):
    return render(request, "login.html")
    ##HttpResponse("<h3> Hello ASU </h3>")
def newd(request):
    data = {"username": request.user.username,  }
    return render(request, "app.html", context=data)

def calculations(request):
    if request.user.is_authenticated:
        data = {"username": request.user.username, }
        return render(request,"calc.html", context=data)

def theory(request):
    if request.user.is_authenticated:
        data = {"username": request.user.username, }
        return render(request,"theory.html", context=data)

def history(request):
    if request.user.is_authenticated:
        number = [["1", "2"], ["2", "3"]]
        data = {"username": request.user.username,"number":number, }
        return render(request,"history.html", context=data)

def resset(request):
    args = {}
    args.update(csrf(request))
    rails = request.POST.get('rails', '')
    number = [["1", "2"], ["2", "3"]]
    number = json.dumps(number)
    data={"speed":rails, "number":number, }
    return render(request,"restest.html", context=data)

def fetch_pdf_resources(uri,rel):
    if settings.STATIC_URL and uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    elif settings.MEDIA_URL and uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    else:
        path = os.path.join(settings.STATIC_ROOT, uri)
    return path


def test(request):
    #auth.get_user(request).username
    if request.user.is_authenticated:
        #return redirect('/testpage')
        #path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")

        types = ["English", "German", "French", "Spanish", "Chinese"]
        data = {"username": request.user.username,"types":types,}
        return render(request, "test.html", context=data)
    else:
        return redirect('/auth/login')


def pdf(request):
    types = ["English", "German", "French", "Spanish", "Chinese"]
    path=fetch_pdf_resources
    data = {"username": request.user.username, "types": types, "path": path, }
    template = get_template('test.html')
    html = template.render(data)
    file = open('test.pdf', "w+b")
    pisaf = pisa.pisaDocument(html.encode('UTF-8'), dest=file,link_callback=fetch_pdf_resources)
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')

def res(request):
    if request.user.is_authenticated:
        now = datetime.datetime.now()
        dt=now.strftime("%d-%m-%Y %H:%M")
        data = {"username": request.user.username,"v1": dt,}
        return render(request, "result.html", context=data)
    else:
        return redirect('/auth/login')

def call(request):
    if request.user.is_authenticated:
        data = {"username": request.user.username, }
       # render(request, "result.html", context=data)
       # pyautogui.hotkey('ctrlleft', 'p')
        #time.sleep(2)
        #pyautogui.press('enter')
        #time.sleep(10)
        return render(request, "result.html", context=data)
    else:
        return redirect('/auth/login')

def change(request):
    #args = {}
    #args.update(csrf(request))
    #rails = request.POST.get('rails', '')
    #number = [["1", "2"], ["2", "3"]]
    #number = json.dumps(number)
    #data={"speed":rails, "number":number, }
    data = {"username": request.user.username, }
    return render(request,"change_data.html", context=data)