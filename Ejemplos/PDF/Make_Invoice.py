from reportlab import *
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
import pygame
from CLASSES import *
from datetime import datetime
import numpy as np
##La parte superior en y es 800
##El limite izquierdo en y es 50
##El limite derecho en y es 500
box_group = pygame.sprite.Group()
opt_group = pygame.sprite.Group()
"""def show_services():
    global matrix_csv, window_c, row_group
    pygame.init()
    archive_csv = csv_class("services.csv","rt")
    
    window_c = False
    matrix_csv = archive_csv.get_matrix()
    weight, height = 400,0
    text = ""
    b_group = pygame.sprite.Group()
    y = 0
    row_ = 0
    b_group.empty()
    for line in matrix_csv:
        height += 25
        cont = 0
        for element in line:
            if cont == 0:
                text += element
                text += " "
            else:
                text += "₡"
                text += element
            cont += 1
        a = buttom_text(0,y,400,25, text,row_)
        text = ""
        row_ += 1
        b_group.add(a)
        y += 25
        
    print(text)
    screen_show = pygame.display.set_mode((weight,height))
    screen_show.fill((255,255,255))
    #Set initial clock
    clock = pygame.time.Clock()
    
    #Caption
    pygame.display.set_caption("Services")
    
    #Time
    now = datetime.now()
    now.date()
    #Create the buttons and cursor
    cursor = Cursor()
    
    #While of the loop
    exit_ = False
    while exit_ != True:
        if window_c:
            make_invoice_window
            #Exit
            exit_ = True
            pygame.quit()
            #window_c = False
            break
            
        screen_show.fill((255,255,255))
        clock.tick(60)
        cursor.update()
        b_group.update(screen_show,cursor,None)
        pygame.display.update()
        for event in pygame.event.get():
            b_group.update(screen_show,cursor,event)
            if event.type == pygame.QUIT:
                #Exit
                exit_ = True
                pygame.quit()
                break
    pygame.quit()"""
    

def draw_matrix(screen,y):
    global box_group, matrix
    #Matrix of the items
    x = 0
    row = 0
    box_group.empty()
    for line in matrix:
        row +=1
        colum = 0
        x = 0
        y += 30
        for element in line:
            if colum == 0:
                colum += 1
                x += 150
                box = text_group(x,y,330,30, element, row-1, colum-1)
                box_group.add(box)
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

def draw_matrix_opt(screen,y):
    global opt_group, matrix_csv
    #Matrix of the items
    x = 0
    row = 0
    opt_group.empty()
    for line in matrix_csv:
        row +=1
        colum = 0
        x = 0
        y += 30
        for element in line:
            if colum == 0:
                colum += 1
                x += 150
                box = text_group(x,y,330,30, element, row-1, colum-1)
                opt_group.add(box)
            else:
                if colum == 1:
                    colum += 1
                    x += 330
                    box = text_group(x,y,90,30, element, row-1, colum-1)
                    opt_group.add(box)
                else:
                    colum += 1
                    x += 90
                    box = text_group(x,y,90,30, element, row-1, colum-1)
                    opt_group.add(box)

def eliminate_row_matrix(screen, B_y):
    global matrix
    m = []
    for i in range(len(matrix)-1):
        m += [matrix[i]]
    matrix = m
    draw_matrix(screen,B_y)
        
def add_row_matrix(screen, B_y):
    global matrix
    matrix += [[" "," "," "," "]]
    draw_matrix(screen,B_y)

def create_pdf():
    pass


