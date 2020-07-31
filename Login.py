from reportlab.pdfbase.ttfonts import TTFont
import face_recognition as fr
import face_recognition
import os
import cv2
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
import pygame
from pygame.locals import *
from CLASSES import *
from datetime import datetime
import numpy as np
import time
import sys
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from time import sleep

pdfmetrics.registerFont(TTFont('times','times.ttf'))
pdfmetrics.registerFont(TTFont('timesb','timesbd.ttf'))
archive_csv = csv_class("Services.csv","rt")
matrix_services = archive_csv.get_matrix()
box_group = pygame.sprite.Group()
buttons = []

archive_c = csv_class("data_users.csv","rt")
matrix_data = archive_c.get_matrix()

buttons_box = pygame.sprite.Group()
buttons_services = []
show_services = False
rect_select = None
show_search = False
show_camera = True
show_done = False
name = "Unknown"


"""Funtions for Face Recognition"""

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
    global name, show_camera
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    img = cv2.imread("faces_unknown/"+im, 1)

 
    face_locations = fr.face_locations(img)
    unknown_face_encodings = fr.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        matches = fr.compare_faces(faces_encoded, face_encoding)
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            print(name)
            show_camera = False
        
        face_names.append(name)

    return face_names

"""Functions for manege the matrix"""
def draw_matrix(screen,y):
    global box_group, matrix, buttons
    trans = pygame.image.load("Images/transparent.png")
    #Matrix of the items
    x = 0
    row = 0
    box_group.empty()
    buttons = []
    for line in matrix:
        row +=1
        colum = 0
        x = 0
        y += 30          
        if True:
            for element in line:
                if colum == 0:
                    colum += 1
                    x += 150
                    box = text_group(x,y,330,30, element, row-1, colum-1)
                    box_group.add(box)
                    if row-1 > 0:
                        bt_transparent = Button_(trans,trans,x,y,320,30, row-1, colum-1)
                        buttons += [bt_transparent]
                else:
                    if colum == 1:
                        colum += 1
                        x += 330
                        box = text_group(x,y,90,30, element, row-1, colum-1)
                        box_group.add(box)
                    else:
                        colum += 1
                        x += 90
                        box = text_group(x,y,90,30, element, row-1, colum-1)
                        box_group.add(box)

def draw_matrix_services(screen, y):
    global matrix_services, buttons_services, buttons_box, show_services
    check = pygame.image.load("Images/check_s.png")
    check_s = pygame.image.load("Images/check_s_.png")
    #Matrix of the items
    row = 0
    y = y + 30
    colum = 0
    x = 150
    buttons_services = []
    buttons_box.empty()
    
    for line in matrix_services:
        txt = ""
        for element in line:
            txt += element
        bt_transparent = Button_(check,check_s,x+335,y,30,30, row, colum)
        buttons_services += [bt_transparent]
        box = text_group(x,y,330,30, txt, row, colum)
        buttons_box.add(box)
        txt = " "
        y += 30
        row += 1
        colum += 1
            


def eliminate_row_matrix(screen, B_y):
    global matrix
    m = []
    for i in range(len(matrix)-1):
        m += [matrix[i]]
    matrix = m
    draw_matrix(screen,B_y)
        
def add_row_matrix(screen, B_y):
    global matrix
    matrix += [["","","",""]]
    draw_matrix(screen,B_y)


    

