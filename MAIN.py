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
import webbrowser as wb
from datetime import timedelta

pdfmetrics.registerFont(TTFont('times','times.ttf'))
pdfmetrics.registerFont(TTFont('timesb','timesbd.ttf'))
box_group = pygame.sprite.Group()
box_groupr = pygame.sprite.Group()
buttons = []
buttonsr = []


pdfmetrics.registerFont(TTFont('times','times.ttf'))
pdfmetrics.registerFont(TTFont('timesb','timesbd.ttf'))
box_group = pygame.sprite.Group()
box_groupr = pygame.sprite.Group()
buttons = []
buttonsr = []


buttons_box = pygame.sprite.Group()
buttons_boxr = pygame.sprite.Group()
buttons_services = []
buttons_report = []
buttons_dates = []
show_services = False
show_dates = False
rect_select = None
rect_select2 = None
show_search = False
show_camera = True
show_done = False

name = "Unknown"

#Creation of groups and cursor
buttons_main = pygame.sprite.Group()
buttons_servicesGroup = pygame.sprite.Group()
buttons_servicesTrash = pygame.sprite.Group()
buttons_servicesInspect = pygame.sprite.Group()
buttons_reportGroup = pygame.sprite.Group()

buttons_box_s = pygame.sprite.Group()
box_group_s = pygame.sprite.Group()
buttons_invoiceGroup = pygame.sprite.Group()
buttons_box_i = pygame.sprite.Group()
box_group_i = pygame.sprite.Group()
cursor = Cursor()
FPS = 60
width, height = 900, 800

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
img_check1 = pygame.image.load("Images/check.png")
img_check2 = pygame.image.load("Images/check_1.png")


bt_createInvoice = Button(img_bt_createPDF1, img_bt_createPDF2, (width/4) + 50, 400, scale_x, scale_y)
bt_manageInvoice = Button(img_bt_managerPDF1, img_bt_managerPDF2, (width/4) + 50 , 550, scale_x, scale_y)
bt_report = Button(img_bt_report1, img_bt_report2, (width/3) + 75, 700, scale_x, scale_y)
bt_services = Button(img_bt_services1, img_bt_services2, (width/2) + 25, 400, scale_x, scale_y)
bt_addUser = Button(img_bt_addUser1, img_bt_addUser2, (width/2) + 25, 550, scale_x, scale_y)
#bt_manageUser = Button(img_bt_manageUser1, img_bt_manageUser2, (width/2) + 25, 700, scale_x, scale_y)
bt_exit = Button(img_bt_exit1, img_bt_exit2, width - 175, height - 100, scale_x, scale_y)
buttons_main.add(bt_createInvoice, bt_manageInvoice, bt_report, bt_services, bt_addUser, bt_exit)

bt_return_s = Button(img_bt_return1, img_bt_return2, width - 160 , 10, scale_x, scale_y)
bt_more_s = Button(more, more_b, 650, 210, 60, 60)
bt_less_s = Button(less, less_b, 650, 270, 60, 60)
buttons_servicesGroup.add(bt_return_s, bt_more_s, bt_less_s)

bt_return_i = Button(img_bt_return1, img_bt_return2, width - 160 , 10, scale_x, scale_y)
buttons_invoiceGroup.add(bt_return_i)

bt_return_r = Button(img_bt_return1, img_bt_return2, width - 110 , 10, scale_x, scale_y)
bt_check_r = Button(img_check1, img_check2, 415, 700, 60, 60)
buttons_reportGroup.add(bt_return_r, bt_check_r)

archive_csv = csv_class("Invoices.csv", "rt")
matrix_invoices = archive_csv.get_matrix()

archive_csv = csv_class("Reports.csv", "rt")
matrix_reports = archive_csv.get_matrix()