def make_invoice_window():
    global box_group, window_c
    #Settings of the screen
    pygame.init()
    weight, height = 952,768
    screen = pygame.display.set_mode((weight,height))
    scroll = 10
    scroll_ = 30
    #List of the invoice numers
    archive_csv = csv_class("invoice num.csv","rt")
    matrix_csv = archive_csv.get_matrix()
    inv_number = 1
    if matrix_csv[0] != []:
        for row in matrix_csv:
            for num in row:
                inv_number = int(num) + 1
    matrix_csv[0] += [inv_number]
    
    
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
    background = pygame.image.load("images/background.png")
    logo = pygame.image.load("Logo.png")
    check = pygame.image.load("images/check.png")
    check_1 = pygame.image.load("images/check_1.png")

    arrow_up = pygame.image.load("images/arrow_up.png")
    arrow_u = pygame.image.load("images/arrow_u.png")

    arrow_down = pygame.image.load("images/arrow_down.png")
    arrow_d = pygame.image.load("images/arrow_d.png")

    more = pygame.image.load("images/more.png")
    more_b = pygame.image.load("images/more_b.png")

    less = pygame.image.load("images/less.png")
    less_b = pygame.image.load("images/less_b.png")
    
    #Create the buttons and cursor
    cursor = Cursor()
    bt_check = Button(check,check_1,470,700,60,60)
    bt_up = Button(arrow_up,arrow_u,900,0,40,40)
    bt_down = Button(arrow_down,arrow_d,900,720,40,40)

    #permanent text
    Inv_d = "Invoice For"
    Inv_d = font_n.render(Inv_d, True, (0, 0, 0))

    C_name = "[Customer Name]"
    C_name = font.render(C_name, True, (0, 0, 0))

    C_email = "[Customer Email]"
    C_email = font.render(C_email, True, (0, 0, 0))

    Inv_n = "Invoice Number: " + str(inv_number)
    Inv_n = font_n.render(Inv_n, True, (0, 0, 0))

    S_date = "Sent: " + str(now.date())
    S_date = font.render(S_date, True, (0, 0, 0))

    D_date = "Due: "
    D_date = font.render(D_date, True, (0, 0, 0))

    Sub = "Subtotal: "
    Sub = font.render(Sub, True, (0, 0, 0))

    Tax = "Tax: "
    Tax = font.render(Tax, True, (0, 0, 0))
    
    #Position in y of the blits
    Inv_y = 300
    C_y = 325
    E_y = 350
    L_y = 50
    B_y = 425
    M_y = 600
    l_y = 600
    S_y = 575
    T_y = 600
    sub_input = text_box(660,S_y,90,25, "")
    tax_input = text_box(660,T_y,90,25, "")
    #Draw the matrix
    draw_matrix(screen, B_y)
    #While of the loop
    exit_ = False
    while exit_ != True:
        #Buttons dynamics
        bt_more = Button(more,more_b,150,M_y,60,60)
        bt_less = Button(less,less_b,205,l_y,60,60)
        print
        
        clock.tick(60)
        cursor.update()
        screen.blit(pygame.transform.scale(background,(weight,height)),(0,0))
        screen.blit(pygame.transform.scale(logo,(400,200)),(250,L_y))

        #Update the text box
        due_input.update(screen,cursor, True, d_y)
        note_input.update(screen,cursor, False,n_y)
        box_group.update(screen, cursor, False, None)
        sub_input.update(screen,cursor,False,S_y)
        tax_input.update(screen,cursor,False,T_y)
        
        
        #Blit the text
        screen.blit(Inv_d,(150,Inv_y))
        screen.blit(C_name,(150,C_y))
        screen.blit(C_email,(150,E_y))

        screen.blit(Inv_n,(600,Inv_y))
        screen.blit(S_date,(600,C_y))
        screen.blit(D_date,(600,E_y))

        screen.blit(Sub,(585,S_y))
        screen.blit(Tax,(622,T_y))
        
        #Update Buttons
        bt_check.update(screen, cursor)
        bt_down.update(screen,cursor)
        bt_up.update(screen,cursor)
        bt_more.update(screen,cursor)
        bt_less.update(screen,cursor)
        #Update Display
        pygame.display.update()
        global colide
        print(colide)
        for event in pygame.event.get():
            #Update the text of the box
            due_input.text_update(event)
            note_input.text_update(event)
            sub_input.text_update(event)
            tax_input.text_update(event)
            #box_group.update(screen, cursor, False, event)
            rect_group = box_group.update(screen, cursor, False, event)
            if rect_group:
                print("rect_group")
            #print(rect_group)
            if event.type == pygame.QUIT:
                #Exit
                exit_ = True
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(bt_check.rect):
                    print("Push Check")
                if cursor.colliderect(bt_down.rect):
                    d_y += scroll
                    n_y += scroll
                    Inv_y += scroll
                    C_y += scroll
                    E_y += scroll
                    L_y += scroll
                    B_y += scroll
                    M_y += scroll
                    l_y += scroll
                    S_y += scroll
                    T_y += scroll
                    draw_matrix(screen, B_y)
                if cursor.colliderect(bt_up.rect):
                    d_y -= scroll
                    n_y -= scroll
                    Inv_y -= scroll
                    C_y -= scroll
                    E_y -= scroll
                    L_y -= scroll
                    B_y -= scroll
                    M_y -= scroll
                    l_y -= scroll
                    S_y -= scroll
                    T_y -= scroll
                    draw_matrix(screen, B_y)
                if cursor.colliderect(bt_more.rect):
                    d_y -= scroll_
                    n_y -= scroll_
                    Inv_y -= scroll_
                    C_y -= scroll_
                    E_y -= scroll_
                    L_y -= scroll_
                    B_y -= scroll_
                    #M_y -= scroll_
                    #l_y -= scroll_
                    add_row_matrix(screen, B_y)
                if cursor.colliderect(bt_less.rect):
                    d_y += scroll_
                    n_y += scroll_
                    Inv_y += scroll_
                    C_y += scroll_
                    E_y += scroll_
                    L_y += scroll_
                    B_y += scroll_
                    #M_y += scroll_
                    #l_y += scroll_
                    eliminate_row_matrix(screen,B_y)
    pygame.quit()
    
make_invoice_window()
#show_services()
