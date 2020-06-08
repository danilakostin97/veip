import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa
from django.template.context_processors import csrf
from . import veip_params1
from string import digits
import psycopg2
import random
import re


def newd(request):
    data = {"username": request.user.username,  }
    return render(request, "app.html", context=data)

def getHistory():
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('''select * from (select distinct "id_input" from "result") t1, "input" where t1.id_input=input.id''')
    dataInput = []
    for row in cursor:
        inp=[]
        for i in range(1,18):
            inp.append(row[i])
        inp.append(row[18])
        inp.append(0)
        dataInput.append(inp)
    cursor.execute('''select * from (select distinct "id_input" from "result") t3,  
(select * from (select t1."parent_id", max(t1."cl(9)"), min(t2."cl(9)") from (select * from "input" where "parent_id">0) t1 
left join (select * from "input" where "parent_id"=0) t2 on t1."parent_id"=t2."id" group by t1.parent_id) tspeed left join  
"input" on input.id=tspeed.parent_id) tmul where t3.id_input=tmul.id;''')
    for row in cursor:
        inp=[]
        for i in range(4,20):
            inp.append(row[i])
        speedmin=str(row[3])+'-'+str(row[2])
        inp.append(speedmin)
        inp.append(row[2])
        inp.append(row[3])
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
        return render(request,"calculations.html", context=data)

def theory(request):

    data = {"username": request.user.username, 'alert_flag': True, }
    return render(request, "theory.html", context=data)

def history(request):
    if request.user.is_authenticated:
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
                "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, #"vzs": vzs
                }
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
    s = request.POST.get('speed')
    remove_digits = str.maketrans('', '', digits)
    res = s.translate(remove_digits)

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
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('''select "t(i)" from "TPS" where "id"=%(id_TPS)s;''',{'id_TPS':tps})
    tps = cursor.fetchone()[0]
    cursor.execute('''select "v(i)" from "VSP"where "id"=%(id_VSP)s;''',{'id_VSP':vsp})
    vsp = cursor.fetchone()[0]
    cursor.execute('''select "name_spkh" from "SPKH"where "id"=%(id_SPKH)s;''',{'id_SPKH':spkh})
    spkh = cursor.fetchone()[0]
    cursor.execute('''select "name_spkv" from "SPKV"where "id"=%(id_SPKV)s;''',{'id_SPKV':spkv})
    spkv = cursor.fetchone()[0]
    cursor.execute('''select "name_ekip" from "EKIP"where "id"=%(id_EKIP)s;''',{'id_EKIP':ekip})
    ekip = cursor.fetchone()[0]
    inputd=[["Тип подвижного состава", tps],["Конструкция верхнего строения пути",vsp],["Спектральные плотности неровностей пути в горизонтальной плоскости", spkh],
            ["Спектральные плотности неровностей пути в вертикальной плоскости ", spkv],["Характерные точки кузова",ekip],["Радиус кривой, м",rk],
            ["Расстояние между кругами катания, м", rmk],["Возвышение наружного рельса, м",voz],["Коэффициент Крипа, тс/м",krip],["Горизонтальная жесткость пути, тс/м", gor],
            ["Половина ширины зазора в колее",pol],["Угловой коэффициент", ugl],["Соотношение коэффициентов Крипа",skrip],["Скорость движения, м/с",speed]]
    if res=='.-.':
        parent_id = request.POST.get('id')
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
        datasolo = {"p": p, "onapr": onapr, "y": y, "q": q, "ball": ball,
                "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, #"vzs": vzs,
                    "inputd":inputd}
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
                "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, #"vzs": vzs,
                "inputd":inputd}
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
            "opzp": opzp, "aksr": aksr, "akss": akss, "aksb": aksb, #"vzs": vzs
              }
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

def change_SPKH(request):
    args = {}
    args.update(csrf(request))

    if request.method == "POST":
        nomh=int(request.POST.get('nomh'))
        name_spkh=request.POST.get('name_spkh')
        f=request.POST.get('f')
        fp=request.POST.get('fp')
        fh=request.POST.get('fh')
        print(name_spkh)
    params=[f,fp,fh]
    alert_flag=None
    #print(re.search(r'[^\W\d]', '124.,43'))
    for param in params:
        if re.search(r'[^\W\d]', param) is not None:
            alert_flag = param

    if alert_flag is not None:
        data = {"username": request.user.username, "name_spkh_val": name_spkh, "f_val": f, "fp_val": fp,
                "fh_val": fh, "alert_flag": alert_flag, "nomh_val":nomh}
        return render(request, "change_data.html", context=data)
    f=parseArr(f)
    fp = parseArr(fp)
    fh = parseArr(fh)
    query = 'INSERT INTO "SPKH" VALUES (default, %s,%s, %s,%s, %s);'
    data = (name_spkh,nomh, f,fp, fh)
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    return redirect('/testpage/change')