rep_number = str(0)

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
        print(best_match_index)
        print(known_face_names)
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
def register_window():
    global matrix_customer
    
    camera = cv2.VideoCapture(0)
    pygame.init()
    pygame.display.set_caption("Register User")
    weight, height = 952,768
    screen = pygame.display.set_mode((weight,height))
    
    #Font
    font = pygame.font.Font("times.ttf", 60)
    font_n = pygame.font.Font("timesbd.ttf", 20)

    #text
    User = "User"
    User = font_n.render(User, True, (0,0,0))
    Name = "Full Name"
    Name = font_n.render(Name, True, (0,0,0))
    Id = "Id Number"
    Id = font_n.render(Id, True, (0,0,0))
    Age = "Age"
    Age = font_n.render(Age, True, (0,0,0))
    Email = "Email"
    Email = font_n.render(Email, True, (0,0,0))
    Address = "Residence Address"
    Address = font_n.render(Address, True, (0,0,0))
    
    #text box
    User_box = text_box(50, 75, 300,30, "")
    Name_box = text_box(50, 150, 300,30, "")
    Id_box = text_box(50, 225, 300,30, "")
    Age_box = text_box(50, 300, 300,30, "")
    Email_box = text_box(50, 375, 300,30, "")
    Address_box = text_box(50, 450, 300,30,"")

    
    background = pygame.image.load("Images/background.png")
    check = pygame.image.load("Images/check.png")
    check_1 = pygame.image.load("Images/check_1.png")
    camera_ = pygame.image.load("Images/camera.png")
    camera_1 = pygame.image.load("Images/camera_b.png")
    logo = pygame.image.load("Images/Logo.png")
    camera_1 = pygame.image.load("Images/camera_b.png")
    return_ = pygame.image.load("Images/bt_return.png")
    return_1 = pygame.image.load("Images/bt_return2.png")
    
    
    cursor =  Cursor()
    button = Button(check,check_1, 100, 550,80,80)
    button_c = Button(camera_,camera_1, 400, 500,80,80)
    button_r = Button(return_,return_1, 65,650,150,80)
    get_data  = True
    exit_ = False
    while exit_ != True:
        screen.blit(pygame.transform.scale(background,(weight,height)),(0,0))
        
        ret, frame_ = camera.read()
        cursor.update()
        button_r.update(screen,cursor)
        if not get_data:
            frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (150,0))
            screen.blit(pygame.transform.scale(logo,(300,150)),(600,600))
            button_c.update(screen,cursor)
            pygame.display.update()
            
        if get_data:
            screen.blit(User,(50,50))
            screen.blit(Name,(50,125))
            screen.blit(Age,(50,200))
            screen.blit(Id,(50,275))
            screen.blit(Email,(50,350))
            screen.blit(Address,(50,425))
            screen.blit(pygame.transform.scale(logo,(500,200)),(400,150))
            button.update(screen,cursor)
            User_box.update(screen, cursor, True, 75)
            Name_box.update(screen, cursor, True, 150)
            Age_box.update(screen, cursor, True, 225)
            Id_box.update(screen, cursor, True, 300)
            Email_box.update(screen, cursor, True, 375)
            Address_box.update(screen, cursor, True, 450)
            pygame.display.update()

            
        for event in pygame.event.get():
            if get_data:
                User_box.text_update(event)
                Name_box.text_update(event)
                Id_box.text_update(event)
                Age_box.text_update(event)
                Email_box.text_update(event)
                Address_box.text_update(event)
                pygame.display.update()
            
            if event.type == pygame.QUIT:
                # Exit
                exit_ = True
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(button.rect):
                    if not get_data:
                        pass
                    if get_data:
                        get_data = False
                if cursor.colliderect(button_c.rect):
                    for i in range(1):
                        cv2.imwrite("faces/"+User_box.get_text()+".png", frame_)
                    m_list = []
                    m_list += [User_box.get_text()]
                    m_list += [Name_box.get_text()]
                    m_list += [Age_box.get_text()]
                    m_list += [Id_box.get_text()]
                    m_list += [Email_box.get_text()]
                    m_list += [Address_box.get_text()]
                    matrix_customer += [m_list]
                    print(matrix_customer)
                    archive_c_.write(matrix_customer)
                    archive_c_.update_matrix("customer_data.csv","w")
                    main_menu_window()
                    exit_ = True
                    pygame.quit()
                    break
                if cursor.colliderect(button_r.rect):
                    if get_data:
                        camera.release()
                        main_menu_window()
                        exit_ = True
                        pygame.quit()
                        break
                    if not get_data:
                        get_data = True
                        
