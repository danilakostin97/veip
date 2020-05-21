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
from . import veip_params1
from string import digits
import psycopg2



def newd(request):
    data = {"username": request.user.username,  }
    return render(request, "app.html", context=data)

def getHistory():
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('''select * from "input"''')
    dataInput = []
    for row in cursor:
        inp=[]
        for i in range(0,17):
            inp.append(row[i])
        dataInput.append(inp)
    print(dataInput)
    return dataInput


def getDataFromCur(cursor):
    arr=[]
    for row in cursor:
        arr.append(row[0])
    return arr

def calculations(request):
    if request.user.is_authenticated:
        ### ПОДКЛЮЧЕНИЕ К БД ###

        conn = psycopg2.connect(dbname='veip', user='postgres',
                                password='postgres', host='localhost')
        cursor = conn.cursor()
        cursor.execute('''select "t(i)" from "TPS"''')
        tps=getDataFromCur(cursor) #list(cursor.fetchall())
        cursor.execute('''select "v(i)" from "VSP"''')
        vsp=getDataFromCur(cursor)
        cursor.execute('''select "name_spkh" from "SPKH"''')
        spkh=getDataFromCur(cursor)
        cursor.execute('''select "name_spkv" from "SPKV"''')
        spkv = getDataFromCur(cursor)
        cursor.execute('''select "name_ekip" from "EKIP"''')
        ekip = getDataFromCur(cursor)
        inputdata=getHistory()
        #test

        # inputdata=[["Vag","on","ed","et",5,6,7,8,9,10,11,12,13,"Готово"]]
        # inputdata.append(["Pri", "exal", "vag", "on",15,16,17,18,19,20,21,22,"60..90", "В работе"])
        #
        #inputdata=getHistory()
        data = {"username": request.user.username, "inputdata":inputdata, "tps":tps, "vsp":vsp, "spkh":spkh, "spkv":spkv, "ekip":ekip }
        return render(request,"calculations.html", context=data)

def theory(request):
    data = {"username": request.user.username, }
    return render(request, "theory.html", context=data)
    # if request.user.is_authenticated:
    #     data = {"username": request.user.username, }
    #     return render(request,"theory.html", context=data)

def history(request):
    if request.user.is_authenticated:
        # test
        # inputdata = [["Vag", "on", "ed", "et", 5, 6, 7, 8, 9, 10, 11, 12, 13, "Готово"]]
        # inputdata.append(["Pri", "exal", "vag", "on", 15, 16, 17, 18, 19, 20, 21, 22, "60..90", "В работе"])
        #
        inputdata=getHistory()
        data = {"username": request.user.username, "inputdata": inputdata, }
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


def getdata(arrres):
    p = arrset(0, arrres)
    onapr = arrset(2, arrres)
    y = arrset(4, arrres)
    q = arrset(6, arrres)
    ball = arrset(8, arrres)
    opzp = arrset(10, arrres)
    aksr = arrset(12, arrres)
    akss = arrset(14, arrres)
    aksb = arrset(16, arrres)
    vzs = arrset(18, arrres)
    data = { "p": p, "onapr": onapr, "y": y, "q": q, "ball": ball, "opzp": opzp,
            "aksr": aksr, "akss": akss, "aksb": aksb, "vzs": vzs}
    return data

