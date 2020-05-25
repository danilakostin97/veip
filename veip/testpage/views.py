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
import random



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
        inp.append(row[17])
        inp.append(0)
        dataInput.append(inp)
    cursor.execute('''select * from (select t1."parent_id", max(t1."cl(9)"), min(t2."cl(9)") from (select * from "input" where "parent_id">0) t1
left join (select * from "input" where "parent_id"=0) t2 on t1."parent_id"=t2."id" group by t1.parent_id) tspeed left join  "input" on input.id=tspeed.parent_id;''')
    for row in cursor:
        inp=[]
        for i in range(3,19):
            inp.append(row[i])
        speedmin=str(row[2])+'-'+str(row[1])
        inp.append(speedmin)
        inp.append(row[1])
        inp.append(row[2])
        dataInput.append(inp)
    return dataInput


def getDataFromCur(cursor):
    arr=[]
    for row in cursor:
        arr.append(row[0])
    return arr

def findRes(tps, vsp, spkh, spkv, ekip,rk,rmk,voz,krip,gor,pol,ugl,skrip,speed):
    data={}
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('''select "id" from "TPS" where "t(i)" ='%s';''' % tps)
    id_tps = cursor.fetchone()[0]
    cursor.execute('''select "id" from "VSP" where "v(i)" ='%s';''' % vsp)
    id_vsp = cursor.fetchone()[0]
    cursor.execute('''select "id" from "SPKH" where "name_spkh" ='%s';''' % spkh)
    id_spkh = cursor.fetchone()[0]
    cursor.execute('''select "id" from "SPKV" where "name_spkv" ='%s';''' % spkv)
    id_spkv = cursor.fetchone()[0]
    cursor.execute('''select "id" from "EKIP" where "name_ekip" ='%s';''' % ekip)
    id_ekip = cursor.fetchone()[0]
    cursor.execute('''select "id" from "input" where "id_TPS"=%(id_tps)s and "id_VSP"=%(id_vsp)s and "id_SPKH"=%(id_spkh)s and "id_SPKV"=%(id_spkv)s 
            and "id_EKIP"=%(id_ekip)s and "cl(1)"=%(rk)s and "cl(2)"=%(rmk)s and "cl(3)"=%(voz)s and "cl(4)"=%(krip)s and "cl(5)"=%(gor)s and "cl(6)"=%(pol)s 
            and "cl(7)"=%(ugl)s and "cl(8)"=%(skrip)s and "cl(9)"=%(speed)s;
    ''', {'id_tps': id_tps, 'id_vsp': id_vsp, 'id_spkh': id_spkh, 'id_spkv': id_spkv, 'id_ekip': id_ekip, 'rk': rk,
          'rmk': rmk, 'voz': voz,
          'krip': krip, 'gor': gor, 'pol': pol, 'ugl': ugl, 'skrip': skrip, 'speed': speed})
    #print(cursor.rowcount)
    if cursor.rowcount > 0:
        id_of_new_row = cursor.fetchone()[0]
        cursor.execute(
            '''select * from "result" where id_input=%(id_input)s;''',
            { 'id_input': id_of_new_row})
        if cursor.rowcount>0:
            p = getRes('p', id_of_new_row)
            onapr = getRes('onapr', id_of_new_row)
            y = getRes('y', id_of_new_row)
            ball = getRes('ball', id_of_new_row)
            opzp = getRes('opzp', id_of_new_row)
            aksr = getRes('aksr', id_of_new_row)
            akss = getRes('akss', id_of_new_row)
            aksb = getRes('aksb', id_of_new_row)
            vzs = getRes('vzs', id_of_new_row)
            q = getRes('q', id_of_new_row)
            data = {"p": p, "onapr": onapr, "y": y, "q": q, "ball": ball,
                    "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, "vzs": vzs}

    return data

def parseData(data,param, id_input):
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    for row in data[param]:
        number_axis=row[0]
        expected_value=row[1]
        cko=row[2]
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO "result" VALUES (default,%s,%s,%s,%s,%s) """,
            (id_input, param, number_axis, expected_value, cko))
        conn.commit()
    return 1

def calculations(request):
    if request.user.is_authenticated:
        ### ПОДКЛЮЧЕНИЕ К БД ###

        conn = psycopg2.connect(dbname='veip', user='postgres',
                                password='postgres', host='localhost')
        cursor = conn.cursor()
        cursor.execute('''select "t(i)" from "TPS"''')
        tps=getDataFromCur(cursor)
        cursor.execute('''select "v(i)" from "VSP"''')
        vsp=getDataFromCur(cursor)
        cursor.execute('''select "name_spkh" from "SPKH"''')
        spkh=getDataFromCur(cursor)
        cursor.execute('''select "name_spkv" from "SPKV"''')
        spkv = getDataFromCur(cursor)
        cursor.execute('''select "name_ekip" from "EKIP"''')
        ekip = getDataFromCur(cursor)
        inputdata=getHistory()
        data = {"username": request.user.username, "inputdata":inputdata, "tps":tps, "vsp":vsp, "spkh":spkh, "spkv":spkv, "ekip":ekip }
        # test = [[1, 0.02, 0.03, 60], [2, 0.201, 0.045, 60], [3, 0.02556, 0.005, 60], [4, 0.546, 0.02, 60]]
        # test2=[[5, 0.02, 0.03, 60], [6, 0.201, 0.045, 60], [7, 0.02556, 0.005, 60], [8, 0.546, 0.02, 60]]
        # data2={'test':test, 'test2':test2}
        # value='test'
        # print(data2[value])
        # for row in data2[value]:
        #     print(row[0])
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

def setInput(user_name, tps, vsp, spkh, spkv, ekip,rk,rmk,voz,krip,gor,pol,ugl,skrip,speed, parent_id):

    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('''select "id" from "TPS" where "t(i)" ='%s';''' % tps)
    id_tps = cursor.fetchone()[0]
    cursor.execute('''select "id" from "VSP" where "v(i)" ='%s';''' % vsp)
    id_vsp = cursor.fetchone()[0]
    cursor.execute('''select "id" from "SPKH" where "name_spkh" ='%s';''' % spkh)
    id_spkh = cursor.fetchone()[0]
    cursor.execute('''select "id" from "SPKV" where "name_spkv" ='%s';''' % spkv)
    id_spkv = cursor.fetchone()[0]
    cursor.execute('''select "id" from "EKIP" where "name_ekip" ='%s';''' % ekip)
    id_ekip = cursor.fetchone()[0]
    print(id_tps)
    cursor.execute(
        """INSERT INTO "input" VALUES (default,%s,default,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING "id" """,
        (user_name, id_tps, id_vsp, id_spkh, id_spkv, id_ekip, rk, rmk, voz, krip, gor, pol, ugl, skrip,
         speed, parent_id))

    id_of_new_row = cursor.fetchone()[0]
    print(id_of_new_row)
    conn.commit()
    return id_of_new_row

#sozdat raschet
def setCalc(user_name, tps, vsp, spkh, spkv, ekip,rk,rmk,voz,krip,gor,pol,ugl,skrip,speed, parent_id):

    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    id_of_new_row =setInput(user_name, tps, vsp, spkh, spkv, ekip,rk,rmk,voz,krip,gor,pol,ugl,skrip,speed, parent_id)
    params = veip_params1.cput()
    params.start(cursor, id_of_new_row)
    conn.commit()
    return id_of_new_row

#odnovariant
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
    data=findRes(tps, vsp, spkh, spkv, ekip,rk,rmk,voz,krip,gor,pol,ugl,skrip,speed)
    if data!={}:
        return render(request,"restest.html", context=data)
    else:
        id_of_new_row = setCalc(request.user.username, tps, vsp, spkh, spkv, ekip, rk, rmk, voz, krip, gor, pol, ugl,
                                skrip, speed, 0)
        p = getRes('p', id_of_new_row)
        onapr = getRes('onapr', id_of_new_row)
        y = getRes('y', id_of_new_row)
        ball = getRes('ball', id_of_new_row)
        opzp = getRes('opzp', id_of_new_row)
        aksr = getRes('aksr', id_of_new_row)
        akss = getRes('akss', id_of_new_row)
        aksb = getRes('aksb', id_of_new_row)
        vzs = getRes('vzs', id_of_new_row)
        q = getRes('q', id_of_new_row)
        data = {"p": p, "onapr": onapr, "y": y, "q": q, "ball": ball,
                "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, "vzs": vzs}
        return render(request, "restest.html", context=data)


def getRes(name, id_input):
    resAll=[]
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('''select "expected_value","cko" from "result" where "name_param" =%(name)s and id_input=%(id_input)s;''' ,{ 'name':name,'id_input':id_input})
    i=1
    for row in cursor:
        res=[]
        res.append(i)
        res.append(row[0])
        res.append(row[1])
        resAll.append(res)
        i+=1
    return  resAll

def viewresult(request):
    # sql poisk rezultata
    s = request.POST.get('speed')
    remove_digits = str.maketrans('', '', digits)
    res = s.translate(remove_digits)

    if res=='.-.':
        parent_id = request.POST.get('id')
        print(parent_id)
        p = getResMulti('p', parent_id)
        onapr = getResMulti('onapr', parent_id)
        y = getResMulti('y', parent_id)
        ball = getResMulti('ball', parent_id)
        opzp = getResMulti('opzp', parent_id)
        aksr = getResMulti('aksr', parent_id)
        akss = getResMulti('akss', parent_id)
        aksb = getResMulti('aksb', parent_id)
        vzs = getResMulti('vzs', parent_id)
        q = getResMulti('q', parent_id)
        # p = [[1, 0.02, 0.03, 60], [2, 0.201, 0.045, 60], [3, 0.02556, 0.005, 60], [4, 0.546, 0.02, 60]]
        # onapr = [[1, 0.2, 0.02, 60], [2, 0.0201, 0.0045, 60], [3, 0.56, 0.05, 60], [4, 0.546, 0.02, 60]]
        # y = [[1, 0.211, 0.025, 60], [2, 0.201, 0.045, 60], [3, 0.67, 0.25, 60], [4, 0.689, 0.2, 60]]
        # ball = [[1, 0.3, 0.03, 60], [2, 0.31, 0.05, 60], [3, 0.756, 0.163, 60], [4, 0.946, 0.02, 60]]
        # opzp = [[1, 0.21, 0.02, 60], [2, 0.201, 0.045, 60], [3, 0.156, 0.0075, 60], [4, 0.846, 0.12, 60]]
        # aksr = [[1, 0.72, 0.2, 60], [2, 0.9201, 0.045, 60], [3, 0.564, 0.05, 60], [4, 0.526, 0.02, 60]]
        # akss = [[1, 0.2, 0.02, 60], [2, 0.0201, 0.0045, 60], [3, 0.56, 0.05, 60], [4, 0.546, 0.02, 60]]
        # aksb = [[1, 0.211, 0.025, 60], [2, 0.201, 0.045, 60], [3, 0.67, 0.25, 60], [4, 0.689, 0.2, 60]]
        # vzs = [[1, 0.21, 0.02, 60], [2, 0.201, 0.045, 60], [3, 0.156, 0.0075, 60], [4, 0.846, 0.12, 60]]
        # q = [[1, 0.72, 0.2, 60], [2, 0.9201, 0.045, 60], [3, 0.564, 0.05, 60], [4, 0.526, 0.02, 60]]
        datasolo = {"p": p, "onapr": onapr, "y": y, "q": q, "ball": ball,
                "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, "vzs": vzs}
        return render(request,"multires.html", context=datasolo)
    else:
        id_input=request.POST.get('id')
        p = getRes('p',id_input)
        onapr = getRes('onapr',id_input)
        y = getRes('y',id_input)
        ball = getRes('ball',id_input)
        opzp = getRes('opzp',id_input)
        aksr = getRes('aksr',id_input)
        akss = getRes('akss',id_input)
        aksb = getRes('aksb',id_input)
        vzs = getRes('vzs',id_input)
        q = getRes('q',id_input)
        data = {"p": p, "onapr": onapr, "y": y, "q": q, "ball": ball,
                "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, "vzs": vzs}
        return render(request,"restest.html", context=data)

def getResMulti(name, id_inputl):
    resAll=[]
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('''select "expected_value","cko", "cl(9)" from "result" left join "input" on id_input=input.id where "name_param"=%(name)s and (id_input=%(id_inputl)s or parent_id=%(id_inputl)s )''',{ 'name':name,'id_inputl':id_inputl,})
    i=1
    for row in cursor:
        res=[]
        if i==5:
            i=1
        res.append(i)
        res.append(row[0]) #float(row[0])*float(row[2])/125*random.uniform(1.3, 1.7))
        res.append(row[1]) #float(row[1])*float(row[2])/125*random.uniform(1.3, 1.7))
        res.append(row[2])
        resAll.append(res)
        i+=1
    return  resAll

def createRand():
    resAll=[]
    s=30
    for j in range(1,5):
        for i in range(1, 5):
            res = []
            res.append(i)
            res.append(random.uniform(1.4, 1.7) * s)
            res.append(random.uniform(0.5, 1.1) * s)
            res.append(s)
            resAll.append(res)
        s=s+10
    return resAll

def multires(request):
    args = {}
    args.update(csrf(request))
    if request.method =="POST":
        tps = request.POST.get('tps')
        vsp = request.POST.get('vsp')
        spkh = request.POST.get('spkh')
        spkv = request.POST.get('spkv')
        ekip= request.POST.get('ekip')
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


    speedl=float(speedl)
    speedh=float(speedh)
    diff=round((speedh-speedl)/3)
    arr_speed=[float(speedl), speedl+diff, speedh-diff, float(speedh)]
    params=['p','onapr', 'y','q','ball', 'opzp','aksr', 'akss',  'aksb','vzs']
    for speed in arr_speed:
        data_Res = findRes(tps, vsp, spkh, spkv, ekip, rk, rmk, voz, krip, gor, pol, ugl, skrip, speed)
        if data_Res !={}:
            #print(data_Res)
            if speed==speedl:
                parent_id=setInput(request.user.username, tps, vsp, spkh, spkv, ekip, rk, rmk, voz, krip, gor, pol, ugl, skrip,
                         speed, 0)
                for param in params:
                    parseData(data_Res,param,parent_id)
            else:
                id_input=setInput(request.user.username, tps, vsp, spkh, spkv, ekip, rk, rmk, voz, krip, gor, pol,
                                     ugl, skrip,
                                     speed, parent_id)
                for param in params:
                    parseData(data_Res,param,id_input)

        else:
            if speed==speedl:
                parent_id=setCalc(request.user.username, tps, vsp, spkh, spkv, ekip, rk, rmk, voz, krip, gor, pol, ugl, skrip,
                        speed, 0)
            else:
                setCalc(request.user.username, tps, vsp, spkh, spkv, ekip, rk, rmk, voz, krip, gor, pol,
                                    ugl, skrip,
                                    speed, parent_id)

    #
    # parent_id=setCalc(request.user.username, tps, vsp, spkh, spkv, ekip,rk,rmk,voz,krip,gor,pol,ugl,skrip,speedl,0)
    # setCalc(request.user.username, tps, vsp, spkh, spkv, ekip,rk,rmk,voz,krip,gor,pol,ugl,skrip,speedl+diff,parent_id)
    # setCalc(request.user.username, tps, vsp, spkh, spkv, ekip,rk,rmk,voz,krip,gor,pol,ugl,skrip,speedh-diff,parent_id)
    # setCalc(request.user.username, tps, vsp, spkh, spkv, ekip,rk,rmk,voz,krip,gor,pol,ugl,skrip,speedh,parent_id)

    p = getResMulti('p',parent_id)
    onapr = getResMulti('onapr',parent_id)
    y = getResMulti('y',parent_id)
    ball = getResMulti('ball',parent_id)
    opzp = getResMulti('opzp',parent_id)
    aksr = getResMulti('aksr',parent_id)
    akss = getResMulti('akss',parent_id)
    aksb = getResMulti('aksb',parent_id)
    vzs = getResMulti('vzs',parent_id)
    q = getResMulti('q',parent_id)
    # p = createRand()
    # onapr = createRand()
    # y = createRand()
    # ball =createRand()
    # opzp = createRand()
    # aksr = createRand()
    # akss = createRand()
    # aksb = createRand()
    # vzs = createRand()
    # q = createRand()

    data = {  "p": p, "onapr": onapr, "y": y, "q": q, "ball": ball,
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

