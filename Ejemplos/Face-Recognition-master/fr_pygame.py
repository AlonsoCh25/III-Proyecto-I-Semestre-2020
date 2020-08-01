import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from time import sleep
import pygame
from pygame.locals import *
import sys
from CLASSES import *
show_search = False
show_done = False

def get_encoded_faces():
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(im):
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    img = cv2.imread("faces_unknown/"+im, 1)

 
    face_locations = fr.face_locations(img)
    unknown_face_encodings = fr.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = fr.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)

    return face_names


def window_pygame():
    global show_search, show_done
    
    camera = cv2.VideoCapture(0)
    pygame.init()
    pygame.display.set_caption("Login")
    weight, height = 952,768
    screen = pygame.display.set_mode((weight,height))
    
    background = pygame.image.load("Images/background.png")
    check = pygame.image.load("Images/check.png")
    check_1 = pygame.image.load("Images/check_1.png")
    cursor =  Cursor()
    button = Button(check,check_1, 400, 500,80,80)
    show_camera = True
    exit_ = False
    
    while exit_ != True:
        screen.blit(pygame.transform.scale(background,(weight,height)),(0,0))
        ret, frame_ = camera.read()
        cursor.update()
        button.update(screen,cursor)
        
        if show_camera:
            frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (150,0))
            pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit
                exit_ = True
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(button.rect):
                    for i in range(1):
                        cv2.imwrite("faces_unknown/unknown"+str(i)+".png", frame_)
                    for dirpath, dnames, fnames in os.walk("./faces_unknown"):
                        for f in fnames:
                            if f.endswith(".jpg") or f.endswith(".png"):
                                print(type(f))
                                classify_face(f)
                                
                


window_pygame()