def login_window():
    global show_search, show_done, show_camera, name
    camera_login = cv2.VideoCapture(0)
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
        ret, frame_ = camera_login.read()
        cursor.update()
        if show_camera:
            frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (150,0))
            button.update(screen,cursor)
            pygame.display.update()
        if not show_camera:
            camera_login.release()
            Welcome = "Welcome " + name
            Welcome = font.render(Welcome, True, (0, 0, 0))
            screen.blit(Welcome, (250,200))
            pygame.display.update()
            sleep(2)
            exit_ = True
            pygame.quit()
            main_menu_window()
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
                        print("Here")
                        for i in range(1):
                            cv2.imwrite("faces_unknown/unknown"+str(i)+".png", frame_)
                        for dirpath, dnames, fnames in os.walk("./faces_unknown"):
                            for f in fnames:
                                if f.endswith(".jpg") or f.endswith(".png"):
                                    classify_face(f)
                    if not show_camera:
                        pass

def make_invoice_window():
    global name, box_group,matrix_customer, matrix_data, window_c,buttons, show_services,matrix_services, buttons_services, buttons_box,matrix, rect_select,matrix_invoices
    def create_pdf():
        global matrix
        n_pdf = pdf("invoices\Invoice " + str(inv_number), "logo.png")
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
        n_pdf.write_string("    Discount " + discount_input.get_text()+"%", 475,y-45,"times",12)
        n_pdf.write_string("         Total " + total_input.get_text(), 475,y-60,"times",12)
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
    inv_number = 1
    if matrix_invoices != [[]] and matrix_invoices != []:
        for row in matrix_invoices:
            inv_number = int(row[0]) + 1
    inv_number = str(inv_number)
    #Time
    m_days = datetime.now() + timedelta(days=3)
    now = datetime.now()
    now.date()
    
    #Text input
    d_y = 350
    due_input = text_box(645,d_y,140,25, str(m_days.date()))
    n_y = 400
    note_input = text_box(150,n_y,600,30, "[Add note]")

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
    bt_return = Button(img_bt_return1,img_bt_return2,5,5,100,50)
    #Load the customers info
    if name != "Unknown":
        for customer in matrix_customer:
            if customer[0] == name:
                C_name_ = customer[1]
                C_email_ = customer[4]
                C_addres = customer[5]
    if name == "Unknown":
        C_name_ = "Unknown"
        C_email_ = "Unknown"
        C_addres = "Unknown"
    
    #permanent text
    Inv_d = "Invoice For"
    Inv_d = font_n.render(Inv_d, True, (0, 0, 0))
    
    C_name = font.render(C_name_, True, (0, 0, 0))

    C_email = font.render(C_email_, True, (0, 0, 0))

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

    discount = "Discount: "
    discount = font.render(discount, True, (0, 0, 0))
    
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
    total_input = text_box(660,T_y+25,90,25, "")
    discount_input = text_box(660,T_y,90,25, "")
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
            screen.blit(discount,(580,To_y))
            screen.blit(Total,(610,To_y+25))
            sub_input.update(screen,cursor,False,S_y)
            tax_input.update(screen,cursor,False,T_y)
            discount_input.update(screen,cursor,False,To_y)
            total_input.update(screen,cursor,False,To_y+25)
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
        bt_return.update(screen,cursor)

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
            discount_input.text_update(event)
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
                    a = []
                    a += [inv_number]
                    a += [note_input.get_text()]
                    a += [str(now.date())]
                    a += [round(float(total_input.get_text()))]
                    a += [round(float(sub_input.get_text()) * float(int(tax_input.get_text())/100))]
                    a += [0]
                    a += [0]
                    matrix_invoices += [a]
                    archive_csv.write(matrix_invoices)
                    archive_csv.update_matrix("Invoices.csv", "w")
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
                    b = discount_input.get_text()
                    draw_matrix(screen, B_y)
                    if a != "":
                        to = sub_total+(((int(a)/100)*sub_total)-(sub_total*(int(b)/100)))
                        total_input.edit_text(str(to))
                if cursor.colliderect(bt_return.rect):
                    archive_csv.write(matrix_invoices)
                    archive_csv.update_matrix("Invoices.csv", "w")
                    main_menu_window()
                    exit_ = True
                    pygame.quit()
    
    pygame.quit()
    
