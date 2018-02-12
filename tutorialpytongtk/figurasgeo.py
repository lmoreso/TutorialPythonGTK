import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import random
import math

bdebug = True

def hiperbolaPointY(x, fCoef, fDespl):
    if x != 0: 
        y = round(fCoef / x + fDespl, 3)
    else:
        y = 0
        
    return y

def Hiperbola(lstStore, fCoef = 1, fDespl = 0):
    lstStore.clear()
    cntPunts = 0

    if bdebug:
        print("Hiperbola")
        print ("    fCoef = {0}  fDespl = {1}".format(fCoef, fDespl))

    paso = 50
    for xx in range(-900, -150, paso):
        cntPunts += 1
        x = xx / 100.0
        if x != 0: 
            y = hiperbolaPointY(x, fCoef, fDespl)
            listiter = lstStore.append([x, y, "{0:0>3d})".format(int(cntPunts))])     
    paso = 10
    for xx in range(-150, 150, paso):
        cntPunts += 1
        x = xx / 100.0
        if x != 0: 
            y = hiperbolaPointY(x, fCoef, fDespl)
            listiter = lstStore.append([x, y, "{0:0>3d})".format(int(cntPunts))])     
    paso = 50
    for xx in range(150, 900 + paso, paso):
        cntPunts += 1
        x = xx / 100.0
        if x != 0: 
            y = hiperbolaPointY(x, fCoef, fDespl)
            listiter = lstStore.append([x, y, "{0:0>3d})".format(int(cntPunts))])     

def describeTramo(iTramo, desde, hasta, paso):
    txt = "T{0:0>2d}) desde {1:> 3.3f} hasta {2:> 3.3f} ({3:>5.5f})".format(iTramo, desde, hasta, paso)
    
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
        print("Elipse")
        print ("    fAncho = {0}  fAlto = {1}".format(fAncho, fAlto))
        print ("    numTramos = {0}".format(numTramos))
        print ("    lstTramos = {0}".format(lstTramos))
    
    # calcular el primer arco de 4
    iTramo = 0
    xIni = -fAncho
    fAnchoAcum = 0
    bContinuar = True
    while iTramo < numTramos and bContinuar:
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
        
        sDesc = describeTramo(iTramo, x, xFin, fPaso)
        if bdebug:
            print ("nº = {0} | x = {1} | xFin = {2} | paso = {3} ".format(iTramo, x, xFin, fPaso))
        while x < xFin:
            cntPunts += 1
            y = elipsePointY(x, fAncho, fAlto)
            listiter = lstStore.append([x, y, "{0:0>3d}) {1}".format(int(cntPunts), sDesc)]) 
            x += fPaso
        
        iTramo += 1
        
    # pongo el último punto del primer arco (x = 0)
    cntPunts += 1
    x = 0
    y = elipsePointY(x, fAncho, fAlto)
    listiter = lstStore.append([x, y, "{0:0>3d}) {1}".format(int(cntPunts), sDesc)]) 
            
    # el segundo arco es igual al primero pero con las x cambiadas de signo y en orden contrario
    iLst = len(lstStore) - 2
    while iLst >= 0:
        cntPunts += 1
        listiter = lstStore.append([-lstStore[iLst][0], lstStore[iLst][1], "{0:0>3d})".format(int(cntPunts))]) 
        iLst -= 1

    # el 3o y 4o es igual a los dos primeros pero con las x en orden contrario y las y cambiadas de signo
    iLst = len(lstStore) - 2
    while iLst >= 0:
        cntPunts += 1
        listiter = lstStore.append([lstStore[iLst][0], -lstStore[iLst][1], "{0:0>3d})".format(int(cntPunts))]) 
        iLst -= 1
    