"""Windows Functions"""
def login_window():
    global show_search, show_done, show_camera, name
    
    camera = cv2.VideoCapture(0)
    pygame.init()
    pygame.display.set_caption("Login")
    weight, height = 952,768
    screen = pygame.display.set_mode((weight,height))
    
    #Font
    font = pygame.font.Font("times.ttf", 60)
    font_n = pygame.font.Font("timesbd.ttf", 30)
    
    background = pygame.image.load("Images/background.png")
    check = pygame.image.load("Images/check.png")
    check_1 = pygame.image.load("Images/check_1.png")
    cursor =  Cursor()
    button = Button(check,check_1, 400, 500,80,80)
    
    
    
    exit_ = False
    while exit_ != True:
        screen.blit(pygame.transform.scale(background,(weight,height)),(0,0))
        ret, frame_ = camera.read()
        cursor.update()
        
        if show_camera:
            frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (150,0))
            button.update(screen,cursor)
            pygame.display.update()
        if not show_camera:
            Welcome = "Welcome " + name
            Welcome = font.render(Welcome, True, (0, 0, 0))
            screen.blit(Welcome, (250,200))
            pygame.display.update()
            sleep(2)
            exit_ = True
            pygame.quit()
            main_menu_window()
            camera.release()
            break

            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit
                exit_ = True
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(button.rect):
                    if show_camera:
                        for i in range(1):
                            cv2.imwrite("faces_unknown/unknown"+str(i)+".png", frame_)
                        for dirpath, dnames, fnames in os.walk("./faces_unknown"):
                            for f in fnames:
                                if f.endswith(".jpg") or f.endswith(".png"):
                                    print(type(f))
                                    classify_face(f)
                    if not show_camera:
                        pass