"""Functions"""
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
    print(matrix_services)

def add_row_matrix_services(y):
    global matrix_services
    matrix_services += [["", ""]]
    draw_matrix_services_s(y)
    print(matrix_services)

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

        clock.tick(10)
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

filter_invoices = ""
def draw_matrix_invoices(y):
    global box_group_i, matrix_invoices, buttons_invoice, filter_invoices
    archive_csv_ = csv_class("Invoices.csv", "rt")
    matrix_invoices = archive_csv_.get_matrix()
    #Matrix of the services
    x = 0
    row = 0
    print(y)
    box_group_i.empty()
    buttons_servicesTrash.empty()
    buttons_servicesInspect.empty()
    for line in matrix_invoices:
        row +=1
        colum = 0
        x = 0
        y += 30
        if line[2] == filter_invoices or filter_invoices == "":
            for element in line:
                if colum == 0:
                    colum += 1
                    x += 15
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
                        box = text_box_invoices(x,y,125,30, element, row-1, colum-1)
                        box_group_i.add(box)
                    elif colum == 3:
                        colum += 1
                        x += 125
                        box = text_box_invoices(x, y, 125, 30, element, row - 1, colum - 1)
                        box_group_i.add(box)
                    elif colum == 4:
                        colum += 1
                        x += 125
                        box = text_box_invoices(x, y, 125, 30, element, row - 1, colum - 1)
                        box_group_i.add(box)
                    elif colum == 5:
                        colum += 1
                        x += 125
                        bt_trash = Button_(img_trash1, img_trash2, x, y + 2, 25, 25, row - 1, colum - 1)
                        buttons_servicesTrash.add(bt_trash)
                    else:
                        colum += 1
                        x += 30
                        bt_inspect = Button_(img_inspect1, img_inspect2, x, y + 2, 25, 25, row - 1, colum - 1)
                        buttons_servicesInspect.add(bt_inspect)

