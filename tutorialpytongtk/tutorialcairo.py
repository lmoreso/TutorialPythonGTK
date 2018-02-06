import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import random
import math

bdebug = True

class Bezier():
    def_punts = [(-2, 3), (-2, 5), (2, 5), (2, 3)]
    def_tini = -1.0
    def_tend = 2.0
    def_paso = 0.05
    
    pa = ()
    pb = ()
    pc = ()
    pd = ()
    tini = 0
    tend = 0
    paso = 0
    lststore = 0
    
    def __init__(self, lststore):
        self.lststore = lststore
        self.set_bezier(self.def_punts, self.def_tini, self.def_tend, self.def_paso)       
    
    def set_bezier(self, punts, tini, tend, paso):
        self.pa = punts[0]
        self.pb = punts[1]
        self.pc = punts[2]
        self.pd = punts[3]
        self.tini = tini
        self.tend = tend
        self.paso = paso
        self.regenera_punts()
        
    def regenera_punts(self):
        self.lststore.clear()

        if bdebug:
            print("regenera_punts")
            indent = "    "
            print("\n" + indent, "tini".rjust(6), "tfin".rjust(6), "paso".rjust(6))
            print(indent, "=====".rjust(6), "=====".rjust(6), "=====".rjust(6))
            print(indent, str(self.tini).rjust(6), str(self.tend).rjust(6), str(self.paso).rjust(6))
            print("\n" + indent, "punto".rjust(6), "X".rjust(6), "Y".rjust(6))
            print(indent, "=====".rjust(6), "=====".rjust(6), "=====".rjust(6))
            print(indent, "pa".rjust(6), str(self.pa[0]).rjust(6), str(self.pa[1]).rjust(6))
            print(indent, "pb".rjust(6), str(self.pb[0]).rjust(6), str(self.pb[1]).rjust(6))
            print(indent, "pc".rjust(6), str(self.pc[0]).rjust(6), str(self.pc[1]).rjust(6))
            print(indent, "pd".rjust(6), str(self.pd[0]).rjust(6), str(self.pd[1]).rjust(6))
            print("\n" + indent, "t".rjust(6), "X".rjust(8), "Y".rjust(8))
            print(indent, "=====".rjust(6), "=======".rjust(8), "=======".rjust(8))
            
        paso = int(round(self.paso * 100, 0))
        tini = int(round(self.tini * 100, 0))
        tend = int(round(self.tend * 100, 0))
        for tt in range (tini, tend + paso, paso):
            t = tt / 100.0
            x = self.pa[0] * ((1 - t) ** 3) + 3 * self.pb[0] * t * ((1 - t) ** 2) + 3 * self.pc[0] * (t ** 2) * (1 - t) + self.pd[0] * (t ** 3)
            y = self.pa[1] * ((1 - t) ** 3) + 3 * self.pb[1] * t * ((1 - t) ** 2) + 3 * self.pc[1] * (t ** 2) * (1 - t) + self.pd[1] * (t ** 3)
            listiter = self.lststore.append([round(x, 3), round(y, 3), str(t)])  
            if bdebug:
                print(indent, '{0:>6.2f} {0:>8.3f} {1:>8.3f}'.format(t, round(x, 3), round(y, 3)))

        