def change_SPKV(request):
    args = {}
    args.update(csrf(request))
    if request.method == "POST":
        name_spkv=request.POST.get('name_spkv')
        nomv=request.POST.get('nomv')
        s=request.POST.get('s')
        s1=request.POST.get('s1')
        s2=request.POST.get('s2')
        s3=request.POST.get('s3')

        params = [s, s1, s2,s3]
        alert_flag = None
        for param in params:
            if re.search(r'[^\W\d]', param) is not None:
                alert_flag = param

        if alert_flag is not None:
            data = {"username": request.user.username, "name_spkv_val": name_spkv, "nomv_val": nomv, "s_val": s,
                    "s1_val": s1, "alert_flag": alert_flag, "s2_val": s2, "s3_val":s3}
            return render(request, "change_data.html", context=data)
        s=parseArr(s)
        s1 = parseArr(s1)
        s2 = parseArr(s2)
        s3 = parseArr(s3)
        query = 'INSERT INTO "SPKV" VALUES (default, %s,%s, %s,%s,%s,%s);'
        data = (name_spkv, nomv, s, s1, s2,s3)
        conn = psycopg2.connect(dbname='veip', user='postgres',
                                password='postgres', host='localhost')
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
    return redirect('/testpage/change')

def parseArr(value):
    value = str(value)
    value = value.split(',')
    value= list(map(float, value))
    return value

def change_EKIP(request):
    args = {}
    args.update(csrf(request))
    if request.method == "POST":
        name_ekip = request.POST.get('name_ekip')
        ikus=int(request.POST.get('ikus'))

        xkus= request.POST.get('xkus')
        ykus= request.POST.get('ykus')
        zkus= request.POST.get('zkus')
        itel1= int(request.POST.get('itel1'))
        xtel1= request.POST.get('xtel1')
        ytel1= request.POST.get('ytel1')
        ztel1= request.POST.get('ztel1')
        itel2 = int(request.POST.get('itel2'))
        xtel2 = request.POST.get('xtel2')
        ytel2 = request.POST.get('ytel2')
        ztel2 = request.POST.get('ztel2')

    params = [xkus, ykus, zkus,xtel1,ytel1,ztel1,xtel2,ytel2,ztel2]
    alert_flag = None
    for param in params:
        if re.search(r'[^\W\d]', param) is not None:
            alert_flag = param

    if alert_flag is not None:
        data = {"username": request.user.username, "name_ekip_val":name_ekip, "ikus_val":ikus, "xkus_val":xkus, "ykus_val":ykus,
                "zkus_val":zkus, "itel1_val":itel1,"xtel1_val":xtel1,"ytel1_val":ytel1,"ztel1_val":ztel1,
                "itel2_val":itel2,"xtel2_val":xtel2,"ytel2_val":ytel2,"ztel2_val":ztel2,"alert_flag":alert_flag}
        return render(request, "change_data.html", context=data)

    xkus = parseArr(xkus)
    ykus = parseArr(ykus)
    zkus = parseArr(zkus)
    xtel1 = parseArr(xtel1)
    ytel1 = parseArr(ytel1)
    ztel1 = parseArr(ztel1)
    xtel2 = parseArr(xtel2)
    ytel2 = parseArr(ytel2)
    ztel2 = parseArr(ztel2)
    query = 'INSERT INTO "EKIP" VALUES (default, %s,%s, %s,%s,%s,%s, %s,%s, %s,%s,%s,%s,%s);'
    data = (name_ekip, ikus, xkus, ykus, zkus, itel1,xtel1,ytel1,ztel1, itel2,xtel2,ytel2,ztel2)
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    return redirect('/testpage/change')