def manage_invoices_window():
    global FPS,update, cursor, width, height, buttons_box_i, buttons_, matrix_invoices, buttons_servicesTrash, buttons_servicesInspect,filter_invoices
    archive_csv_ = csv_class("Invoices.csv", "rt")
    matrix_invoices = archive_csv_.get_matrix()
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Services Window")
    clock = pygame.time.Clock()
    background = pygame.image.load("Images/background.png")
    background = pygame.transform.scale(background, (width, height))
    logo = pygame.image.load("Images/Logo.png")
    logo = pygame.transform.scale(logo, (300, 150))
    font = pygame.font.Font("times.ttf", 20)
    p_y = 325
    draw_matrix_invoices(p_y)
    number_box = text_box(15, 250, 150, 30, "Invoice Number")
    detail_box = text_box(165, 250, 300, 30, "Invoice Detail")
    date_box = text_box(465, 250, 125, 30, "Invoice Date")
    price_box = text_box(590, 250, 125, 30, "Invoice Total")
    tax_box = text_box(715, 250, 125, 30, "Invoice Taxes")
    search_box = text_box(125, 275, 155, 30, "")

    services_txt = "Invoices Manager"
    services_txt = font.render(services_txt, True, (0, 0, 0))

    search = "Search Date: "
    search = font.render(search, True, (0, 0, 0))

    bt_search = Button(img_inspect1, img_inspect2, 285, 275, 25, 25)
    
    exit_ = False
    while exit_ != True:

        for event in pygame.event.get():
            search_box.text_update(event)
            if event.type == pygame.QUIT:
                # Exit
                exit_ = True
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                for trash in buttons_servicesTrash:
                    trash.update_trash(screen, cursor, event)
                
                for inspect in  buttons_servicesInspect:
                    inspect.update_inspect(screen, cursor, event)
                if cursor.colliderect(bt_return_i.rect):
                    archive_csv.write(matrix_invoices)
                    archive_csv.update_matrix("Invoices.csv", "w")
                    main_menu_window()
                    exit_ = True
                    pygame.quit()
                if cursor.colliderect(bt_search.rect):
                    filter_invoices = search_box.get_text()
                    draw_matrix_invoices(p_y)       
        clock.tick(30)
        screen.blit(background, (0, 0))
        screen.blit(logo, (round((width / 2)) - 150, 25))
        screen.blit(services_txt, (round(width / 2 - 80), 185))
        screen.blit(search,(15, 275))
        cursor.update()
        bt_search.update(screen, cursor)
        search_box.update(screen, cursor, False, 275)
        number_box.update(screen, cursor, False, p_y)
        detail_box.update(screen, cursor, False, p_y)
        date_box.update(screen, cursor, False, p_y)
        price_box.update(screen, cursor, False, p_y)
        tax_box.update(screen, cursor, False, p_y)
        box_group_i.update(screen, cursor, False, p_y)
        buttons_invoiceGroup.update(screen, cursor)
        for trash in buttons_servicesTrash:
            trash.update_trash(screen, cursor, None)
        for inspect in  buttons_servicesInspect:
            inspect.update_inspect(screen, cursor, None)
        pygame.display.update()

    pygame.quit()
def main_menu_window():
    global FPS, cursor, buttons_main, width, height,matrix, name
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
    user = name

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
                    make_report_window()
                    exit_ = True
                    pygame.quit()
                elif cursor.colliderect(bt_services.rect):
                    services_window()
                    exit_ = True
                    pygame.quit()
                    break
                elif cursor.colliderect(bt_addUser.rect):
                    register_window()
                    exit_ = True
                    pygame.quit()
                    break

        

    pygame.quit()
def report_pdf_creator(matrix_report):
    global rep_number

    matrix_pdf = matrix_report
    ##La parte superior en y es 800
    ##El limite izquierdo en y es 50
    ##El limite derecho en y es 500
    n_pdf = pdf("Reports/Report " + str(rep_number), "logo.png")
    n_pdf.write_string("3C Landscaping services", 50, 650, "timesb", 12)

    txt_data = ""
    for row in matrix_data:
        for element in row:
            txt_data += str(element)
            txt_data += "\n"
    n_pdf.write_text(txt_data, 50, 635, "times", 12)
    txt_data = ""
    n_pdf.write_string("3C Landscaping services", 50, 650, "timesb", 12)
    n_pdf.write_string(("Report #" + rep_number), 400, 650, "times", 12)
    n_pdf.write_string(("Invoice #"), 50, 555, "times", 12)
    n_pdf.write_string(("Invoice Detail"), 125, 555, "times", 12)
    n_pdf.write_string(("Invoice Date"), 370, 555, "times", 12)
    n_pdf.write_string(("Amount"), 450, 555, "times", 12)
    n_pdf.write_string(("Taxes"), 525, 555, "times", 12)

    colum = 0
    row_ = 0
    y = 525
    amounts = 0
    taxes = 0
    for row in matrix_pdf:
        colum = 0
        x = 50
        for element in row:
            if row.index(element) == 0:
                n_pdf.write_string(element, x, y, "times", 12)
                colum += 1
                x += 75
            elif row.index(element) == 1:
                n_pdf.write_string(element, x, y, "times", 12)
                colum += 1
                x += 245
            elif row.index(element) == 2:
                n_pdf.write_string(element, x, y, "times", 12)
                colum += 1
                x += 80
            else:
                n_pdf.write_string(element, x, y, "times", 12)
                colum += 1
                x += 75
            if row.index(element) == 3:
                amounts += float(element)
            elif row.index(element) == 4:
                taxes += float(element)
        row_ += 1
        y -= 15

    n_pdf.write_string((f"Total        {round(amounts)}          {round(taxes)}"), 400, y - 15, "times", 12)

    n_pdf.save()

