from reportlab import *
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
import pygame
from CLASSES import *
from datetime import datetime

##La parte superior en y es 800
##El limite izquierdo en y es 50
##El limite derecho en y es 500
box_group = pygame.sprite.Group()
draw_m = True
def draw_matrix(screen,y):
    global box_group
    #Matrix of the items
    matrix = [["Item", "Quantity","Price","Amount"],[" "," "," "," "],[" "," "," "," "]]
    x = 0
    box_group.empty()
    for line in matrix:
        x = 0
        y += 30
        for element in line:
            x += 150
            box = text_group(x,y,140,30, element)
            box_group.add(box)
            
def make_invoice_window():
    global box_group
    #Settings of the screen
    pygame.init()
    weight, height = 952,768
    screen = pygame.display.set_mode((weight,height))
    scroll = 10
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
    #Position in y of the blits
    Inv_y = 300
    C_y = 325
    E_y = 350
    L_y = 50
    B_y = 425

    #Draw the matrix
    draw_matrix(screen, B_y)
    #While of the loop
    exit_ = False
    while exit_ != True:
        
        clock.tick(60)
        cursor.update()
        screen.blit(pygame.transform.scale(background,(weight,height)),(0,0))
        screen.blit(pygame.transform.scale(logo,(400,200)),(250,L_y))

        #Update the text box
        due_input.update(screen,cursor, True, d_y)
        note_input.update(screen,cursor, False,n_y)
        box_group.update(screen, cursor, True, None)
        
        
        #Blit the text
        screen.blit(Inv_d,(150,Inv_y))
        screen.blit(C_name,(150,C_y))
        screen.blit(C_email,(150,E_y))

        screen.blit(Inv_n,(600,Inv_y))
        screen.blit(S_date,(600,C_y))
        screen.blit(D_date,(600,E_y))
        
        #Update Buttons
        bt_check.update(screen, cursor)
        bt_down.update(screen,cursor)
        bt_up.update(screen,cursor)

        #Update Display
        pygame.display.update()
        for event in pygame.event.get():
            #Update the text of the box
            due_input.text_update(event)
            note_input.text_update(event)
            box_group.update(screen, cursor, True, event)
            #box_group.text_update(event)
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
                    draw_matrix(screen, B_y)
                if cursor.colliderect(bt_up.rect):
                    d_y -= scroll
                    n_y -= scroll
                    Inv_y -= scroll
                    C_y -= scroll
                    E_y -= scroll
                    L_y -= scroll
                    B_y -= scroll
                    draw_matrix(screen, B_y)
    pygame.quit()
    
make_invoice_window()