def change_TPS(request):
    args = {}
    args.update(csrf(request))
    print('TPS')
    if request.method == "POST":
        print(request.POST)
        t=request.POST.get('t')
        ek1=float(request.POST.get('ek1'))
        ek2=float(request.POST.get('ek2'))
        ek3=float(request.POST.get('ek3'))
        ek4=float(request.POST.get('ek4'))
        ek5=float(request.POST.get('ek5'))
        ek6=float(request.POST.get('ek6'))
        ek7=float(request.POST.get('ek7'))
        ek8=float(request.POST.get('ek8'))
        ek9=float(request.POST.get('ek9'))
        ek10=float(request.POST.get('ek10'))
        ek11=float(request.POST.get('ek11'))
        ek12=float(request.POST.get('ek12'))
        ek13=float(request.POST.get('ek13'))
        ek14=float(request.POST.get('ek14'))
        ek15=float(request.POST.get('ek15'))
        ek16=float(request.POST.get('ek16'))
        ek17=float(request.POST.get('ek17'))
        ek18=float(request.POST.get('ek18'))
        ek19=float(request.POST.get('ek19'))
        ek20=float(request.POST.get('ek20'))
        ek21=float(request.POST.get('ek21'))
        ek22=float(request.POST.get('ek22'))
        ek23=float(request.POST.get('ek23'))
        ek24=float(request.POST.get('ek24'))
        hct=float(request.POST.get('hct'))
        n1=int(request.POST.get('n1'))
        no1=int(request.POST.get('no1'))
        an1=request.POST.get('an1')
        an2=request.POST.get('an2')

    params = [an1,an2]
    alert_flag = None
    for param in params:
        if re.search(r'[^\W\d]', param) is not None:
            alert_flag = param

    if alert_flag is not None:
        data = {"username": request.user.username, "t_val":t, "ek1_val":ek1, "ek2_val":ek2, "ek3_val":ek3, "ek4_val":ek4, "ek5_val":ek5,
                "ek6_val":ek6, "ek7_val":ek7, "ek8_val":ek8, "ek9_val":ek9, "ek10_val":ek10, "ek11_val":ek11, "ek12_val":ek12,"ek13_val":ek13,"ek14_val":ek14,
                "ek15_val":ek15,"ek16_val":ek16,"ek17_val":ek17,"ek18_val":ek18,"ek19_val":ek19,"ek20_val":ek20,"ek21_val":ek21,"ek22_val":ek22,"ek23_val":ek23,
                "ek24_val":ek24,"hct_val":hct,"n1_val":n1,"no1_val":no1, "an1_val":an1,"an2_val":an2, "alert_flag": alert_flag}
        return render(request, "change_data.html", context=data)

    an1 = parseArr(an1)
    an2 = parseArr(an2)
    query = 'INSERT INTO "TPS" VALUES (default, %s,%s, %s,%s,%s,%s, %s,%s, %s,%s,%s,%s,%s, %s,%s, %s,%s,%s,%s, %s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s);'
    data = (t, ek1, ek2, ek3, ek4, ek5, ek6, ek7, ek8, ek9, ek10, ek11, ek12,ek13,ek14,ek15,ek16,ek17,ek18,ek19,ek20,ek21,ek22,ek23,ek24,hct,n1,no1, an1,an2)
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    return redirect('/testpage/change')

def change_VSP(request):
    args = {}
    args.update(csrf(request))
    print('TPS')
    if request.method == "POST":
        v=request.POST.get('v')
        put1 = float(request.POST.get('put1'))
        put2 = float(request.POST.get('put2'))
        put3 = float(request.POST.get('put3'))
        put4 = float(request.POST.get('put4'))
        put5 = float(request.POST.get('put5'))
        put6 = float(request.POST.get('put6'))
        put7 = float(request.POST.get('put7'))
        put8 = float(request.POST.get('put8'))
        put9 = float(request.POST.get('put9'))
        put10 = float(request.POST.get('put10'))
        put11 = float(request.POST.get('put11'))
        put12 = float(request.POST.get('put12'))
        put13 = float(request.POST.get('put13'))
        put14 = float(request.POST.get('put14'))
        put15 = float(request.POST.get('put15'))
        put16 = float(request.POST.get('put16'))
        put17 = float(request.POST.get('put17'))
        put18 = float(request.POST.get('put18'))
        put19 = float(request.POST.get('put19'))
        put20 = float(request.POST.get('put20'))
        put21 = float(request.POST.get('put21'))
        put22 = float(request.POST.get('put22'))
        put23 = float(request.POST.get('put23'))
        put24 = float(request.POST.get('put24'))
        put25 = float(request.POST.get('put25'))
        put26 = float(request.POST.get('put26'))
        put27 = float(request.POST.get('put27'))
        put28 = float(request.POST.get('put28'))
        put29 = float(request.POST.get('put29'))
        put30 = float(request.POST.get('put30'))
        put31 = float(request.POST.get('put31'))
        put32 = float(request.POST.get('put33'))
        put33 = float(request.POST.get('put33'))

    query = 'INSERT INTO "VSP" VALUES (default, %s,%s, %s,%s,%s,%s, %s,%s, %s,%s,%s,%s,%s, %s,%s, %s,%s,%s,%s, %s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    data = (v, put1, put2, put3, put4, put5, put6, put7, put8, put9, put10, put11, put12, put13, put14, put15, put16, put17, put18, put19, put20,
put21, put22, put23, put24,put25, put26, put27, put28, put29,put30, put31, put32, put33)
    conn = psycopg2.connect(dbname='veip', user='postgres',
                            password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    return redirect('/testpage/change')