def draw_matrix_date(y):
    global box_groupr, matrix_dates2, buttonsr

    trans = pygame.image.load("Images/transparent.png")
    # Matrix of the items
    x = 0
    row = 0
    box_groupr.empty()
    buttonsr = []
    for line in matrix_dates2:
        row += 1
        colum = 0
        x = 0
        y += 30
        if True:
            for element in line:
                if colum == 0:
                    colum += 1
                    x += round(width/2) - 75
                    box = text_group(x, y, 150, 30, element, row - 1, colum - 1)
                    box_groupr.add(box)
                    if row - 1 == 0:
                        bt_transparent = Button_(trans, trans, x, y, 150, 30, row - 1, colum - 1)
                        buttonsr += [bt_transparent]

def draw_matrix_dates(y):
    global buttons_report, buttons_boxr, show_dates, matrix_dates

    check = pygame.image.load("Images/check_s.png")
    check_s = pygame.image.load("Images/check_s_.png")
    # Matrix of the items
    row = 0
    y = y + 30
    colum = 0
    x = round(width / 2) - 75
    buttons_report = []
    matrix_dates = [['Last day'], ['Last week'], ['Last month'], ['Last year']]
    buttons_boxr.empty()

    for line in matrix_dates:
        txt = ""
        for element in line:
            txt += element
        bt_transparent = Button_(check, check_s, x + 155, y, 30, 30, row, colum)
        buttons_report += [bt_transparent]
        box = text_group(x, y, 150, 30, txt, row, colum)
        buttons_boxr.add(box)
        txt = " "
        y += 30
        row += 1
        colum += 1

