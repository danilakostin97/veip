import numpy as np
import sympy as sp
import sys
import warnings
import time
import psycopg2

class cput():
    def load_from_db(self, cursor, id_input):
        self.cursor=cursor

        ### ПОДКЛЮЧЕНИЕ К БД ###


        ### ТАБЛИЦА INPUT ###

        cursor.execute(''' select "id_TPS" from "input"
        where id =%s;''' % id_input)
        itps = cursor.fetchone()[0]

        cursor.execute(''' select "id_VSP" from "input"
        where id =%s; ''' % id_input)
        ivsp = cursor.fetchone()[0]

        cursor.execute(''' select "id_SPKH" from "input"
        where id =%s; ''' % id_input)
        isph = cursor.fetchone()[0]

        cursor.execute(''' select "id_SPKV" from "input"
        where id =%s; ''' % id_input)
        ispv = cursor.fetchone()[0]

        ipec = 0  # игнор, всегда равно 0

        cursor.execute(''' select "id_EKIP" from "input"
        where id =%s; ''' % id_input)
        iekip = cursor.fetchone()[0]

        cursor.execute('''  select "cl(1)","cl(2)","cl(3)","cl(4)",
        "cl(5)","cl(6)","cl(7)","cl(8)","cl(9)"
        from "input"
        where id =%s;''' % id_input)
        c1 = list(cursor.fetchone())

        ### ТАБЛИЦА TPS ###

        cursor.execute(''' select "t(i)" from "TPS"
        where id =%s; ''' % itps)

        tp = str(cursor.fetchone()[0])  # t(4)

        cursor.execute('''select  "ek(1)","ek(2)", "ek(3)","ek(4)", "ek(5)","ek(6)",
                          "ek(7)","ek(8)", "ek(9)","ek(10)", "ek(11)","ek(12)",
                          "ek(13)","ek(14)", "ek(15)","ek(16)","ek(17)","ek(18)",
                          "ek(19)","ek(20)", "ek(21)","ek(22)","ek(23)","ek(24)"
                          from "TPS"
                          where id =%s;''' % itps)

        ek = list(cursor.fetchone())

        cursor.execute(''' select "hct" from "TPS"
        where id =%s;''' % itps)
        hc = cursor.fetchone()[0]  # hct

        cursor.execute('''select "n1" from "TPS"
        where id =%s;''' % itps)

        n = int(cursor.fetchone()[0])  # nl

        cursor.execute('''select "nol" from "TPS"
        where id =%s;''' % itps)
        no1 = int(cursor.fetchone()[0])

        cursor.execute('''select "an1(i)" from "TPS"
        where id =%s;''' % itps)
        an1 = cursor.fetchone()[0]

        cursor.execute('''select "an2(i:j)" from "TPS"
        where id =%s;''' % itps)
        a1 = cursor.fetchone()[0]  # проблема, должно быть 6 значений, у нас 4
        a1_1 = [a1[0], a1[1]]
        a1_2 = [a1[2], a1[3]]
        a1_3 = [0, 0]
        an2 = [a1_1, a1_2, a1_3]

        ### ТАБЛИЦА VSP ###

        cursor.execute('''select "v(i)" from "VSP"
        where id =%s;''' % ivsp)
        vc = cursor.fetchone()[0]  # v

        cursor.execute('''select
           "put(1)" , "put(2)" , "put(3)" , "put(4)",
          "put(5)" , "put(6)" , "put(7)" , "put(8)",
          "put(9)" , "put(10)" , "put(11)" , "put(12)",
          "put(13)" , "put(14)" , "put(15)" , "put(16)",
          "put(17)" , "put(18)" , "put(19)" , "put(20)",
          "put(21)" , "put(22)" , "put(23)" , "put(24)",
          "put(25)" , "put(26)" , "put(27)" , "put(28)",
          "put(29)" , "put(30)" , "put(31)" , "put(32)",
          "put(33)"
        from "VSP"
        where id =%s;''' % ivsp)
        pt = list(cursor.fetchone())  # put(33)

        ### ТАБЛИЦА SPKH ###

        # не хватает названия для файла spkh (поле name_spkh)

        cursor.execute('''select "nomh" from "SPKH"
        where id=%s; ''' % isph)
        nomh = cursor.fetchone()[0]

        cursor.execute('''select "f(i)" from "SPKH"
        where id=%s; ''' % isph)
        zeros = [0.0] * 39  # массив для хранения нулей
        f = list(cursor.fetchone())[0] + zeros

        cursor.execute('''select "fp(i)" from "SPKH"
        where id=%s; ''' % isph)
        fp = list(cursor.fetchone())[0] + zeros

        cursor.execute('''select "fh(i)" from "SPKH"
        where id=%s; ''' % isph)
        fh = list(cursor.fetchone())[0] + zeros

        ### ТАБЛИЦА SPKV ###

        # не хватает названия для файла spkv (поле name_spkv)

        cursor.execute('''select "nomv" from "SPKV"
          where id =%s;''' % ispv)
        nomv = cursor.fetchone()[0]

        cursor.execute('''select "s(i)" from "SPKV"
          where id =%s;''' % ispv)
        zeros = [0.0] * 25
        s = cursor.fetchone()[0] + zeros

        cursor.execute('''select "s1(i)" from "SPKV"
          where id =%s;''' % ispv)
        s1 = cursor.fetchone()[0] + zeros
        zeros = [0.0] * 50  # т.к s2 и s3  равны 0
        s2 = zeros
        s3 = zeros

        ### ТАБЛИЦА EKIP ###

        # не хватает поля name_ekip

        zeros = [0.0] * 2

        cursor.execute('''select "ikus" from "EKIP"
          where id =%s;''' % iekip)
        ikus = cursor.fetchone()[0]

        cursor.execute('''select "xkus(i)" from "EKIP"
          where id =%s;''' % iekip)
        xkus = cursor.fetchone()[0] + zeros

        cursor.execute('''select "ykus(i)" from "EKIP"
          where id =%s;''' % iekip)
        ykus = cursor.fetchone()[0] + zeros

        cursor.execute('''select "zkus(i)" from "EKIP"
          where id =%s;''' % iekip)
        zkus = cursor.fetchone()[0] + zeros

        zeros = [0.0] * 10

        cursor.execute('''select "itel1" from "EKIP"
          where id =%s;''' % iekip)
        itel1 = cursor.fetchone()[0]

        cursor.execute('''select "xtel1(i)" from "EKIP"
          where id =%s;''' % iekip)
        xtell = cursor.fetchone()[0] + zeros

        cursor.execute('''select "ytel1(i)" from "EKIP"
          where id =%s;''' % iekip)
        ytell = cursor.fetchone()[0] + zeros

        cursor.execute('''select "ztel1(i)" from "EKIP"
          where id =%s;''' % iekip)
        ztell = [0.0] * 17

        cursor.execute('''select "itel1" from "EKIP"
          where id =%s;''' % iekip)
        itel2 = cursor.fetchone()[0]

        cursor.execute('''select "xtel2(i)" from "EKIP"
          where id =%s;''' % iekip)
        xtel2 = cursor.fetchone()[0] + zeros

        cursor.execute('''select "ytel2(i)" from "EKIP"
          where id =%s;''' % iekip)
        ytel2 = cursor.fetchone()[0] + zeros

        cursor.execute('''select "ztel2(i)" from "EKIP"
          where id =%s;''' % iekip)
        ztel2 = [0.0] * 17
        ######### ДАЛЬШЕ НЕ ТРОГАТЬ #########
        self.put.fill(0)
        self.ek1.fill(0)
        self.ek2.fill(0)
        self.ek3.fill(0)
        self.ek4.fill(0)
        self.spektr.fill(0)
        self.v.fill(0)
        self.rs.fill(0)
        self.ntoch = 5
        self.put[1 - 1] = pt[25 - 1]
        self.put[2 - 1] = pt[27 - 1]
        self.put[3 - 1] = pt[22 - 1]
        self.put[4 - 1] = pt[1 - 1]
        self.put[5 - 1] = pt[2 - 1]
        self.put[6 - 1] = pt[12 - 1]
        self.put[7 - 1] = pt[12 - 1] / pt[4 - 1]
        self.put[8 - 1] = pt[19 - 1]
        self.put[9 - 1] = pt[20 - 1]
        self.put[10 - 1] = pt[20 - 1]
        self.nom = nomv
        for i in range(self.nom):
            self.spektr[1 - 1][i] = s[i]
            self.spektr[2 - 1][i] = s1[i]
            self.spektr[3 - 1][i] = s2[i]
            self.spektr[4 - 1][i] = s3[i]
        self.v[1 - 1] = c1[1 - 1] * 3.6
        self.v[2 - 1] = c1[1 - 1] * 3.6
        self.v[3 - 1] = c1[1 - 1] * 3.6
        self.shp[1 - 1] = pt[16 - 1]
        self.shp[2 - 1] = pt[17 - 1]
        self.shp[3 - 1] = pt[33 - 1]
        self.shp[4 - 1] = pt[16 - 1] * pt[17 - 1] * pt[18 - 1] / 2
        self.rs[1 - 1] = pt[32 - 1]
        self.rs[2 - 1] = pt[31 - 1]
        self.rs[3 - 1] = pt[30 - 1]
        self.rs[4 - 1] = pt[29 - 1]
        self.n1 = n * no1
        self.n2 = n
        self.n3 = 1
        self.n4 = 0
        ek[1 - 1] = ek[1 - 1] / 10
        ek[2 - 1] = ek[2 - 1] / 10
        ek[5 - 1] = ek[5 - 1] / 10
        ek[6 - 1] = ek[6 - 1] / 10
        ek[7 - 1] = ek[7 - 1] / 1962
        ek[8 - 1] = ek[8 - 1] / 1962
        ek[9 - 1] = ek[9 - 1] / 1962
        ek[10 - 1] = ek[10 - 1] * 100
        ek[15 - 1] = ek[15 - 1] / 10 ** 4
        ek[16 - 1] = ek[16 - 1] / 10 ** 4
        ek[17 - 1] = ek[17 - 1] * 10
        ek[18 - 1] = ek[18 - 1] / 10 ** 4
        ek[19 - 1] = ek[19 - 1] / 10 ** 4
        ek[20 - 1] = ek[20 - 1] * 10
        ek[21 - 1] = ek[21 - 1] / 10
        ek[24 - 1] = ek[24 - 1] / 10
        for i in range(n):
            for j in range(no1):
                if j == 1 - 1:
                    an1[i] = an1[i] * 100
                an2[i][j] = an2[i][j] * 100
        for i in range(self.n1):
            self.ek1[1 - 1][i] = ek[7 - 1]
            self.ek1[2 - 1][i] = ek[3 - 1]
            self.ek1[3 - 1][i] = ek[22 - 1]
            j = 1 - 1
            l = i
            if i > no1 - 1:
                j = 2 - 1
                l = i - no1
            self.ek1[4 - 1][i] = an2[l][j] - an2[1 - 1][1 - 1]
            self.ek1[5 - 1][i] = ek[10 - 1]
            self.ek1[6 - 1][i] = j + 1
        for i in range(self.n2):
            self.ek2[1 - 1][i] = ek[8 - 1]
            self.ek2[2 - 1][i] = ek[4 - 1] / 2
            self.ek2[3 - 1][i] = ek[23 - 1]
            self.ek2[4 - 1][i] = an1[i] - an2[1 - 1][1 - 1]
            self.ek2[5 - 1][i] = ek[17 - 1] / 2
            self.ek2[6 - 1][i] = self.ek2[4 - 1][i]
            self.ek2[7 - 1][i] = 1
        self.ek3[1 - 1][1 - 1] = ek[9 - 1]
        self.ek3[2 - 1][1 - 1] = 0
        self.ek3[3 - 1][1 - 1] = 0
        self.ek3[4 - 1][1 - 1] = 0 - an2[1 - 1][1 - 1]
        self.ek3[5 - 1][1 - 1] = ek[20 - 1] / 2
        self.ek3[6 - 1][1 - 1] = 0 - an2[1 - 1][1 - 1]
        self.v[4 - 1] = self.v[1 - 1]
        self.v[1 - 1] = 250 * self.v[4 - 1] / 9
        self.trp(id_input)

    def __init__(self):
        self.put = np.ndarray(10, dtype=float)
        self.spektr = np.ndarray((4, 100), dtype=float, order='F')
        self.ek1 = np.ndarray((6, 12), dtype=float, order='F')
        self.ek2 = np.ndarray((7, 8), dtype=float, order='F')
        self.ek3 = np.ndarray((6, 4), dtype=float, order='F')
        self.ek4 = np.ndarray(3, dtype=float)
        self.ek4.fill(0)
        self.n1=self.n2=self.n3=self.n4=self.nom=int(0)
        self.v = np.ndarray(4, dtype=float)
        self.wo = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.wy = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.sk = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.wm = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.ws = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.wb = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.wp = np.ndarray((4, 4), dtype=np.complex128, order='F')
        self.sp = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.om=self.omb=0
        self.cu = np.ndarray(10, dtype=np.complex128)
        self.z = np.ndarray(10, dtype=np.complex128)
        self.z1 = np.ndarray(10, dtype=np.complex128)
        self.wbm = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.wbp = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.wksi=self.mksi=complex(0, 0)
        self.wa = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.wr = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.s = np.ndarray(3, dtype=float)
        self.sr = np.ndarray(12, dtype=float)
        self.sa = np.ndarray(12, dtype=float)
        self.rs = np.ndarray(4, dtype=float)
        self.shp = np.ndarray(4, dtype=float)
        self.ntoch = 0
        self.sh1 = np.ndarray(12, dtype=float)
        self.sh2 = np.ndarray(12, dtype=float)
        self.sy = np.ndarray(12, dtype=float)
        self.sm = np.ndarray(12, dtype=float)
        self.ss = np.ndarray(12, dtype=float)
        self.sb = np.ndarray(12, dtype=float)
        self.so = np.ndarray(12, dtype=float)
        self.sbm = np.ndarray(12, dtype=float)
        self.sbp = np.ndarray(12, dtype=float)
        self.wshp = np.ndarray((12, 12), dtype=np.complex128, order='F')
        self.sshp = np.ndarray(12, dtype=float)
        self.a = np.ndarray((38, 50), dtype=np.complex128, order='F').transpose()
        self.se = np.ndarray((22, 22), dtype=np.complex128, order='F')
        self.n = int(0)
        self.wyv = np.ndarray((12,12), dtype=np.complex128, order='F')
        self.sv = np.ndarray(12, dtype=float)


    def trp(self,id_input):
        skv = np.ndarray((65, 22, 22), dtype=np.complex128, order='F')
        wk = np.ndarray(128, dtype=np.complex128)
        vy = np.ndarray(12, dtype=float)
        vm = np.ndarray(12, dtype=float)
        vs = np.ndarray(12, dtype=float)
        vb = np.ndarray(12, dtype=float)
        vo = np.ndarray(12, dtype=float)
        vp = np.ndarray(12, dtype=float)
        vy3 = np.ndarray(12, dtype=float)
        vm3 = np.ndarray(12, dtype=float)
        vs3 = np.ndarray(12, dtype=float)
        vb3 = np.ndarray(12, dtype=float)
        vo3 = np.ndarray(12, dtype=float)
        vbp3 = np.ndarray(12, dtype=float)
        vz = np.ndarray(12, dtype=float)
        vzs = np.ndarray(12, dtype=float)
        vzs3 = np.ndarray(12, dtype=float)
        vz3 = np.ndarray(12, dtype=float)
        bz = np.ndarray(12, dtype=float)
        sz = np.ndarray(12, dtype=float)
        vp3 = np.ndarray(12, dtype=float)
        sbh = np.ndarray((128, 12), dtype=float, order='F')
        sbh1 = np.ndarray((128, 12), dtype=float, order='F')
        shh1 = np.ndarray((128, 12), dtype=float, order='F')
        shh2 = np.ndarray((128, 12), dtype=float, order='F')
        vr = np.ndarray(12, dtype=float)
        vr1 = np.ndarray(12, dtype=float)
        vr2 = np.ndarray(12, dtype=float)
        vr3 = np.ndarray(12, dtype=float)
        vbm3 = np.ndarray(12, dtype=float)
        va = np.ndarray(12, dtype=float)
        va3 = np.ndarray(12, dtype=float)
        om1 = np.ndarray(65, dtype=float)
        #######
        am2=0
        az=0
        #######
        iz=0
        w01=0.
        w02=0.
        self.omb=0.1E-03
        self.s[1-1]=self.spektr[2-1][1-1]
        self.s[2-1]=self.spektr[3-1][1-1]
        self.s[3-1]=self.spektr[4-1][1-1]
        self.om=self.omb*self.v[1-1]
        h=0
        self.way(h)
        n8=self.n
        iekip=1
        om1[1-1]=self.om
        for i in range(self.n):
            for j in range(self.n):
                skv[1][i][j]=self.se[i][j]
        wk[1-1]=self.wksi
        for k in range(self.n1):
            sbh[1-1][k]=self.sb[k]
            shh1[1-1][k]=self.sh1[k]
            shh2[1-1][k]=self.sh2[k]
            sbh1[1-1][k]=self.sbm[k]+self.sbp[k]
            vy3[k]=0
            vb3[k]=0
            vzs3[k]=0
            vr3[k]=0
            va3[k]=0
            vbm3[k]=0
            vbp3[k]=0
            vm3[k]=0
            vs3[k]=0
            vo3[k]=0
            vp3[k]=self.ek1[5-1][k]
            for j in range(self.n1):
                w01+=self.wyv[k][j]*self.ek1[5-1][j]
                vy3[k]+=self.wy[k][j]*self.ek1[5-1][j]
                vzs3[k]+=self.wshp[k][j]*self.ek1[5-1][j]
                vm3[k]+=self.wm[k][j]*self.ek1[5-1][j]
                vr3[k]+=self.wr[k][j]*self.ek1[5-1][j]
                va3[k]+=self.wa[k][j]*self.ek1[5-1][j]
                vs3[k]+=self.ws[k][j]*self.ek1[5-1][j]
                vbm3[k]+=self.wbm[k][j]*self.ek1[5-1][j]
                vbp3[k]+=self.wbp[k][j]*self.ek1[5-1][j]
                vb3[k]+=self.wb[k][j]*self.ek1[5-1][j]
        w01=w01**2*self.put[2-1]/2
        self.omb=self.spektr[1-1][1-1]
        for aaa in range(self.nom):
            if(self.spektr[1-1][aaa]>37/self.v[1-1]):
                k=aaa
                break
        h1=self.spektr[1-1][k]-self.spektr[1-1][1-1]
        h2=self.spektr[1-1][self.nom-1]-self.spektr[1-1][k]
        im=2
        ki=2
        ni=int(2**self.ntoch)
        if h1!=0:
            h=h1/ni
            for k in range(self.n1):
                vp[k]=0
                vzs[k]=0
                vr[k]=0
                va[k]=0
                vy[k]=0
                vm[k]=0
                vb[k]=0
                vs[k]=0
                vo[k]=0

            while True:
                for i in range(ni):
                    m=ni-i+(im-1)*ni
                    am1=1
                    if i==1-1 or i==ni-1:
                        am1=0.5
                    for k in range(self.n1):
                        i1=1
                        sbh[i+(2-ki)*ni][k]=self.sb[k]
                        sbh1[i+(2-ki)*ni][k]=self.sbm[k]+self.sbp[k]
                        shh1[i+(2-ki)*ni][k]=self.sh1[k]
                        shh2[i+(2-ki)*ni][k]=self.sh2[k]
                        wk[i+(2-ki)*ni]=self.wksi
                        vp[k]+=self.sp[k][k]*am1
                        vr[k]+=self.sr[k]*am2
                        va[k]=self.sa[k]*am2
                        vy[k]+=(self.sy[k]+self.s[3-1]*abs(self.wksi)**2*h)*am1
                        vzs[k]+=(self.sshp[k]+self.s[3-2]*abs(self.wksi)**2*h)*am1
                        vm[k]+=(self.sm[k]+self.s[3-2]*abs(self.mksi)**2*h)*am1
                        wwp=((1.-abs(self.wksi))*self.put[3-1]*self.put[9-1])**2*self.s[3-1]
                        vs[k]+=(self.ss[k]+wwp*h)*am1
                        vb[k]+=(self.sb[k]+wwp/self.shp[4-1]**2*h)*am1
                        vo[k]+=self.so[k]*am2
                        w02+=w02+self.sv[k]*am2*h
                    imis=1
                    for j1 in range(self.nom):
                        if self.omb-self.spektr[1-1][j1]==0:
                            self.s[1-1]=self.spektr[2-1][j1]
                            self.s[2-1]=self.spektr[3-1][j1]
                            self.s[3-1]=self.spektr[4-1][j1]
                            break
                        elif self.omb-self.spektr[1-1][j1]<0:
                            if j1!=0:
                                e=(np.log(self.omb)-np.log(self.spektr[1-1][j1-1]))/(np.log(self.spektr[1-1][j1])-np.log(self.spektr[1-1][j1-1]))
                                for k1 in range(2-1,4):
                                    if self.spektr[k1][j1]<=0:
                                        self.s[k1-1]=0.
                                    else:
                                        self.s[k1-1]=self.spektr[k1][j1]**e*self.spektr[k1][j1-1]**(1-e)
                                break
                            else:
                                self.s[1] = self.spektr[2 - 1][j1]
                                self.s[2] = self.spektr[3 - 1][j1]
                                self.s[3] = self.spektr[4 - 1][j1]
                                break
                        else:
                            if j1-self.nom==0:
                                e=(np.log(self.omb)-np.log(self.spektr[1-1][j1-1]))/(np.log(self.spektr[1-1][j1])-np.log(self.spektr[1-1][j1-1]))
                                for k1 in range(2 - 1, 4):
                                    if self.spektr[k1][j1] <= 0:
                                        self.s[k1 - 1] = 0.
                                    else:
                                        self.s[k1 - 1] = self.spektr[k1][j1] ** e * self.spektr[k1][j1 - 1] ** (1 - e)
                                break
                    self.om=self.omb*self.v[1-1]
                    imis=2
                    self.way(h)
                    if((i+1)//2*2==i+1):
                        iekip+=1
                        om1[iekip]=self.om
                        for mi in range(self.n):
                            for mj in range(self.n):
                                skv[iekip][mi][mj]=self.se[mi][mj]
                    self.omb+=h
                ki=1
                if im!=1:
                    h=h2/ni
                    im=1
                    if ki==2:
                        break
                else:
                    break

            for k in range(self.n1):
                vp[k]=np.sqrt(abs(vp[k]))
                vr[k]=np.sqrt(abs(vr[k]))
                va[k]=np.sqrt(abs(va[k]))
                vy[k]=np.sqrt(abs(vy[k]))
                vzs[k]=np.sqrt(abs(vzs[k]))
                vs[k]=np.sqrt(abs(vs[k]))
                vm[k]=np.sqrt(abs(vm[k]))
                vb[k]=np.sqrt(abs(vb[k]))/self.shp[4-1]
                vo[k]=np.sqrt(abs(vo[k]))

            c1h=(self.put[9-1]+self.shp[2-1]/2)/self.shp[3-1]
            c2h=(self.put[9-1]-self.shp[2-1]/2)/self.shp[3-1]
            bet1=np.arctan(c1h)
            bet2=np.arctan(c2h)
            az=(bet1-bet2+(np.sin(2*bet1)-np.sin(2*bet2))/2)/(4*self.shp[4-1])
            c1h=1.02*self.shp[2-1]*self.shp[3-1]/(self.shp[2-1]**2+4*self.shp[3-1]**2)
            c2h=0.509*(1-self.shp[2-1]**2/(12*self.shp[3-1]**2))*self.shp[2-1]/(2*self.shp[3-1])
            for k in range(self.n1):
                bz[k]=8.9/(vb3[k]/self.shp[4-1]+2.5*vb[k]+4.35)
                if bz[k]<1:
                    bz[k]=1
                if bz[k]>2:
                    bz[k]=2
                bz[k]=(bz[k]*c2h+(2.-bz[k])*c1h)/self.shp[4-1]
            imis=3
            iz=1

        # ветка для iz=1
        for k in range(self.n1):
            vz3[k]=az*(vbm3[k]+vbp3[k])+bz[k]*vb3[k]
            vb3[k] = vb3[k]/self.shp[4-1]
        omb=self.spektr[1-1][1-1]
        for aaa in range(self.nom):
            if (self.spektr[1 - 1][aaa] > 37 / self.v[1 - 1]):
                k=aaa
                break
        k = aaa
        h1 = self.spektr[1-1][k]-self.spektr[1-1][1-1]
        h2 = self.spektr[1-1][self.nom]-self.spektr[1-1][k]
        im = 2
        ki = 2
        ni = int(2 ** self.ntoch)
        if h1 != 0:
            h = h1 / ni
            for k in range(self.n1):
                vz[k] = 0
            while True:
                for i in range(ni):
                    m=ni-i+(im-1)*ni
                    am1=1
                    if i==1-1 or i==ni-1:
                        am1=0.5
                    for k in range(self.n1):
                        i1=1
                        sz[k]=az**2*sbh1[i+(2-ki)*ni][k]+bz[k]**2*sbh[i+(2-ki)*ni][k]+2*az \
                         *(bz[k]*shh1[i+(2-ki)*ni][k]+az*shh2[i+(2-ki)*ni][k])
                        ch1=self.s[3-1]*((1.-abs(wk[i+(2-ki)*ni]))*self.put[3-1]*self.put[9-1])**2/self.shp[4-1]**2
                        ch1*=(2.*az*np.cos(self.put[9-1]*self.omb)+bz[k])**2
                        vz[k]+=(sz[k]+ch1*h)*am1
                    imis=1
                    for j1 in range(self.nom):
                        if self.omb - self.spektr[1 - 1][j1] == 0:
                            self.s[1 - 1] = self.spektr[2 - 1][j1]
                            self.s[2 - 1] = self.spektr[3 - 1][j1]
                            self.s[3 - 1] = self.spektr[4 - 1][j1]
                            break
                        elif self.omb - self.spektr[1 - 1][j1] < 0:
                            if j1 != 0:
                                e = (np.log(self.omb) - np.log(self.spektr[1 - 1][j1 - 1])) / (
                                            np.log(self.spektr[1 - 1][j1]) - np.log(self.spektr[1 - 1][j1 - 1]))
                                for k1 in range(2 - 1, 4):
                                    if self.spektr[k1][j1] <= 0:
                                        self.s[k1 - 1] = 0.
                                    else:
                                        self.s[k1 - 1] = self.spektr[k1][j1] ** e * self.spektr[k1][j1 - 1] ** (1 - e)
                                break
                            else:
                                self.s[1] = self.spektr[2 - 1][j1]
                                self.s[2] = self.spektr[3 - 1][j1]
                                self.s[3] = self.spektr[4 - 1][j1]
                                break
                        else:
                            if j1 - self.nom == 0:
                                e = (np.log(self.omb) - np.log(self.spektr[1 - 1][j1 - 1])) / (
                                            np.log(self.spektr[1 - 1][j1]) - np.log(self.spektr[1 - 1][j1 - 1]))
                                for k1 in range(2 - 1, 4):
                                    if self.spektr[k1][j1] <= 0:
                                        self.s[k1 - 1] = 0.
                                    else:
                                        self.s[k1 - 1] = self.spektr[k1][j1] ** e * self.spektr[k1][j1 - 1] ** (1 - e)
                                break
                    self.om=self.omb*self.v[1-1]
                    self.omb+=h
                ki=1
                if im!=1:
                    h=h2/ni
                    im=1
                    if ki==2:
                        break
                else:
                    break
        for k in range(self.n1):
            vz[k]=np.sqrt(abs(vz[k]))

        #### ВЫГРУЗКА РЕЗУЛЬТАТОВ В БД ####
        cursor = self.cursor
        for number_axis in range(self.n1):
            cursor.execute("""INSERT INTO "result" VALUES (default,%s,%s, %s,%s, %s)""",
                           (id_input, 'p', number_axis + 1, vp3[number_axis], vp[number_axis]))
            

            cursor.execute("""INSERT INTO "result" VALUES (default,%s,%s, %s,%s, %s)""",
                           (id_input, 'onapr', number_axis + 1, vm3[number_axis], vm[number_axis]))
            

            cursor.execute("""INSERT INTO "result" VALUES (default,%s,%s, %s,%s, %s)""",
                           (id_input, 'y', number_axis + 1, vy3[number_axis], vy[number_axis]))
            

            cursor.execute("""INSERT INTO "result" VALUES (default,%s,%s, %s,%s, %s)""",
                           (id_input, 'q', number_axis + 1, vs3[number_axis], vs[number_axis]))
            

            cursor.execute("""INSERT INTO "result" VALUES (default,%s,%s, %s,%s, %s)""",
                           (id_input, 'ball', number_axis + 1, vb3[number_axis], vb[number_axis]))
            

            cursor.execute("""INSERT INTO "result" VALUES (default, %s,%s, %s,%s, %s)""",
                           (id_input, 'opzp', number_axis + 1, vz3[number_axis], vz[number_axis]))
            

            cursor.execute("""INSERT INTO "result" VALUES (default,%s,%s, %s,%s, %s)""",
                           (id_input, 'aksr', number_axis + 1, vr3[number_axis], vr[number_axis]))
            

            cursor.execute("""INSERT INTO "result" VALUES (default,%s,%s, %s,%s, %s)""",
                           (id_input, 'akss', number_axis + 1, va3[number_axis], va[number_axis]))
            

            cursor.execute("""INSERT INTO "result" VALUES (default, %s,%s, %s,%s, %s)""",
                           (id_input, 'aksb', number_axis + 1, vo3[number_axis], vo[number_axis]))
            

            cursor.execute("""INSERT INTO "result" VALUES (default, %s,%s, %s,%s, %s)""",
                           (id_input, 'vzs', number_axis + 1, vzs3[number_axis], vzs[number_axis]))
            

    def way(self, hhhh):
        self.train()
        self.cu[1-1]=complex(1.,0.)
        self.cu[2-1]=0.
        ci=complex(0.,1.)
        a1=self.put[4-1]*self.put[6-1]
        b1=(self.put[1-1]*self.v[1-1]**2)/a1
        c1=self.put[2-1]*self.v[1-1]/a1
        r1=self.put[3-1]/a1
        self.cu[3-1]=complex(b1,0.)
        self.cu[4-1]=complex(-c1,-2.*b1*self.omb)
        self.cu[5-1]=complex(r1-b1*self.omb**2,c1*self.omb)
        for i in range(5):
            self.cu[i]=self.cu[i]/(self.cu[5-1]*10**((5-i+1)*1.5))

        # Решение характеристического уравнения через SymPy
        r = sp.Symbol('r')
        rez = sp.solve(self.cu[0] * r ** 4 + self.cu[2] * r ** 2 + self.cu[3] * r + self.cu[4], r)
        #self.lmrots(self.cu,self.z1,self.z,0.000001,4)
        self.z1[0]=rez[1]*(10**(0-1.5))
        self.z1[1]=rez[3]*(10**(0-1.5))
        self.z1[2]=rez[0]*(10**(0-1.5))
        self.z1[3]=rez[2]*(10**(0-1.5))


        '''
        for i in range(4):
            self.z[i]=self.z[i]*10**(-1.5)
        k=1-1
        i=4-1
        for j in range(4):
            alf=self.z[j]
            r1=float(alf)
            if r1<=0:
                self.z1[k]=alf
                k=k+2
            else:
                self.z1[i]=alf
                i=i-2
        '''
        ed=1.
        for k in range(4):
            self.z[k]=complex(1,0)
            for j in range(4):
                if k!=j:
                    self.z[k]=self.z[k]/(self.z1[k]-self.z1[j])
            self.z[k]=ed*self.z[k]/a1
            ed=-1.*ed

        omb1=complex(0,self.omb)
        wksi=self.put[3-1]/(a1*self.omb**4+self.put[3-1])
        mksi=self.put[3-1]*a1*self.omb**2/(a1*self.omb**4+self.put[3-1])/self.put[7-1]
        s1=self.s[1-1]+self.s[3-1]*(abs(wksi))**2
        for j in range(self.n1):
            for k in range(self.n1):
                x=self.ek1[4-1][j]-self.ek1[4-1][k]
                xx=x-self.put[9-1]
                for l in range(3):
                    x=xx+(l-1+1)*self.put[9-1]
                    cu1=complex(0.,-x*self.omb)
                    i=1-1
                    if x<0:
                        i=2-1
                    self.cu[3-1]=self.put[9-1]*(self.put[3-1]+self.put[2-1]*self.v[1-1]*(omb1-self.z[i]))
                    self.cu[4-1]=self.put[9-1]*(self.put[3-1]+self.put[2-1]*self.v[1-1]*(omb1-self.z[i+2]))
                    if abs(x)>2500:
                        x=2500.*(-1)**(i+1)
                    self.cu[1-1]=self.z[i]*np.exp(self.z1[i]*x)
                    self.cu[2-1]=self.z[i+2]*np.exp(self.z1[i+2]*x)
                    if l==2-1:
                        self.wy[j][k]=self.cu[1-1]+self.cu[2-1]
                        self.wyv[j][k]=self.z[1-1]*(ci*self.om-self.v[1-1]*self.z1[1-1])/abs(self.z1[1-1]) \
                         +self.z[2-1]*(ci*self.om-self.v[1-1]*self.z1[2-1])/abs(self.z1[2-1]) \
                         +self.z[3-1]*(ci*self.om-self.v[1-1]*self.z1[3-1])/abs(self.z1[3-1]) \
                         +self.z[4-1]*(ci*self.om-self.v[1-1]*self.z1[4-1])/abs(self.z1[4-1])
                        self.wshp[j][k]=self.rs[1-1]*self.wy[j][k]/(-self.om**2*self.put[8-1]+self.rs[2-1]+self.rs[1-1]+ci*self.om*(self.rs[4-1]+self.rs[3-1]))
                        self.wr[j][k]=(self.cu[1-1]*(self.v[1-1]**2*self.z1[i]**2-self.om**2-2*ci*self.om*self.v[1-1]*self.z1[i]) \
                         +self.cu[2-1]*(self.v[1-1]**2*self.z1[i+2]**2-self.om**2-2*ci*self.om*self.v[1-1]*self.z1[i+2]))/981.
                        self.wa[j][k]=self.cu[1-1]*(self.v[1-1]**2*self.z1[i]**2-self.om**2-2*ci*self.om*self.v[1-1]*self.z1[i]) \
                         *(self.rs[1-1]+self.rs[3-1]*ci*self.om-self.rs[3-1]*self.v[1-1]*self.z1[i]) \
                         +self.cu[2-1]*(self.v[1-1]**2*self.z1[i+2]**2-self.om**2-2*ci*self.om*self.v[1-1]*self.z1[i+2]) \
                         *(self.rs[1-1]+self.rs[3-1]*ci*self.om-self.rs[3-1]*self.v[1-1]*self.z1[i+2])
                        self.wa[j][k]=self.wa[j][k]/(981.*(self.rs[2-1]+self.rs[1-1]-self.om**2*self.put[8-1]+ci*self.om*(self.rs[3-1]+self.rs[4-1])))
                        self.wm[j][k]=(-a1*self.cu[1-1]*self.z1[i]**2-a1*self.cu[2-1]*self.z1[i+2]**2)/self.put[7-1]
                        self.wp[j][k]=self.wy[j][k]-self.wo[j][k]
                        self.wo[j][k]=-self.omb*self.omb*self.v[1-1]*self.v[1-1]*self.wo[j][k]/981.
                        self.ws[j][k]=(self.cu[3-1]+self.put[8-1]*(self.v[1-1]*(omb1-self.z1[i]))**2)*self.cu[1-1]+(self.cu[4-1]+self.put[8-1]*(self.v[1-1]*(omb1-self.z1[i+2]))**2)*self.cu[2-1]
                        self.sk[j][k]=s1*np.exp(cu1)
                        if hhhh!=0:
                            if(x==0):
                                cu1=hhhh
                            else:
                                cu1=complex(-np.sin(-x*(self.omb+hhhh/2.))+np.sin(-x*(self.omb-hhhh/2.)), -np.cos(-x*(self.omb+hhhh/2.))+np.cos(-x*(self.omb-hhhh/2.)))/x
                            self.sk[j][k]=s1*cu1
                        if k==j:
                            self.wp[j][k]=1./self.put[5-1]+self.wp[j][k]
                            self.sk[j][k]=self.sk[j][k]+self.s[2-1]
                        self.wb[j][k]=self.cu[1-1]*(self.rs[2-1]*(self.rs[1-1]+ci*self.om*self.rs[3-1]-self.v[1-1]*self.rs[3-1]*self.z1[i])+self.rs[4-1]*ci*self.om*(self.rs[1-1]+ci*self.om*self.rs[3-1])-self.z1[i]*self.rs[4-1]*(2*ci*self.om*self.v[1-1]*self.rs[3-1]+self.v[1-1]*self.rs[1-1])+self.rs[4-1]*self.v[1-1]**2*self.rs[3-1]*self.z1[i]**2) \
                         +self.cu[2-1]*(self.rs[2-1]*(self.rs[1-1]+ci*self.om*self.rs[3-1]-self.v[1-1]*self.rs[3-1]*self.z1[i+2])+self.rs[4-1]*ci*self.om*(self.rs[1-1]+ci*self.om*self.rs[3-1])-self.z1[i+2]*self.rs[4-1]*(2*ci*self.om*self.v[1-1]*self.rs[3-1]+self.v[1-1]*self.rs[1-1])+self.rs[4-1]*self.v[1-1]**2*self.rs[3-1]*self.z1[i+2]**2)
                        self.wb[j][k]=self.wb[j][k]/(self.rs[2-1]+self.rs[1-1]-self.om**2*self.put[8-1]+ci*self.om*(self.rs[3-1]+self.rs[4-1]))
                        if l==2-1:
                            self.sp[j][k]=self.wb[j][k]
                        elif l==1-1:
                            self.wbm[j][k]=self.wb[j][k]
                        elif l==3-1:
                            self.wbp[j][k]=self.wb[j][k]
                    else:
                        self.wb[j][k]=self.cu[1-1]*(self.rs[2-1]*(self.rs[1-1]+ci*self.om*self.rs[3-1]-self.v[1-1]*self.rs[3-1]*self.z1[i])+self.rs[4-1]*ci*self.om*(self.rs[1-1]+ci*self.om*self.rs[3-1])-self.z1[i]*self.rs[4-1]*(2*ci*self.om*self.v[1-1]*self.rs[3-1]+self.v[1-1]*self.rs[1-1])+self.rs[4-1]*self.v[1-1]**2*self.rs[3-1]*self.z1[i]**2) \
                         +self.cu[2-1]*(self.rs[2-1]*(self.rs[1-1]+ci*self.om*self.rs[3-1]-self.v[1-1]*self.rs[3-1]*self.z1[i+2])+self.rs[4-1]*ci*self.om*(self.rs[1-1]+ci*self.om*self.rs[3-1])-self.z1[i+2]*self.rs[4-1]*(2*ci*self.om*self.v[1-1]*self.rs[3-1]+self.v[1-1]*self.rs[1-1])+self.rs[4-1]*self.v[1-1]**2*self.rs[3-1]*self.z1[i+2]**2)
                        self.wb[j][k]=self.wb[j][k]/(self.rs[2-1]+self.rs[1-1]-self.om**2*self.put[8-1]+ci*self.om*(self.rs[3-1]+self.rs[4-1]))
                        if l==2-1:
                            self.sp[j][k]=self.wb[j][k]
                        elif l==1-1:
                            self.wbm[j][k]=self.wb[j][k]
                        elif l==3-1:
                            self.wbp[j][k]=self.wb[j][k]


                self.wb[j][k]=self.sp[j][k]

        # Инвертирование через NumPy
        self.wp = np.linalg.inv(self.wp)
        #self.lmcinv(self.wp,12,self.n1,1,0) #index, nerror
        #if nerror!=0:
        #    exit()

        for j in range(self.n1):
            for i in range(self.n1):
                z2=0.
                for k in range(self.n1):
                    for l in range(self.n1):
                        z2=z2+self.wp[j][l]*self.sk[k][l]*np.conj(self.wp[i][k])
                self.sp[i][j]=z2

        fz = np.ndarray((22,8), dtype=np.complex128, order='F')
        for i in range(self.n):
            for j in range(self.n1):
                fz[i][j]=0.
                for k in range(self.n1):
                    fz[i][j]=fz[i][j]+self.a[i][k]*self.wp[k][j]

        for i in range(self.n):
            for j in range(self.n):
                self.se[i][j]=0.
                for k in range(self.n1):
                    for l in range(self.n1):
                        self.se[i][j]=self.se[i][j]+fz[i][k]*self.sk[k][l]*np.conj(fz[j][l])

        for j in range(self.n1):
            self.sr[j]=0.
            self.sa[j]=0.
            self.so[j]=0.
            self.sy[j]=0.
            self.sshp[j]=0.
            self.sm[j]=0.
            self.ss[j]=0.
            self.sbm[j]=0.
            self.sbp[j]=0.
            self.sb[j]=0.
            self.sh1[j]=0.
            self.sh2[j]=0.
            self.sv[j]=0.
            for k in range(self.n1):
                for l in range(self.n1):
                    self.sv[j]=self.sv[j]+self.wyv[j][l]*self.sp[k][l]*np.conj(self.wyv[j][k])
                    self.so[j]=self.so[j]+self.wo[j][l]*self.sp[k][l]*np.conj(self.wo[j][k])
                    self.sy[j]=self.sy[j]+self.wy[j][l]*self.sp[k][l]*np.conj(self.wy[j][k])
                    self.sshp[j]=self.sshp[j]+self.wshp[j][l]*self.sp[k][l]*np.conj(self.wshp[j][k])
                    self.sr[j]=self.sr[j]+self.wr[j][l]*self.sp[k][l]*np.conj(self.wr[j][k])
                    self.sa[j]=self.sa[j]+self.wa[j][l]*self.sp[k][l]*np.conj(self.wa[j][k])
                    self.sm[j]=self.sm[j]+self.wm[j][l]*self.sp[k][l]*np.conj(self.wm[j][k])
                    self.ss[j]=self.ss[j]+self.ws[j][l]*self.sp[k][l]*np.conj(self.ws[j][k])
                    self.sh1[j]=self.sh1[j]+float((self.wbm[j][l]+self.wbp[j][l])*self.sp[k][l]*np.conj(self.wb[j][k]))
                    self.sh2[j]=self.sh2[j]+float(self.wbm[j][l]*self.sp[k][l]*np.conj(self.wbp[j][k]))
                    self.sbm[j]=self.sbm[j]+self.wbm[j][l]*self.sp[k][l]*np.conj(self.wbm[j][k])
                    self.sbp[j]=self.sbp[j]+self.wbp[j][l]*self.sp[k][l]*np.conj(self.wbp[j][k])
                    self.sb[j]=self.sb[j]+self.wb[j][l]*self.sp[k][l]*np.conj(self.wb[j][k])
        '''
        hjj1=self.wp[1-1][1-1]*np.conj(self.wp[1-1][1-1])
        hjj2=self.wo[1-1][1-1]*np.conj(self.wo[1-1][1-1])
        hjj3=self.wy[1-1][1-1]*np.conj(self.wy[1-1][1-1])
        hjj4=self.wr[1-1][1-1]*np.conj(self.wr[1-1][1-1])
        hjj5=self.wa[1-1][1-1]*np.conj(self.wa[1-1][1-1])
        hjj6=self.wm[1-1][1-1]*np.conj(self.wm[1-1][1-1])
        hjj7=self.ws[1-1][1-1]*np.conj(self.ws[1-1][1-1])
        hjj8=self.wb[1-1][1-1]*np.conj(self.wb[1-1][1-1])
        ommm=self.om/6.28
        '''




    def train(self):
        # Попытка составить матрицы А и Б
        self.n = self.n1 + 2*(self.n2+self.n3+self.n4)
        m=0
        f=0
        for k in range(self.n):
            if self.n1 > k:
                a1=self.ek1[4-1][k]
                c1=self.ek1[2-1][k]
                r1=self.ek1[3-1][k]
                mu=int(self.ek1[6-1][k])
                nu=1
                f=1
            elif self.n1 + 2*self.n2 > k:
                m=int(((k+1)-self.n1+1)/2)-1
                a1=self.ek2[4-1][m]
                b1=self.ek2[6-1][m]
                c1=self.ek2[2-1][m]
                r1=self.ek2[3-1][m]
                mu=int(self.ek2[7-1][m])
                nu=2
            elif self.n1+2*self.n2+2*self.n3 > k:
                m=int(((k+1)-self.n1-2*self.n2+1)/2)-1
                a1=self.ek3[6-1][m]
                b1=self.ek3[4-1][m]
                c1=self.ek3[2-1][m]
                r1=self.ek3[3-1][m]
                nu=3
            else:
                a1=self.ek4[3-1]
                b1=self.ek4[3-1]
                c1=0.
                r1=0.
                nu=4

            if (self.n1+2*(((k+1)-self.n1)//2)-(k+1) != 0) or (f==1):
                f=0
                # Составление уравнения типа сумма Р
                alf=complex(c1,r1*self.om)
                if c1==0 and r1==0:
                    aalf=0.
                    balf=1.
                else:
                    aalf=1.
                    balf=self.om**2/alf

                if nu==4:
                    for j in range(self.n):
                        j1=j+self.n
                        if j<self.n1:
                            mas=self.ek1[1-1][j]
                            self.a[k][j1]=balf/self.om**2
                            self.a[k][j]=balf*mas
                        else:
                            if j<self.n:
                                self.a[k][j]=0.
                            elif j==self.n:
                                self.a[k][j]=balf*self.ek4[1-1]-aalf
                            else:
                                if (j-self.n1-2*((j-self.n1)/2))==0:
                                    self.a[k][j]=0.
                                else:
                                    m=(j-self.n1+1)/2-1
                                    if m<self.n2:
                                        mas=self.ek2[1-1][m]
                                    else:
                                        m=m-self.n2
                                        mas=self.ek3[1-1][m]
                                    self.a[k][j]=balf*mas

                elif nu==3:
                    for j in range(self.n):
                        j1=j+self.n
                        if j<self.n1:
                            m1=int(self.ek1[6-1][j]-1)
                            m1=int(self.ek2[7-1][m1]-1)
                            if m==m1:
                                self.a[k][j1]=balf/self.om**2
                                mas=self.ek1[1-1][j]
                                self.a[k][j]=balf*mas
                            else:
                                self.a[k][j1]=0.
                                self.a[k][j]=0.
                        else:
                            if (j+1)-self.n1-2*self.n2<=0:
                                m1=(j+1-self.n1+1)//2-1
                                mas=self.ek2[1-1][m1]
                                m1=int(self.ek2[7-1][m1]-1)
                                if (m!=m1) or (j+1-self.n1-2*((j+1-self.n1)//2)==0):
                                    self.a[k][j]=0.
                                else:
                                    self.a[k][j]=balf*mas
                            else:
                                if j!=k:
                                    if j<k+1:
                                        self.a[k][j]=0.
                                    elif j==k+1:
                                        self.a[k][j]=aalf*(a1-b1)
                                    else:
                                        if j<self.n-1:
                                            self.a[k][j]=0.
                                        elif j==self.n-1:
                                            self.a[k][j]=aalf
                                        else:
                                            self.a[k][j]=aalf*(self.ek4[3-1]-a1)
                                else:
                                    self.a[k][j]=balf*self.ek3[1-1][m]-aalf

                elif nu==2:
                    for j in range(self.n):
                        j1=j+self.n
                        if j<self.n1:
                            m1=self.ek1[6-1][j]-1
                            if m==m1:
                                self.a[k][j1]=balf/self.om**2
                                mas=self.ek1[1-1][j]
                                self.a[k][j]=balf*mas
                            else:
                                self.a[k][j1]=0.
                                self.a[k][j]=0.
                        else:
                            if j<k:
                                self.a[k][j]=0.
                            elif j==k:
                                self.a[k][j]=balf*self.ek2[1-1][m]-aalf
                            else:
                                if j==k+1:
                                    self.a[k][j]=aalf*(a1-b1)
                                else:
                                    if (j+1)-self.n1-2*(self.n2+mu)+1 < 0:
                                        self.a[k][j]=0.
                                    elif (j+1)-self.n1-2*(self.n2+mu)+1 == 0:
                                        self.a[k][j]=aalf
                                    else:
                                        if (j+1)-self.n1-2*(self.n2+mu) == 0:
                                            self.a[k][j]=aalf*(self.ek3[6-1][mu-1]-a1)
                                        else:
                                            self.a[k][j] = 0.

                else:
                    for j in range(self.n):
                        j1=j+self.n
                        if j==k:
                            self.a[k][j1]=balf/self.om**2
                            self.a[k][j]=balf*self.ek1[1-1][j]-aalf
                        else:
                            if (j+1)-self.n1-2*mu+1==0:
                                self.a[k][j]=aalf
                            else:
                                if (j+1)-self.n1-2*mu==0:
                                    self.a[k][j]=aalf*(self.ek2[6-1][mu-1]-a1)
                                else:
                                    if j<self.n1:
                                        self.a[k][j1]=0.
                                    self.a[k][j]=0.

            else:
                if nu<3:
                    for j in range(self.n):
                        j1=j+self.n
                        if j<self.n1:
                            if self.ek1[6-1][j]==(m+1):
                                self.a[k][j1]=(a1-self.ek1[4-1][j])/self.om**2
                                self.a[k][j]=(a1-self.ek1[4-1][j])*self.ek1[1-1][j]
                            else:
                                self.a[k][j1]=0.
                                self.a[k][j]=0.
                        else:
                            if j<k:
                                if j==k-1:
                                    self.a[k][j]=(a1-b1)*self.ek2[1-1][m]
                                else:
                                    self.a[k][j]=0.
                            elif j==k:
                                self.a[k][j]=self.ek2[5-1][m]
                            else:
                                self.a[k][j] = 0.

                elif nu==3:
                    for j in range(self.n):
                        j1=j+self.n
                        if j<self.n1:
                            m1=int(self.ek1[6-1][j])-1
                            c1=b1-self.ek2[4-1][m1]
                            m1=int(self.ek2[7-1][m1])-1
                            if m==m1:
                                self.a[k][j1]=c1/self.om**2
                                self.a[k][j]=c1*self.ek1[1-1][j]
                            else:
                                self.a[k][j1]=0.
                                self.a[k][j]=0.
                        else:
                            if j<k:
                                if j==k-1:
                                    self.a[k][j]=(a1-a1)*self.ek3[1-1][m]
                                else:
                                    if j+1-self.n1-2*self.n2<=0:
                                        if j+1-2*((j+1)//2)!=0:
                                            m1=(j+1-self.n1)//2
                                            mas=self.ek2[1-1][m1]
                                            c1=self.ek2[4-1][m1]
                                            m1=int(self.ek2[7-1][m1])-1
                                            if m1==m:
                                                self.a[k][j]=mas*(b1-c1)
                                            else:
                                                self.a[k][j]=0.
                                        else:
                                            self.a[k][j]=0.
                                    else:
                                        self.a[k][j]=0.
                            elif j==k:
                                self.a[k][j]=self.ek3[5-1][m]
                            else:
                                self.a[k][j] = 0.

                else:
                    for j in range(self.n):
                        j1=j+self.n
                        if j<self.n1:
                            mas=self.ek1[1-1][j]
                            m1=int(self.ek1[6-1][j])-1
                            m1=int(self.ek2[7-1][m1])-1
                            self.a[k][j1]=(b1-self.ek3[4-1][m1])/self.om**2
                            self.a[k][j]=mas*(b1-self.ek3[4-1][m1])
                        else:
                            if j<self.n-1:
                                m1=(j-self.n1+1)//2-1
                                if self.n1+2*m1==j+1:
                                    self.a[k][j]=0.
                                else:
                                    if m1<self.n2:
                                        mas=self.ek2[1-1][m1]
                                        m1=int(self.ek2[7-1][m1])-1
                                        self.a[k][j]=mas*(b1-self.ek3[4-1][m1])
                                    else:
                                        m1=m1-self.n2
                                        if m1<self.n3:
                                            self.a[k][j]=self.ek3[1-1][m1]*(a1-self.ek3[4-1][m1])
                                        else:
                                            self.a[k][j]=0.
                            else:
                                self.a[k][j]=self.ek4[2-1]

        #Финальные манипуляции с матрицами
        ak = np.ndarray((self.n,self.n),dtype=np.complex128, order='F')
        bk = np.ndarray((self.n,self.n),dtype=np.complex128, order='F')
        for i in range(self.n):
            for j in range(self.n):
                ak[i][j]=self.a[i][j]
                if j<self.n1:
                    bk[i][j]=self.a[i][j+self.n]

        ak=np.linalg.inv(ak)

        for i in range(self.n):
            for j in range(self.n1):
                self.a[i][j]=0.
                for k in range(self.n):
                    self.a[i][j]=self.a[i][j]+ak[i][k]*bk[k][j]

        for i in range(self.n1):
            for j in range(self.n1):
                self.wo[i][j]=self.a[i][j]

    def start(self, cursor, id_input):
        if not sys.warnoptions:
            warnings.simplefilter("ignore")
        t = time.time()
        print('callLOAD')
        self.load_from_db(cursor, id_input)
        print(time.time() - t)
