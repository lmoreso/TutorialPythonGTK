import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import random
import math

bdebug = True

def describeTramo(desde, hasta, paso):
    txt = "Desde {0:> 3.3f} hasta {1:> 3.3f} ({2:>3.3f})".format(desde, hasta, paso)
    
    return txt

def elipsePointY(x, ancho, alto, esArriba = True, redondeo = 3):
    y = round(math.sqrt((1 - (x ** 2) / (ancho ** 2)) * (alto ** 2)), redondeo)
    if not esArriba:
        y = -y
    
    return y

def Elipse(lstStore, fAncho = 5, fAlto = 4, lstTramos = [(0.25, 0.025), (1, 0.1), (0, 0.25)]):
    lstStore.clear()
    numTramos = len(lstTramos)
    cntPunts = 0

    if bdebug:
        print ("numTramos = {0}".format(numTramos))
        print ("lstTramos = {0}".format(lstTramos))
    
    # calcular el primer arco de 4
    iTramo = 0
    xIni = -fAncho
    fAnchoAcum = 0
    bContinuar = True
    while iTramo < numTramos or bContinuar:
        fAnchoTramo = lstTramos[iTramo][0]
        fPaso = lstTramos[iTramo][1]
        if fAnchoTramo <= 0 or iTramo == numTramos - 1:    #último tramo
            fAnchoTramo = (fAncho / 2.0) - fAnchoAcum
            xFin = 0
            bContinuar = False
        else:
            xFin = xIni + fAnchoTramo
        x = xIni
        xIni += fAnchoTramo  
        
        sDesc = describeTramo(x, xFin, fPaso)
        if bdebug:
            print ("nº = {0} | x = {1} | xFin = {2} | paso = {3} ".format(iTramo, x, xFin, fPaso))
        while x < xFin:
            cntPunts += 1
            y = elipsePointY(x, fAncho, fAlto)
            listiter = lstStore.append([x, y, "{0:3d}) {1}".format(int(cntPunts), sDesc)]) 
            x += fPaso
        
        iTramo += 1
        
    # pongo el último punto del primer arco (x = 0)
    cntPunts += 1
    x = 0
    y = elipsePointY(x, fAncho, fAlto)
    listiter = lstStore.append([x, y, "{0:3d}) {1}".format(int(cntPunts), sDesc)]) 
            
    # el segundo arco es igual al primero pero con las x cambiadas de signo y en orden contrario
    iLst = len(lstStore) - 2
    while iLst >= 0:
        cntPunts += 1
        listiter = lstStore.append([-lstStore[iLst][0], lstStore[iLst][1], "{0:3d})".format(int(cntPunts))]) 
        iLst -= 1

    # el 3o y 4o es igual a los dos primeros pero con las x en orden contrario y las y cambiadas de signo
    iLst = len(lstStore) - 2
    while iLst >= 0:
        cntPunts += 1
        listiter = lstStore.append([lstStore[iLst][0], -lstStore[iLst][1], "{0:3d})".format(int(cntPunts))]) 
        iLst -= 1
    
def Bezier(lstStore, tIni = -1.0, tFin = 2.0, fPaso = 0.05, lstPunts = [(-2, 3), (-2, 5), (2, 5), (2, 3)]):
    lstStore.clear()
    pa = lstPunts[0]
    pb = lstPunts[1]
    pc = lstPunts[2]
    pd = lstPunts[3]
        
    if bdebug:
        print("Bezier")
        indent = "    "
        print("\n" + indent, "tIni".rjust(6), "tFin".rjust(6), "fPaso".rjust(6))
        print(indent, "=====".rjust(6), "=====".rjust(6), "=====".rjust(6))
        print(indent, str(tIni).rjust(6), str(tFin).rjust(6), str(fPaso).rjust(6))
        print("\n" + indent, "lstPunts".rjust(6), "X".rjust(6), "Y".rjust(6))
        print(indent, "=====".rjust(6), "=====".rjust(6), "=====".rjust(6))
        print(indent, "pa".rjust(6), str(pa[0]).rjust(6), str(pa[1]).rjust(6))
        print(indent, "pb".rjust(6), str(pb[0]).rjust(6), str(pb[1]).rjust(6))
        print(indent, "pc".rjust(6), str(pc[0]).rjust(6), str(pc[1]).rjust(6))
        print(indent, "pd".rjust(6), str(pd[0]).rjust(6), str(pd[1]).rjust(6))
        print("\n" + indent, "t".rjust(6), "X".rjust(8), "Y".rjust(8))
        print(indent, "=====".rjust(6), "=======".rjust(8), "=======".rjust(8))

    paso = int(round(fPaso * 100, 0))
    tini = int(round(tIni * 100, 0))
    tend = int(round(tFin * 100, 0))
    for tt in range (tini, tend + paso, paso):
        t = tt / 100.0
        x = pa[0] * ((1 - t) ** 3) + 3 * pb[0] * t * ((1 - t) ** 2) + 3 * pc[0] * (t ** 2) * (1 - t) + pd[0] * (t ** 3)
        y = pa[1] * ((1 - t) ** 3) + 3 * pb[1] * t * ((1 - t) ** 2) + 3 * pc[1] * (t ** 2) * (1 - t) + pd[1] * (t ** 3)
        listiter = lstStore.append([round(x, 3), round(y, 3), str(t)])  
        if bdebug:
            print(indent, '{0:>6.2f} {0:>8.3f} {1:>8.3f}'.format(t, round(x, 3), round(y, 3)))
    
                
