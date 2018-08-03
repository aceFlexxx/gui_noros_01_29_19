#! /usr/bin/python
import wx
import wx.xrc
import numpy as np
import math as m
import pyautogui as pyg
import csv

class Sinusoidal():

    def __init__(self):
        self.width,self.height = pyg.size()
        self.half_w = self.width/2
        self.half_h = self.height/2
        #used to loop around column to thicken path
        self.offset = int(m.ceil(self.height*.01))




    def SinWave(self):
        ev = np.ones(shape=(self.width,self.height))
        ufm = np.zeros(shape=(self.width,self.height))
        for i in range(self.width):
            for j in range(self.height):
                if j == self.half_h + int(self.half_h*np.sin(i/self.width*5*2*np.pi)):
                    ev[i][j]=0
                    ufm[i][j]=1
                    for k in range(j-self.offset,j+self.offset+1):
                        ufm[i][k]=1

        self.ev_sin = ev
        self.ufm_sin = ufm

    def CosWave(self):
        ev = np.ones(shape=(self.width,self.height))
        ufm = np.zeros(shape=(self.width,self.height))
        for i in range(self.width):
            for j in range(self.height):
                if j == self.half_h + self.half_h*np.cos(i/self.width*5*2*np.pi):
                    ev[i][j]=0
                    ufm[i][j]=1
                    for k in range(j-self.offset,j+self.offset+1):
                        ufm[i][k]=1
        self.ev_cos = ev
        self.ufm_sin = ufm

if __name__ == "__main__":
    sin = Sinusoidal()
    sin.SinWave()
    cos = Sinusoidal()
    cos.CosWave()

    with open("ev.csv","w+") as mycsv:
        writer = csv.writer(mycsv,delimiter = ',')
        writer.writerows(sin.ev_sin)