def make_invoice_window():
    global box_group, matrix_data, window_c,buttons, show_services,matrix_services, buttons_services, buttons_box,matrix, rect_select
    def create_pdf():
        global matrix
        ##La parte superior en y es 800
        ##El limite izquierdo en y es 50
        ##El limite derecho en y es 500
        n_pdf = pdf(inv_number, "logo.png")
        n_pdf.write_string("3C Landscaping services", 50,650,"timesb",12)
        
        txt_data = ""
        for row in matrix_data:
            for element in row:
                txt_data += str(element)
                txt_data += "\n"
        n_pdf.write_text(txt_data,50,635,"times", 12)
        txt_data = ""
        n_pdf.write_string("3C Landscaping services", 50,650,"timesb",12)
        n_pdf.write_string(("Invoice #" + inv_number), 400,650,"times",12)
        n_pdf.write_string(("Invoice Date " + str(now.date())), 400,635,"times",12)
        n_pdf.write_string(("Due Date " + due_input.get_text()), 400,620,"times",12)
        n_pdf.write_string("Bill To", 50,590,"timesb",12)
        n_pdf.write_string(C_name_, 50,575,"times",12)
        n_pdf.write_string(C_email_, 50,560,"times",12)
        n_pdf.write_string(C_addres, 50,545,"times",12)
        n_pdf.write_string("Ship To", 400,590,"timesb",12)
        n_pdf.write_string(C_name_, 400,575,"times",12)
        n_pdf.write_string("San Jose-Costa Rica", 400,560,"times",12)
       
        colum = 0
        row_ = 0
        x = 50
        y = 525
        for row in matrix:
            colum = 0
            x = 50
            
            for element in row:
                if row_ == 0:
                    n_pdf.write_string(element, x,y,"timesb",12)
                    colum += 1
                    x += 160
                else:
                    n_pdf.write_string(element, x,y,"times",12)
                    colum += 1
                    x += 160
            row_ +=1
            y -= 15

        n_pdf.write_string("    Subtotal " + sub_input.get_text(), 475,y-15,"times",12)
        n_pdf.write_string("        Taxes " + tax_input.get_text()+"%", 475,y-30,"times",12)
        n_pdf.write_string("         Total " + total_input.get_text(), 475,y-45,"times",12)
        n_pdf.save()
        matrix = [["Item", "Quantity","Price","Amount"],["","","",""],["","","",""],["","","",""]]
        main_menu_window()
    #Settings of the screen
    pygame.init()
    weight, height = 952,768
    screen = pygame.display.set_mode((weight,height))
    scroll = 10
    scroll_ = 30
    #List of the invoice numers
    archive_csv = csv_class("Invoices.csv","rt")
    matrix_csv = archive_csv.get_matrix()
    inv_number = 1
    if matrix_csv[0] != []:
        for row in matrix_csv:
            inv_number = int(row[0]) + 1
    inv_number = str(inv_number)
    
    #Text input
    d_y = 350
    due_input = text_box(645,d_y,140,25, "")
    n_y = 400
    note_input = text_box(150,n_y,600,30, "[Add a note or instruction for your customer]")
    

    #Time
    now = datetime.now()
    now.date()


    #Caption
    pygame.display.set_caption("Make Invoice")

    #Set initial clock
    clock = pygame.time.Clock()

    #Font
    font = pygame.font.Font("times.ttf", 20)
    font_n = pygame.font.Font("timesbd.ttf", 20)
    
    #Images of the screen
    background = pygame.image.load("Images/background.png")
    logo = pygame.image.load("logo.png")
    check = pygame.image.load("Images/check.png")
    check_1 = pygame.image.load("Images/check_1.png")

    arrow_up = pygame.image.load("Images/arrow_up.png")
    arrow_u = pygame.image.load("Images/arrow_u.png")

    arrow_down = pygame.image.load("Images/arrow_down.png")
    arrow_d = pygame.image.load("Images/arrow_d.png")

    more = pygame.image.load("Images/more.png")
    more_b = pygame.image.load("Images/more_b.png")

    less = pygame.image.load("Images/less.png")
    less_b = pygame.image.load("Images/less_b.png")

    equal = pygame.image.load("Images/equal.png")
    equal_b = pygame.image.load("Images/equal_b.png")
    
    #Create the buttons and cursor
    cursor = Cursor()
    bt_check = Button(check,check_1,470,700,60,60)
    bt_up = Button(arrow_up,arrow_u,900,0,40,40)
    bt_down = Button(arrow_down,arrow_d,900,720,40,40)
    
    
    
    #permanent text
    Inv_d = "Invoice For"
    Inv_d = font_n.render(Inv_d, True, (0, 0, 0))

    C_name_ = "[Customer Name]"
    C_name = font.render(C_name_, True, (0, 0, 0))

    C_email_ = "[Customer Email]"
    C_email = font.render(C_email_, True, (0, 0, 0))

    C_addres = "[Customer Addres]"
    
    Inv_n = "Invoice Number: " + inv_number
    Inv_n = font_n.render(Inv_n, True, (0, 0, 0))

    S_date = "Sent: " + str(now.date())
    S_date = font.render(S_date, True, (0, 0, 0))

    D_date = "Due: "
    D_date = font.render(D_date, True, (0, 0, 0))

    Sub = "Subtotal: "
    Sub = font.render(Sub, True, (0, 0, 0))

    Tax = "Tax: "
    Tax = font.render(Tax, True, (0, 0, 0))

    Total = "Total: "
    Total = font.render(Total, True, (0, 0, 0))
    
    #Position in y of the blits
    Inv_y = 300
    C_y = 325
    E_y = 350
    L_y = 50
    B_y = 425
    M_y = 600
    S_y = 575
    T_y = 600
    To_y = 625
    sub_input = text_box(660,S_y,90,25, "")
    tax_input = text_box(660,T_y,90,25, "")
    total_input = text_box(660,T_y,90,25, "")
    #Draw the matrix
    if not show_services:
        buttons_box.empty()
        draw_matrix(screen, B_y)
    #While of the loop
    exit_ = False
    while exit_ != True:
        #pygame.display.update()
        #Buttons dynamics
        bt_more = Button(more,more_b,150,M_y,60,60)
        bt_less = Button(less,less_b,205,M_y,60,60)
        bt_equal = Button(equal,equal_b,265,M_y+5,50,50)
        
        clock.tick(30)
        cursor.update()
        screen.blit(pygame.transform.scale(background,(weight,height)),(0,0))
        screen.blit(pygame.transform.scale(logo,(400,200)),(250,L_y))
        #Update the text box
        due_input.update(screen,cursor, True, d_y)
        note_input.update(screen,cursor, False,n_y)
                        
        if not show_services:
            box_group.update(screen, cursor, False, None)
            buttons_box.empty()
            buttons_services = []
            for button in buttons:
                button.update(screen, cursor)

            screen.blit(Sub,(585,S_y))
            screen.blit(Tax,(622,T_y))
            screen.blit(Total,(610,To_y))
            sub_input.update(screen,cursor,False,S_y)
            tax_input.update(screen,cursor,False,T_y)
            total_input.update(screen,cursor,False,To_y)
            bt_more.update(screen,cursor)
            bt_less.update(screen,cursor)
            bt_check.update(screen, cursor)
            bt_equal.update(screen, cursor)
            
        if show_services:
            box_group.empty()
            buttons = []
            buttons_box.update(screen, cursor, False, None)
            for button in buttons_services:
                button.update(screen, cursor)
        #Blit the text
        screen.blit(Inv_d,(150,Inv_y))
        screen.blit(C_name,(150,C_y))
        screen.blit(C_email,(150,E_y))

        screen.blit(Inv_n,(600,Inv_y))
        screen.blit(S_date,(600,C_y))
        screen.blit(D_date,(600,E_y))

        
        
        #Update Buttons
        
        bt_down.update(screen,cursor)
        bt_up.update(screen,cursor)
        

        #Read the changes in the matrix
        cont = 0
        sub_total = 0
        for think in matrix:
            if cont > 0:
                if think[1] != " " and think[1] != "":
                    think[3] = str(int(think[1])*int(think[2]))
                    
                if think[3] != " " and think[3] != "":
                    sub_total += int(think[3])
                    
                
            else:
                cont += 1
            
                
        #Update Display
        pygame.display.update()
        for event in pygame.event.get():
            #Update the text of the box
            due_input.text_update(event)
            note_input.text_update(event)
            sub_input.text_update(event)
            tax_input.text_update(event)
            if not show_services:
                box_group.update(screen, cursor, False, event)
                
            if show_services:
                buttons_box.update(screen, cursor, False, event)
                
            if event.type == pygame.QUIT:
                #Exit
                exit_ = True
                pygame.quit()
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not show_services:
                    for button in buttons:
                        if cursor.colliderect(button.rect):
                            print("Push Button")
                            rect_select = button.get_pos()
                            show_services = True
                            draw_matrix_services(screen, B_y)
                            
                if show_services:
                    for button in buttons_services:
                        if cursor.colliderect(button.rect):
                            rect = button.get_pos()
                            matrix[rect_select[0]][0] = matrix_services[rect[0]][0]
                            matrix[rect_select[0]][2] = matrix_services[rect[0]][1]
                            show_services = False
                            draw_matrix(screen, B_y)
                            rect_select = None
                if cursor.colliderect(bt_check.rect):
                    create_pdf()
                    exit_ = True
                    pygame.quit()
                    
                    break
                if cursor.colliderect(bt_down.rect):
                    d_y += scroll
                    n_y += scroll
                    Inv_y += scroll
                    C_y += scroll
                    E_y += scroll
                    L_y += scroll
                    B_y += scroll
                    M_y += scroll
                    S_y += scroll
                    T_y += scroll
                    To_y += scroll
                    if not show_services:
                        draw_matrix(screen, B_y)
                    if show_services:
                        draw_matrix_services(screen, B_y)
                if cursor.colliderect(bt_up.rect):
                    d_y -= scroll
                    n_y -= scroll
                    Inv_y -= scroll
                    C_y -= scroll
                    E_y -= scroll
                    L_y -= scroll
                    B_y -= scroll
                    M_y -= scroll
                    S_y -= scroll
                    T_y -= scroll
                    To_y -= scroll
                    if not show_services:
                        draw_matrix(screen, B_y)
                    if show_services:
                        draw_matrix_services(screen, B_y)
                if cursor.colliderect(bt_more.rect):
                    d_y -= scroll_
                    n_y -= scroll_
                    Inv_y -= scroll_
                    C_y -= scroll_
                    E_y -= scroll_
                    L_y -= scroll_
                    B_y -= scroll_
                    add_row_matrix(screen, B_y)
                if cursor.colliderect(bt_less.rect):
                    d_y += scroll_
                    n_y += scroll_
                    Inv_y += scroll_
                    C_y += scroll_
                    E_y += scroll_
                    L_y += scroll_
                    B_y += scroll_
                    eliminate_row_matrix(screen,B_y)
                if cursor.colliderect(bt_equal.rect):
                    sub_input.edit_text(str(sub_total))
                    a = tax_input.get_text()
                    draw_matrix(screen, B_y)
                    if a != "":
                        print(a)
                        print(sub_total)
                        to = sub_total+((int(a)/100)*sub_total)
                        total_input.edit_text(str(to))
    
    pygame.quit()
    