def Logaritm(lstStore, fBase = 2, fCoefX = 1, fDesplX = -10, fDesplY = 3, 
    fInicio = 0.0001, lstTramos = [(0.001, 0.00025), (0.01, 0.0025), (0.05, 0.01), (0.5, 0.1), (2, 0.25), (8, 0.5), (25, 1)]):
    numTramos = len(lstTramos)
    if fBase <= 1:
        fBase = math.e
        
    if bdebug:
        print("Logaritm")
        print ("    fBase = {0}  fCoefX = {1}  fDesplX = {2}  fDesplY = {3}".format(fBase, fCoefX, fDesplX, fDesplY))
        print ("    fInicio = {0}  numTramos = {1} ".format(fInicio, numTramos))
        print ("    lstTramos = {0}".format(lstTramos))
        
    lstStore.clear()
    cntPunts = 0
    x = fInicio
    for iTramo in range(0, numTramos):
        xFin = lstTramos[iTramo][0]
        fPaso = lstTramos[iTramo][1]
        sDesc = describeTramo(iTramo, x + fDesplX, xFin + fDesplX, fPaso)
        while x < xFin:
            cntPunts += 1
            y = round(math.log(x, fBase), 3)
            listiter = lstStore.append([x + fDesplX, y + fDesplY, "{0:0>3d}) {1}".format(int(cntPunts), sDesc)]) 
            x += fPaso

def Bezier(lstStore, tIni = -1.0, tFin = 2.0, fPaso = 0.05, lstPunts = [(-2, 3), (-2, 5), (2, 5), (2, 3)]):
    lstStore.clear()
    cntPunts = 0
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
        cntPunts += 1
        t = tt / 100.0
        x = pa[0] * ((1 - t) ** 3) + 3 * pb[0] * t * ((1 - t) ** 2) + 3 * pc[0] * (t ** 2) * (1 - t) + pd[0] * (t ** 3)
        y = pa[1] * ((1 - t) ** 3) + 3 * pb[1] * t * ((1 - t) ** 2) + 3 * pc[1] * (t ** 2) * (1 - t) + pd[1] * (t ** 3)
        listiter = lstStore.append([round(x, 3), round(y, 3), '{0:0>3d}) t = {1:> 6.2f}'.format(int(cntPunts), t)])  
        if bdebug:
            print(indent, '{0:>6.2f} {1:>8.3f} {2:>8.3f}'.format(t, x, y))

def Sinus(lstStore, bCos = False, fAltura = 5.0, fPasoFraccionPi = 0.05):
    lstStore.clear()
    cntPunts = 0
    fPaso = fPasoFraccionPi * math.pi
    xIni = (-80) * fPaso 
    xFin = -xIni
    if bCos:
        fMat = math.cos
    else:
        fMat = math.sin

    if bdebug:
        print("Sinus")
        print ("    fAltura = {0} fPasoFraccionPi = {1} fPaso = {2} xIni = {3}".format(fAltura, fPasoFraccionPi, fPaso, xIni))

    x = xIni
    while x <= xFin + fPaso:
        cntPunts += 1
        y = round(fAltura * fMat(x), 3)
        listiter = lstStore.append([x, y, "{0:0>3d})".format(int(cntPunts))]) 
        x += fPaso

    x = xFin
    while x >= xIni - fPaso:
        cntPunts += 1
        y = round((-fAltura) * fMat(x), 3)
        listiter = lstStore.append([x, y, "{0:0>3d})".format(int(cntPunts))]) 
        x -= fPaso

def Parabola(lstStore, a = 0.40, b = 0, c = -5.8, fPaso = 0.25):
    if bdebug:
        print("Parabola")
        print ("    a = {0} b = {1} c = {2} fPaso = {3}".format(a, b, c, fPaso))

    lstStore.clear()
    cntPunts = 0
    paso = int(fPaso * 1000)
    for xx in range(-6000, 6000 + paso, paso):
        cntPunts += 1
        x = xx / 1000.0
        y = round(a * (x ** 2) + b * x + c, 3)
        listiter = lstStore.append([x, y, "{0:0>3d})".format(int(cntPunts))])  

def Recta(lstStore, fCoefX = 0.5, fDesplY = 1, fIni = -8, fPaso = 1):
    if bdebug:
        print("Recta")
        print ("    fCoefX = {0} fDesplY = {1} fIni = {2} fPaso = {3}".format(fCoefX, fDesplY, fIni, fPaso))

    lstStore.clear()
    cntPunts = 0
    for x in range(fIni, -fIni):
        cntPunts += 1
        y = round(fCoefX * x + fDesplY, 3)
        listiter = lstStore.append([x, y, "{0:0>3d})".format(int(cntPunts))])  

    
                
