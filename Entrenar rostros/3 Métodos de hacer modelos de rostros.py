"""
Este programa asigna un label diferente a los rostros que se encuentran en carpetas distintas, por lo contrario 
"""

import cv2
import os
import numpy as np

dataPath = r"C:\Users\Diego García\Desktop\Reconocimiento Facial\Data" #Cambia a la ruta donde hayas almacenado Data

"""
Esto solo es necesario si los rostros estan almacenados en carpetas
peopleList = os.listdir(dataPath)
print('Lista de personas: ', peopleList)
""" 

#Para presentar las personas a la computadora, (es para que sepa de quien se trata)
labels = [] #Para poner las etiquetas
facesData = [] 
label = 0

for nameDir in peopleList:
	personPath = dataPath + '/' + nameDir #Esta es la ruta del directorio donde estan los rostros
	print('Leyendo las imágenes')

	#leer cada rostro
	for fileName in os.listdir(personPath):
		print('Rostros: ', nameDir + '/' + fileName)
		labels.append(label)
		facesData.append(cv2.imread(personPath+'/'+fileName,0))
	label = label + 1 #Agregar una etiqueta a cada rostro

#Para ver la cantidad de etiquetas y la cantidad de rostros con la etiqueta 0,1,2.... la cantidad que haya especificado
#print('labels= ',labels)
#print('Número de etiquetas 0: ',np.count_nonzero(np.array(labels)==0))
#print('Número de etiquetas 1: ',np.count_nonzero(np.array(labels)==1))

# Métodos para entrenar el reconocedor (Son estos tres cualquiera sirve)
#face_recognizer = cv2.face.EigenFaceRecognizer_create()
#face_recognizer = cv2.face.FisherFaceRecognizer_create()
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Entrenando el reconocedor de rostros
face_recognizer.train(facesData, np.array(labels))

# Almacenando el modelo obtenido
#face_recognizer.write('modeloEigenFace.xml')
#face_recognizer.write('modeloFisherFace.xml')
face_recognizer.write('modeloLBPHFace.xml')
print("Modelo almacenado...")