"""Functions"""
#Creation of groups and cursor
buttons_main = pygame.sprite.Group()
buttons_servicesGroup = pygame.sprite.Group()
buttons_box_s = pygame.sprite.Group()
box_group_s = pygame.sprite.Group()
buttons_invoiceGroup = pygame.sprite.Group()
buttons_box_i = pygame.sprite.Group()
box_group_i = pygame.sprite.Group()
cursor = Cursor()
FPS = 60
width, height = 900, 900

#Creation of buttons
scale_x, scale_y = 150, 75
img_bt_createPDF1 = pygame.image.load("Images/bt_createInvoice.png")
img_bt_createPDF2 = pygame.image.load("Images/bt_createInvoice2.png")
img_bt_managerPDF1 = pygame.image.load("Images/bt_manageInvoices.png")
img_bt_managerPDF2 = pygame.image.load("Images/bt_manageInvoices2.png")
img_bt_report1 = pygame.image.load("Images/bt_generateReport.png")
img_bt_report2 = pygame.image.load("Images/bt_generateReport2.png")
img_bt_services1 = pygame.image.load("Images/bt_services.png")
img_bt_services2 = pygame.image.load("Images/bt_services2.png")
img_bt_addUser1 = pygame.image.load("Images/bt_addUser.png")
img_bt_addUser2 = pygame.image.load("Images/bt_addUser2.png")
img_bt_manageUser1 = pygame.image.load("Images/bt_manageUsers.png")
img_bt_manageUser2 = pygame.image.load("Images/bt_manageUsers2.png")
img_bt_exit1 = pygame.image.load("Images/bt_exit.png")
img_bt_exit2 = pygame.image.load("Images/bt_exit2.png")
img_bt_return1 = pygame.image.load("Images/bt_return.png")
img_bt_return2 = pygame.image.load("Images/bt_return2.png")
more = pygame.image.load("Images/more.png")
more_b = pygame.image.load("Images/more_b.png")
less = pygame.image.load("Images/less.png")
less_b = pygame.image.load("Images/less_b.png")
img_trash1 = pygame.image.load("Images/bt_trash.png")
img_trash2 = pygame.image.load("Images/bt_trash2.png")
img_inspect1 = pygame.image.load("Images/bt_inspect.png")
img_inspect2 = pygame.image.load("Images/bt_inspect2.png")

