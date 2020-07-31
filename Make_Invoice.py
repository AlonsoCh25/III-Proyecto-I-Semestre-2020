from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
import pygame
from CLASSES import *
from datetime import datetime
import numpy as np
import time
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('times','times.ttf'))
pdfmetrics.registerFont(TTFont('timesb','timesbd.ttf'))
##La parte superior en y es 800
##El limite izquierdo en y es 50
##El limite derecho en y es 500
archive_csv = csv_class("services.csv","rt")
matrix_services = archive_csv.get_matrix()
box_group = pygame.sprite.Group()
buttons = []

archive_c = csv_class("data_users.csv","rt")
matrix_data = archive_c.get_matrix()

buttons_box = pygame.sprite.Group()
buttons_services = []
show_services = False

rect_select = None
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


    


def make_invoice_window():
    global box_group, matrix_data, window_c,buttons, show_services,matrix_services, buttons_services, buttons_box,matrix, rect_select
    def create_pdf():
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
        n_pdf.write_string(" Impuestos " + tax_input.get_text()+"%", 475,y-30,"times",12)
        n_pdf.write_string("         Total " + total_input.get_text(), 475,y-45,"times",12)
        n_pdf.save()
        
    #Settings of the screen
    pygame.init()
    weight, height = 952,768
    screen = pygame.display.set_mode((weight,height))
    scroll = 10
    scroll_ = 30
    #List of the invoice numers
    archive_csv = csv_class("invoices.csv","rt")
    matrix_csv = archive_csv.get_matrix()
    inv_number = 1
    if matrix_csv[0] != []:
        for row in matrix_csv:
            inv_number = int(row[0]) + 1
    print(matrix_csv)
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
        
        clock.tick(60)
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
    
make_invoice_window()
#show_services()
