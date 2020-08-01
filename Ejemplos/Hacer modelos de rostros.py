import cv2
import os
import numpy as np

dataPath = 'C:/Users/Gaby/Desktop/Reconocimiento Facial/Data' #Cambia a la ruta donde hayas almacenado Data
peopleList = os.listdir(dataPath)
print('Lista de personas: ', peopleList)

labels = []
facesData = []
label = 0

for nameDir in peopleList:
	personPath = dataPath + '/' + nameDir

	for fileName in os.listdir(personPath):
		labels.append(label)
		facesData.append(cv2.imread(personPath+'/'+fileName,0))
	label = label + 1

face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Entrenando el reconocedor de rostros
face_recognizer.train(facesData, np.array(labels))

face_recognizer.write('modeloLBPHFace.xml')
