import os
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa
from django.template.context_processors import csrf
from . import veip_params

def newd(request):
    data = {"username": request.user.username,  }
    return render(request, "app.html", context=data)

def calculations(request):
    if request.user.is_authenticated:
        inputdata=[["Vag","on","ed","et",5,6,7,8,9,10,11,12,13,"Готово"]]
        inputdata.append(["Pri", "exal", "vag", "on",15,16,17,18,19,20,21,22,"60..90", "В работе"])
        data = {"username": request.user.username, "inputdata":inputdata, }
        return render(request,"calculations.html", context=data)

def theory(request):
    if request.user.is_authenticated:
        data = {"username": request.user.username, }
        return render(request,"theory.html", context=data)

def history(request):
    if request.user.is_authenticated:
        number = [["1", "2"], ["2", "3"]]
        data = {"username": request.user.username,"number":number, }
        return render(request,"history.html", context=data)

def arrset(k,par):
    arr=[]
    i=0
    while i<4:
        mas=[]
        mas.append(i+1)
        mas.append(par[k][i])
        mas.append(par[k+1][i])
        arr.append(mas)
        i+=1
    return arr

def resset(request):

    args = {}
    args.update(csrf(request))
    if request.method =="POST":
        tps = request.POST.get('tps')
        vsp = request.POST.get('vsp')
        spkh = request.POST.get('spkh')
        spkv = request.POST.get('spkv')
        rk = request.POST.get('rk')
        rmk = request.POST.get('rmk')
        voz = request.POST.get('voz')
        krip = request.POST.get('krip')
        gor = request.POST.get('gor')
        pol = request.POST.get('pol')
        ugl = request.POST.get('ugl')
        skrip = request.POST.get('skrip')
        speed = request.POST.get('speed')
    print(request.POST)
    print(tps,vsp,spkh,spkv,rk,rmk,voz,krip,gor,pol,ugl,skrip,speed)
    # rails = request.POST.get('rails', '')
    # param = veip_params.cput()
    # arrres = param.putm()
    # number = [["1", "2"], ["2", "3"]]
    # number = json.dumps(number)
    # print(arrres[0])
    # p=arrset(0,arrres)
    # print("done")
    # onapr=arrset(2,arrres)
    # print("done")
    # y=arrset(4,arrres)
    # print("done")
    # q=arrset(6,arrres)
    # print("done")
    # ball=arrset(8,arrres)
    # print("done")
    # opzp=arrset(10,arrres)
    # print("done")
    # aksr=arrset(12,arrres)
    # print("done")
    # akss=arrset(14,arrres)
    # print("done")
    # aksb=arrset(16,arrres)
    # print("done")
    # vzs=arrset(18,arrres)
    # print("done")
    # data={"speed":rails, "number":number, "list":list, "p":p, "onapr":onapr, "y":y, "q":q, "ball":ball, "opzp":opzp, "aksr":aksr, "akss":akss, "aksb":aksb, "vzs":vzs }
    # # render(request, "restest.html", context=data), context=data
    data={"tps":tps, "vsp":vsp, "spkh":spkh, "spkv":spkv, "rk":rk, "rmk":rmk, "voz":voz, "krip":krip, "gor":gor, "pol":pol, "ugl":ugl, "skrip":skrip, "speed":speed}
    return render(request,"restest.html", context=data)



def multires(request):
    args = {}
    args.update(csrf(request))
    if request.method =="POST":
        tps = request.POST.get('tps')
        vsp = request.POST.get('vsp')
        spkh = request.POST.get('spkh')
        spkv = request.POST.get('spkv')
        rk = request.POST.get('rk')
        rmk = request.POST.get('rmk')
        voz = request.POST.get('voz')
        krip = request.POST.get('krip')
        gor = request.POST.get('gor')
        pol = request.POST.get('pol')
        ugl = request.POST.get('ugl')
        skrip = request.POST.get('skrip')
        speed = request.POST.get('speed')
    print(request.POST)
    rails = request.POST.get('rails', '')
    number = [1, 2]
    list = ["p", "onapr", "y", "q", "ball", "opzp", "aksr", "akss", "aksb", "vzs"]
    p = [[1, 0.02, 0.03,60], [2, 0.201, 0.045,60], [3, 0.02556, 0.005,60], [4, 0.546, 0.02,60]]
    onapr = [[1, 0.2, 0.02,60], [2, 0.0201, 0.0045,60], [3, 0.56, 0.05,60], [4, 0.546, 0.02,60]]
    y = [[1, 0.211, 0.025,60], [2, 0.201, 0.045,60], [3, 0.67, 0.25,60], [4, 0.689, 0.2,60]]
    ball = [[1, 0.3, 0.03,60], [2, 0.31, 0.05,60], [3, 0.756, 0.163,60], [4, 0.946, 0.02,60]]
    opzp = [[1, 0.21, 0.02,60], [2, 0.201, 0.045,60], [3, 0.156, 0.0075,60], [4, 0.846, 0.12,60]]
    aksr = [[1, 0.72, 0.2,60], [2, 0.9201, 0.045,60], [3, 0.564, 0.05,60], [4, 0.526, 0.02,60]]
    akss = [[1, 0.2, 0.02,60], [2, 0.0201, 0.0045,60], [3, 0.56, 0.05,60], [4, 0.546, 0.02,60]]
    aksb = [[1, 0.211, 0.025,60], [2, 0.201, 0.045,60], [3, 0.67, 0.25,60], [4, 0.689, 0.2,60]]
    vzs = [[1, 0.21, 0.02,60], [2, 0.201, 0.045,60], [3, 0.156, 0.0075,60], [4, 0.846, 0.12,60]]
    q = [[1, 0.72, 0.2,60], [2, 0.9201, 0.045,60], [3, 0.564, 0.05,60], [4, 0.526, 0.02,60]]
    number = json.dumps(number)
    data = {"speed": rails, "number": number, "list": list, "p": p, "onapr": onapr, "y": y, "q": q, "ball": ball,
            "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, "vzs": vzs}
    return render(request,"multires.html",  context=data)

def fetch_pdf_resources(uri,rel):
    if settings.STATIC_URL and uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    elif settings.MEDIA_URL and uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    else:
        path = os.path.join(settings.STATIC_ROOT, uri)
    return path


def test(request):
    if request.user.is_authenticated:
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
        return render(request, "result.html", context=data)
    else:
        return redirect('/auth/login')

def change(request):

    data = {"username": request.user.username, }
    return render(request,"change_data.html", context=data)