bt_createInvoice = Button(img_bt_createPDF1, img_bt_createPDF2, (width/4) + 50, 400, scale_x, scale_y)
bt_manageInvoice = Button(img_bt_managerPDF1, img_bt_managerPDF2, (width/4) + 50 , 550, scale_x, scale_y)
bt_report = Button(img_bt_report1, img_bt_report2, (width/4) + 50, 700, scale_x, scale_y)
bt_services = Button(img_bt_services1, img_bt_services2, (width/2) + 25, 400, scale_x, scale_y)
bt_addUser = Button(img_bt_addUser1, img_bt_addUser2, (width/2) + 25, 550, scale_x, scale_y)
bt_manageUser = Button(img_bt_manageUser1, img_bt_manageUser2, (width/2) + 25, 700, scale_x, scale_y)
bt_exit = Button(img_bt_exit1, img_bt_exit2, width - 175, height - 100, scale_x, scale_y)
buttons_main.add(bt_createInvoice, bt_manageInvoice, bt_report, bt_services, bt_addUser, bt_manageUser, bt_exit)

bt_return_s = Button(img_bt_return1, img_bt_return2, width - 160 , 10, scale_x, scale_y)
bt_more_s = Button(more, more_b, 650, 210, 60, 60)
bt_less_s = Button(less, less_b, 650, 270, 60, 60)
buttons_servicesGroup.add(bt_return_s, bt_more_s, bt_less_s)

bt_return_i = Button(img_bt_return1, img_bt_return2, width - 160 , 10, scale_x, scale_y)
buttons_invoiceGroup.add(bt_return_i)


archive_csv = csv_class("Invoices.csv", "rt")
matrix_invoices = archive_csv.get_matrix()


