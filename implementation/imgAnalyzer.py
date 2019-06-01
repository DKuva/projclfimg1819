import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

class imgAnalyzer():

    def __init__(self):
        self.signData = 0

    def getColourCode(self,workImg):
        #Detektiraj boje u slici
        #Kod samo uzme HSV sliku i broji svaki piksel u određenom područiju H-kanala
        red = 0 
        blue = 0
        green = 0
        yellow = 0
        for i in range(workImg.shape[0]):
            for j in range(workImg.shape[1]):
                if (workImg[i,j,0] > 340 or workImg[i,j,0] < 20): red += 1
                if (workImg[i,j,0] > 170 and workImg[i,j,0] < 250): blue += 1
                if (workImg[i,j,0] > 100 and workImg[i,j,0] < 140): green += 1
                if (workImg[i,j,0] > 30 and workImg[i,j,0] < 90): yellow += 1
                                
        area = workImg.shape[0]*workImg.shape[1]
        #Izračunaj koncentraciju neke boje na slici, ako je količina boje pre mala, zanemari je.
        list = [red/area, blue/area, green/area, yellow/area]
        colourCode = []

        if (red/area >= 0.1): colourCode.append(1)             
        if (blue/area >= 0.1): colourCode.append(2)             
        if (green/area >= 0.1): colourCode.append(3)         
        if (yellow/area >= 0.1): colourCode.append(4) 
                    
        print('Colour presence= ' + str(red/area) +' '+ str(blue/area) + ' ' +str(green/area) + ' ' +str(yellow/area)+ ' ' +str(colourCode))
        return(colourCode)
    def shapeDetector(self, invMoment):

        #za ulazni moment, identificiraj oblik
        #kriteriji za oblik su eksperimentalni, invarijantni moment ne ovisi o rotaciji ni veličini samog oblika.

        shape = "undefined"
        tolerance = 1

        if  abs(invMoment - 50) < tolerance:
            shape = "triangle"
        elif abs(invMoment - 30) < tolerance:
            shape = "square"
        elif abs(invMoment - 30) < tolerance:
            shape ="pentagon"
        elif abs(invMoment - 15) < tolerance:
            shape ="circle"          

        return shape

    def getShapeCode(self,workImg,colourCode):

        #Detektiraj oblik znaka i simbola
        #za svaku detektiranu boju na slici, filtriraj tu boju, te izračunaj invarijantni moment binarne maske te slike, te s tim podatkom identificiraj oblik

        low_blue = np.array([110,10,10])
        up_blue = np.array([130,255,255])
        low_red = np.array([0,10,10])
        up_red = np.array([20,255,255])
        low_green = np.array([50,10,10])
        up_green = np.array([70,255,255])
        low_yellow = np.array([20,10,10])
        up_yellow = np.array([40,255,255])
        colourString = ["red", "blue", "green", "yellow"]
        mask = []
        moments = []
        for i in range(len(colourCode)):
            if (colourCode[i] == 0): print("cannot detect sign, colourCode = 0")
            if (colourCode[i] == 1): mask.append(cv.inRange(workImg, low_red, up_red))
            if (colourCode[i] == 2): mask.append(cv.inRange(workImg, low_blue, up_blue))
            if (colourCode[i] == 3): mask.append(cv.inRange(workImg, low_green, up_green))
            if (colourCode[i] == 4): mask.append(cv.inRange(workImg, low_yellow, up_yellow))
        
        
        for i in range(len(mask)):
             M = cv.moments(mask[i-1])
             I1 = M["mu11"]/M["m00"]
             I2 = (1000*M["mu21"]*M["mu12"])/(M["m00"]**4)
             print('Inv moment I1 = ' + str(M["mu11"]/M["m00"]))
             plt.imshow(mask[i-1],cmap='gray')          
             plt.show()

             shape = self.shapeDetector(I1)
             if shape == "undefined" : del mask[i-1]
             else: 
                 moments.append({colourString[i-1],shape,I1,I2})
        
        

        print ('Full desc= ' + str(moments))
        shapeCode = 0
        return(shapeCode)
    def describe(self, colourCode, shapeCode, signkey):

        if (colourCode == 0): print("cannot detect sign colour, colourCode = 0")
        if (colourCode == 1): colour = 'red'
        if (colourCode == 2): colour = 'blue'
        if (colourCode == 3): colour = 'green'
        if (colourCode == 4): colour = 'yellow'

    def analyzeImg(self,workImg):
        #Glavni Kod, prolaz roz odo daje konačni rezultat
        #uzmi sliku ->detektiraj sve boje i njihove koncentracije ->segmentiraj sliku po bojama te ovisno o momentu segmenta detektirat oblik segmenta -> eliminirat segmente tako da ostane samo
        # crna ili bijela boja (simbol na sredini znaka) -> izračunat moment simbola -> boju, oblik, i invarijantni moment znaka vratit kao povratnu informaciju

        workImg = cv.cvtColor(workImg, cv.COLOR_BGRA2BGR)
        cv.imshow('img',workImg)
        cv.waitKey(0)
        workImg = cv.cvtColor(workImg, cv.COLOR_BGR2HSV)

        colourCode = self.getColourCode(workImg)
        shapeCode = self.getShapeCode(workImg,colourCode)
        
        return(0)
