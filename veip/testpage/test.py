def arrset(k,par):
    arr=[]
    i=0
    while i<4:
        mas=[]
        mas.append(i+1)
        mas.append(par[k][i])
        mas.append(par[k+1][i])
        arr.append(mas)
    return arr


if __name__=="__main__":
    res=[["1","0.02","0.02"], ["2","0.201","0.045"],["3","0.02556", "0.005"], ["4","0.546","0.02"]]