def draw_matrix_services_s(y):
    global box_group_s, matrix_services

    #Matrix of the services
    x = 0
    row = 0
    box_group_s.empty()
    for line in matrix_services:
        row +=1
        colum = 0
        x = 0
        y += 30
        if True:
            for element in line:
                if colum == 0:
                    colum += 1
                    x += round(width/2 - 225)
                    box = text_group(x,y,330,30, element, row-1, colum-1)
                    box_group_s.add(box)
                else:
                    if colum == 1:
                        colum += 1
                        x += 330
                        box = text_group(x,y,90,30, element, row-1, colum-1)
                        box_group_s.add(box)
                    else:
                        colum += 1
                        x += 90
                        box = text_group(x,y,90,30, element, row-1, colum-1)
                        box_group_s.add(box)

def eliminate_row_matrix_services(y):
    global matrix_services
    m = []
    for i in range(len(matrix_services) - 1):
        m += [matrix_services[i]]
    matrix_services = m
    draw_matrix_services_s(y)


def add_row_matrix_services(y):
    global matrix_services
    matrix_services += [["", ""]]
    draw_matrix_services_s(y)


def services_window():
    global FPS, cursor, width, height, buttons_box_s, buttons_, matrix_services

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Services Window")
    clock = pygame.time.Clock()
    background = pygame.image.load("Images/background.png")
    background = pygame.transform.scale(background, (width, height))
    logo = pygame.image.load("Images/Logo.png")
    logo = pygame.transform.scale(logo, (300, 150))
    font = pygame.font.Font("times.ttf", 20)

    draw_matrix_services_s(210)
    service_box = text_box(225, 100, 330, 30, "Services")
    cost_box = text_box(555, 100, 90, 30, "Cost")
    services_txt = "Services Manager"
    services_txt = font.render(services_txt, True, (0,0,0))

    exit_ = False
    while exit_ != True:

        for event in pygame.event.get():
            for box in box_group_s:
                box.update_services(screen, cursor, False, event)
            
            if event.type == pygame.QUIT:
                # Exit
                exit_ = True
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(bt_more_s.rect):
                    add_row_matrix_services(210)
                if cursor.colliderect(bt_less_s.rect):
                    eliminate_row_matrix_services(210)
                if cursor.colliderect(bt_return_s.rect):
                    archive_csv.write(matrix_services)
                    archive_csv.update_matrix("Services.csv", "w")
                    main_menu_window()
                    exit_ = True
                    pygame.quit()

        clock.tick(60)
        screen.blit(background, (0, 0))
        screen.blit(logo, (round((width / 2)) - 150, 25))
        screen.blit(services_txt, (round(width/2 - 80), 190))
        cursor.update()
        service_box.update(screen, cursor, False, 210)
        cost_box.update(screen, cursor, False, 210)
        for box in box_group_s:
            box.update_services(screen, cursor, False, None)
        buttons_servicesGroup.update(screen, cursor)
        pygame.display.update()

    pygame.quit()

def draw_matrix_invoices(y):
    global box_group_i, matrix_invoices, buttons_invoice

    #Matrix of the services
    x = 0
    row = 0
    box_group_i.empty()
    for line in matrix_invoices:
        row +=1
        colum = 0
        x = 0
        y += 30
        if True:
            for element in line:
                if colum == 0:
                    colum += 1
                    x += 50
                    box = text_box_invoices(x,y,150,30, element, row-1, colum-1)
                    box_group_i.add(box)
                else:
                    if colum == 1:
                        colum += 1
                        x += 150
                        box = text_box_invoices(x,y,300,30, element, row-1, colum-1)
                        box_group_i.add(box)
                    elif colum == 2:
                        colum += 1
                        x += 300
                        box = text_box_invoices(x,y,150,30, element, row-1, colum-1)
                        box_group_i.add(box)
                    elif colum == 3:
                        colum += 1
                        x += 150
                        box = text_box_invoices(x, y, 150, 30, element, row - 1, colum - 1)
                        box_group_i.add(box)
                    elif colum == 4:
                        colum += 1
                        x += 150
                        bt_trash = Button_(img_trash1, img_trash2, x, y + 2, 25, 25, row - 1, colum - 1)
                        buttons_invoiceGroup.add(bt_trash)
                    else:
                        colum += 1
                        x += 30
                        bt_inspect = Button_(img_inspect1, img_inspect2, x, y + 2, 25, 25, row - 1, colum - 1)
                        buttons_invoiceGroup.add(bt_inspect)