def make_report_window():
    global box_groupr, matrix_data, buttonsr, show_dates, matrix_dates, buttons_report, buttons_boxr, matrix_dates, matrix_dates2, rect_select2, rep_number, matrix_reports, matrix_invoices

    # Settings of the screen
    pygame.init()
    weight, height = 952, 768
    screen = pygame.display.set_mode((weight, height))

    # Caption
    pygame.display.set_caption("Make report")

    # Set initial clock
    clock = pygame.time.Clock()

    # Font
    font = pygame.font.Font("times.ttf", 20)

    # Images of the screen
    background = pygame.image.load("Images/background.png")
    logo = pygame.image.load("logo.png")


    cursor = Cursor()

    # Position in y of the blits


    # Draw the matrix
    if not show_dates:
        buttons_boxr.empty()
        draw_matrix_date(425)

    rep_number = 1
    if matrix_reports != []:
        for row in matrix_reports:
            rep_number = int(row[0]) + 1
    rep_number = str(rep_number)

    a = []

    report_txt = "Create a report for the company's sales"
    report_txt = font.render(report_txt, True, (0, 0, 0))
    date_txt = "Choose a date range to create the report"
    date_txt = font.render(date_txt, True, (0, 0, 0))

    now = datetime.now()
    now.date()

    # While of the loop
    exit_ = False
    while exit_ != True:

        clock.tick(30)
        cursor.update()
        screen.blit(pygame.transform.scale(background, (weight, height)), (0, 0))
        screen.blit(pygame.transform.scale(logo, (400, 200)), (250, 50))
        buttons_reportGroup.update(screen, cursor)
        screen.blit(report_txt, (round(width / 2) - 150, 300))
        screen.blit(date_txt, (round(width / 2) - 155, 400))

        if not show_dates:
            box_groupr.update(screen, cursor, False, None)
            buttons_boxr.empty()
            buttons_report = []
            for button in buttonsr:
                button.update(screen, cursor)

        if show_dates:
            box_groupr.empty()
            buttonsr = []
            buttons_boxr.update(screen, cursor, False, None)
            for button in buttons_report:
                button.update(screen, cursor)

        # Update Display
        pygame.display.update()
        for event in pygame.event.get():
            if not show_dates:
                box_groupr.update(screen, cursor, False, event)
            if show_dates:
                buttons_boxr.update(screen, cursor, False, event)

            if event.type == pygame.QUIT:
                # Exit
                exit_ = True
                pygame.quit()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not show_dates:
                    for button in buttonsr:
                        if cursor.colliderect(button.rect):
                            rect_select2 = button.get_pos()
                            show_dates = True
                            draw_matrix_dates(425)

                if show_dates:
                    for button in buttons_report:
                        if cursor.colliderect(button.rect):
                            rect = button.get_pos()
                            matrix_dates2[rect_select2[0]][0] = matrix_dates[rect[0]][0]
                            show_dates = False
                            draw_matrix_date(425)
                            rect_select2 = None
                if cursor.colliderect(bt_return_r.rect):
                    main_menu_window()
                    exit_ = True
                    pygame.quit()
                if cursor.colliderect(bt_check_r.rect):
                    a += [rep_number]
                    matrix_reports += [a]
                    archive_csv.write(matrix_reports)
                    archive_csv.update_matrix("Reports.csv", "w")
                    matrix_report = []
                    day = now.day
                    month = now.month
                    year = now.year
                    if matrix_dates2[0][0] == "Last day":
                        for row in matrix_invoices:
                            if str(row[2]) == f"{year}-{month:02d}-{day:02d}":
                                matrix_report += [row]

                    elif matrix_dates2[0][0] == "Last week":
                        for row in matrix_invoices:
                            if str(f"{year}-{month:02d}") == str(row[2])[:7] and int((row[2])[8:10]) > 7:
                                if day - 7 <= int((row[2])[8:10]) <= day:
                                    matrix_report += [row]
                                    report_pdf_creator(matrix_report)
                            elif str(f"{year}-{month:02d}") == str(row[2])[:7] and int((row[2])[8:10]) <= 7:
                                resta = day - 7
                                month2 = month - 1
                                day2 = 31
                                day2 += resta
                                if month2 <= int((row[2])[5:7]) and day2 <= 31:
                                    matrix_report += [row]
                                elif month >= int((row[2])[5:7]) and day >= int((row[2])[8:10]):
                                    matrix_report += [row]

                    elif matrix_dates2[0][0] == "Last month":
                        for row in matrix_invoices:
                            if year == int((row[2])[:4]):
                                month2 = month - 1
                                if 0 <= int((row[2])[8:10]) <= day and month == int((row[2])[5:7]):
                                    matrix_report += [row]
                                if day <= int((row[2])[8:10]) <= 31 and month2 == int((row[2])[5:7]):
                                    matrix_report += [row]
                    elif matrix_dates2[0][0] == "Last year":
                        for row in matrix_invoices:
                            year2 = year - 1
                            if year == int((row[2])[:4]):
                                if 0 <= int((row[2])[8:10]) <= day and 0 <= int((row[2])[5:7]) <= month:
                                    matrix_report += [row]
                            elif year2 == int((row[2])[:4]):
                               if day <= int((row[2])[8:10]) <= 31 and month <= int((row[2])[5:7]) <= 12:
                                    matrix_report += [row]
                    else:
                        matrix_report = matrix_invoices
                    report_pdf_creator(matrix_report)
                    bt_check_r.update_inspect(screen, cursor, event, rep_number)
                    main_menu_window()
                    exit_ = True
                    pygame.quit()


    pygame.quit()

login_window()
