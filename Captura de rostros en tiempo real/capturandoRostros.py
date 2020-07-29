import cv2
import os
import imutils

faceClassif = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #Se utiliza para la captura de rostros
personName = "Diego"
dataPath =(r"C:\Users\Diego García\Desktop\6 RECONOCIMIENTO FACIAL") #Ruta donde se deseean almacenar los rostros
personPath = dataPath + "/" + personName
#Crear carpeta con el nombre del usuario
if not os.path.exists(personPath):
	print("Carpeta creada: ",personPath)
	os.makedirs(personPath)


cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

count = 0
#Loop para realizar las capturas y modificaciones al rostro
while True:

	ret, frame = cap.read()
	if ret == False: break
	frame =  imutils.resize(frame, width=640)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	auxFrame = frame.copy()

	faces = faceClassif.detectMultiScale(gray,1.3,5)

	for (x,y,w,h) in faces:
		cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
		rostro = auxFrame[y:y+h,x:x+w]
		rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
		cv2.imwrite('Data/rotro_{}.jpg'.format(count),rostro)
		count = count + 1
	cv2.imshow('frame',frame)
#Realiza 300 capturas del rostro
	k =  cv2.waitKey(1)
	if k == 27 or count >= 300:
		break

cap.release()
cv2.destroyAllWindows()