def resset(request):

    args = {}
    args.update(csrf(request))
    if request.method =="POST":
        tps = request.POST.get('tps')
        vsp = request.POST.get('vsp')
        spkh = request.POST.get('spkh')
        spkv = request.POST.get('spkv')
        ekip = request.POST.get('ekip')
        rk = request.POST.get('rk')
        rmk = request.POST.get('rmk')
        voz = request.POST.get('voz')
        krip = request.POST.get('krip')
        gor = request.POST.get('gor')
        pol = request.POST.get('pol')
        ugl = request.POST.get('ugl')
        skrip = request.POST.get('skrip')
        speed = request.POST.get('speed')

    ### ПОДКЛЮЧЕНИЕ К БД ###

    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    print(request.POST)
    cursor.execute('''select "id" from "TPS" where "t(i)" ='%s';''' % tps)
    id_tps= cursor.fetchone()[0]
    cursor.execute('''select "id" from "VSP" where "v(i)" ='%s';''' % vsp)
    id_vsp = cursor.fetchone()[0]
    cursor.execute('''select "id" from "SPKH" where "name_spkh" ='%s';''' % spkh)
    id_spkh = cursor.fetchone()[0]
    cursor.execute('''select "id" from "SPKV" where "name_spkv" ='%s';''' % spkv)
    id_spkv = cursor.fetchone()[0]
    cursor.execute('''select "id" from "EKIP" where "name_ekip" ='%s';''' % ekip)
    id_ekip = cursor.fetchone()[0]
    print(id_tps)
    cursor.execute("""INSERT INTO "input" VALUES (default,%s,default,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING "id" """,
                    ( request.user.username, id_tps, id_vsp, id_spkh, id_spkv, id_ekip,rk,rmk,voz,krip,gor,pol,ugl,skrip,speed))

    print('DONEEEEEEEEEEEE')
    id_of_new_row = cursor.fetchone()[0]
    print(id_of_new_row)
    conn.commit()
    # staroe
    #

    params=veip_params1.cput()
    params.start(cursor, id_of_new_row)

    print('FINAL')
    # print(request.POST)
    # print(tps,vsp,spkh,spkv,rk,rmk,voz,krip,gor,pol,ugl,skrip,speed)
    # param = veip_params.cput()
    # arrres = param.putm()
    # data=getdata(arrres)

    p = [[1, 0.02, 0.03], [2, 0.201, 0.045], [3, 0.02556, 0.005], [4, 0.546, 0.02]]
    onapr = [[1, 0.2, 0.02], [2, 0.0201, 0.0045], [3, 0.56, 0.05], [4, 0.546, 0.02]]
    y = [[1, 0.211, 0.025], [2, 0.201, 0.045], [3, 0.67, 0.25], [4, 0.689, 0.2]]
    ball = [[1, 0.3, 0.03], [2, 0.31, 0.05], [3, 0.756, 0.163], [4, 0.946, 0.02]]
    opzp = [[1, 0.21, 0.02], [2, 0.201, 0.045], [3, 0.156, 0.0075], [4, 0.846, 0.12]]
    aksr = [[1, 0.72, 0.2], [2, 0.9201, 0.045], [3, 0.564, 0.05], [4, 0.526, 0.02]]
    akss = [[1, 0.2, 0.02], [2, 0.0201, 0.0045], [3, 0.56, 0.05], [4, 0.546, 0.02]]
    aksb = [[1, 0.211, 0.025], [2, 0.201, 0.045], [3, 0.67, 0.25], [4, 0.689, 0.2]]
    vzs = [[1, 0.21, 0.02], [2, 0.201, 0.045], [3, 0.156, 0.0075], [4, 0.846, 0.12]]
    q = [[1, 0.72, 0.2], [2, 0.9201, 0.045], [3, 0.564, 0.05], [4, 0.526, 0.02]]
    data = {"p": p, "onapr": onapr, "y": y, "q": q, "ball": ball,
            "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, "vzs": vzs}
    #data={"speed":rails, "list":list, "p":p, "onapr":onapr, "y":y, "q":q, "ball":ball, "opzp":opzp, "aksr":aksr, "akss":akss, "aksb":aksb, "vzs":vzs }
    # # render(request, "restest.html", context=data), context=data
    #data={"tps":tps, "vsp":vsp, "spkh":spkh, "spkv":spkv, "rk":rk, "rmk":rmk, "voz":voz, "krip":krip, "gor":gor, "pol":pol, "ugl":ugl, "skrip":skrip, "speed":speed}
    return render(request,"restest.html", context=data)

def createcalc(speed):

    param = veip_params.cput()
    arrres = param.putm()
    return arrres

def viewresult(request):
    # sql poisk rezultata
    s = request.POST.get('speed')
    remove_digits = str.maketrans('', '', digits)
    res = s.translate(remove_digits)
    if res:
        p = [[1, 0.02, 0.03, 60], [2, 0.201, 0.045, 60], [3, 0.02556, 0.005, 60], [4, 0.546, 0.02, 60]]
        onapr = [[1, 0.2, 0.02, 60], [2, 0.0201, 0.0045, 60], [3, 0.56, 0.05, 60], [4, 0.546, 0.02, 60]]
        y = [[1, 0.211, 0.025, 60], [2, 0.201, 0.045, 60], [3, 0.67, 0.25, 60], [4, 0.689, 0.2, 60]]
        ball = [[1, 0.3, 0.03, 60], [2, 0.31, 0.05, 60], [3, 0.756, 0.163, 60], [4, 0.946, 0.02, 60]]
        opzp = [[1, 0.21, 0.02, 60], [2, 0.201, 0.045, 60], [3, 0.156, 0.0075, 60], [4, 0.846, 0.12, 60]]
        aksr = [[1, 0.72, 0.2, 60], [2, 0.9201, 0.045, 60], [3, 0.564, 0.05, 60], [4, 0.526, 0.02, 60]]
        akss = [[1, 0.2, 0.02, 60], [2, 0.0201, 0.0045, 60], [3, 0.56, 0.05, 60], [4, 0.546, 0.02, 60]]
        aksb = [[1, 0.211, 0.025, 60], [2, 0.201, 0.045, 60], [3, 0.67, 0.25, 60], [4, 0.689, 0.2, 60]]
        vzs = [[1, 0.21, 0.02, 60], [2, 0.201, 0.045, 60], [3, 0.156, 0.0075, 60], [4, 0.846, 0.12, 60]]
        q = [[1, 0.72, 0.2, 60], [2, 0.9201, 0.045, 60], [3, 0.564, 0.05, 60], [4, 0.526, 0.02, 60]]
        datasolo = {"p": p, "onapr": onapr, "y": y, "q": q, "ball": ball,
                "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, "vzs": vzs}
        return render(request,"multires.html", context=datasolo)
    else:
        print(res)
        p = [[1, 0.02, 0.03], [2, 0.201, 0.045], [3, 0.02556, 0.005], [4, 0.546, 0.02]]
        onapr = [[1, 0.2, 0.02], [2, 0.0201, 0.0045], [3, 0.56, 0.05], [4, 0.546, 0.02]]
        y = [[1, 0.211, 0.025], [2, 0.201, 0.045], [3, 0.67, 0.25], [4, 0.689, 0.2]]
        ball = [[1, 0.3, 0.03], [2, 0.31, 0.05], [3, 0.756, 0.163], [4, 0.946, 0.02]]
        opzp = [[1, 0.21, 0.02], [2, 0.201, 0.045], [3, 0.156, 0.0075], [4, 0.846, 0.12]]
        aksr = [[1, 0.72, 0.2], [2, 0.9201, 0.045], [3, 0.564, 0.05], [4, 0.526, 0.02]]
        akss = [[1, 0.2, 0.02], [2, 0.0201, 0.0045], [3, 0.56, 0.05], [4, 0.546, 0.02]]
        aksb = [[1, 0.211, 0.025], [2, 0.201, 0.045], [3, 0.67, 0.25], [4, 0.689, 0.2]]
        vzs = [[1, 0.21, 0.02], [2, 0.201, 0.045], [3, 0.156, 0.0075], [4, 0.846, 0.12]]
        q = [[1, 0.72, 0.2], [2, 0.9201, 0.045], [3, 0.564, 0.05], [4, 0.526, 0.02]]
        data = {"p": p, "onapr": onapr, "y": y, "q": q, "ball": ball,
                "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, "vzs": vzs}
        return render(request,"restest.html", context=data)

def getDataMult(res1,res2,res3,res4,res5):
    resAll=[[]]
    p = []
    onapr = []
    y = []
    q = []
    ball = []
    opzp = []
    aksr = []
    akss = []
    aksb = []
    vzs = []
    resAll.append(res1)
    resAll.append(res2)
    resAll.append(res3)
    resAll.append(res4)
    resAll.append(res5)
    x=0
    for i in range(1,6):
        p.append(arrset(0+x, resAll))
        onapr.append(arrset(2+x, resAll))
        y.append(arrset(4+x, resAll))
        q.append(arrset(6+x, resAll))
        ball.append(arrset(8+x, resAll))
        opzp.append(arrset(10+x, resAll))
        aksr.append(arrset(12+x, resAll))
        akss.append(arrset(14+x, resAll))
        aksb.append(arrset(16+x, resAll))
        vzs.append(arrset(18+x, resAll))
        x=x+20
    data = { "p": p, "onapr": onapr, "y": y, "q": q, "ball": ball, "opzp": opzp,
            "aksr": aksr, "akss": akss, "aksb": aksb, "vzs": vzs}
    return data

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
        speedl = request.POST.get('speedl')
        speedh = request.POST.get('speedh')
    #vstavka zaneseniya v bd

    resSpeed1=createcalc(speedl)
    resSpeed2 = createcalc(round((round((speedl+speedh)/2)+speedl)/2))
    resSpeed3 = createcalc(round((speedl+speedh)/2))
    resSpeed4 = createcalc(round((round((speedl+speedh)/2)+speedh)/2))
    resSpeed5 = createcalc(speedh)

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