def manage_invoices_window():
    global FPS, cursor, width, height, buttons_box_i, buttons_, matrix_invoices

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Services Window")
    clock = pygame.time.Clock()
    background = pygame.image.load("Images/background.png")
    background = pygame.transform.scale(background, (width, height))
    logo = pygame.image.load("Images/Logo.png")
    logo = pygame.transform.scale(logo, (300, 150))
    font = pygame.font.Font("times.ttf", 20)

    draw_matrix_invoices(210)
    number_box = text_box(50, 210, 150, 30, "Invoice Number")
    detail_box = text_box(200, 210, 300, 30, "Invoice Detail")
    date_box = text_box(500, 210, 150, 30, "Invoice Date")
    price_box = text_box(650, 210, 150, 30, "Invoice Total")

    services_txt = "Invoices Manager"
    services_txt = font.render(services_txt, True, (0, 0, 0))

    exit_ = False
    while exit_ != True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit
                exit_ = True
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(bt_return_i.rect):
                    archive_csv.write(matrix_invoices)
                    archive_csv.update_matrix("Invoices.csv", "w")
                    main_menu_window()
                    exit_ = True
                    pygame.quit()

        clock.tick(60)
        screen.blit(background, (0, 0))
        screen.blit(logo, (round((width / 2)) - 150, 25))
        screen.blit(services_txt, (round(width / 2 - 80), 185))
        cursor.update()
        number_box.update(screen, cursor, False, 210)
        detail_box.update(screen, cursor, False, 210)
        date_box.update(screen, cursor, False, 210)
        price_box.update(screen, cursor, False, 210)
        box_group_i.update(screen, cursor, False, 240)
        buttons_invoiceGroup.update(screen, cursor)
        pygame.display.update()

    pygame.quit()
def main_menu_window():
    global FPS, cursor, buttons_main, width, height,matrix
    print(matrix)
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()

    #Load images
    background = pygame.image.load("Images/background.png")
    background = pygame.transform.scale(background, (width, height))
    logo = pygame.image.load("Images/Logo.png")
    logo = pygame.transform.scale(logo, (400, 200))
    font = pygame.font.Font("times.ttf", 30)
    user = "Marcos"

    #Creates texts
    welcome_txt = f"Welcome, {user}"
    welcome_txt = font.render(welcome_txt, True, (0,0,0))
    function_txt = f"{user}, what would you want to do?"
    function_txt = font.render(function_txt, True, (0,0,0))
    now = datetime.now()
    now.date()
    date = str(now.date())
    date = font.render(date, True, (0, 0, 0))


    exit_ = False
    while exit_ != True:
        clock.tick(60)
        cursor.update()
        screen.blit(background, (0, 0))
        screen.blit(welcome_txt, (10, 5))
        screen.blit(function_txt, ((round(width/2)) - 210, 350))
        screen.blit(date, (750, 5))
        screen.blit(logo, (round((width/2)) - 200, 50))
        buttons_main.update(screen, cursor)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit
                exit_ = True
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(bt_exit.rect):
                    exit_ = True
                    pygame.quit()
                    break
                elif cursor.colliderect(bt_createInvoice.rect):
                    make_invoice_window()
                    exit_ = True
                    pygame.quit()
                    break
                    
                elif cursor.colliderect(bt_manageInvoice.rect):
                    manage_invoices_window()
                    exit_ = True
                    pygame.quit()
                    break
                elif cursor.colliderect(bt_report.rect):
                    pass
                elif cursor.colliderect(bt_services.rect):
                    services_window()
                    exit_ = True
                    pygame.quit()
                    break
                elif cursor.colliderect(bt_addUser.rect):
                    pass
                elif cursor.colliderect(bt_manageUser.rect):
                    pass

        

    pygame.quit()

login_window()
