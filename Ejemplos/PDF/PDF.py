from reportlab import *
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
import pygame
from CLASSES import *
from datetime import datetime

##La parte superior en y es 800
##El limite izquierdo en y es 50
##El limite derecho en y es 500
def make_invoice_window(): 
    #Settings of the screen
    pygame.init()
    weight, height = 952,768
    screen = pygame.display.set_mode((weight,height))

    #List of the invoice numers
    archive_csv = csv_class("invoice num.csv","rt")
    matrix_csv = archive_csv.get_matrix()
    inv_number = 1
    if matrix_csv[0] != []:
        for row in matrix_csv:
            for num in row:
                inv_number = int(num) + 1
                
    #Text input
    due_input = text_box(645,350,140,25)
    
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
    
    #Create the buttons and cursor
    cursor = Cursor()
    bt_check = Button(check,check_1,470,700,60,60)

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
    #While of the loop
    exit_ = False
    while exit_ != True:
        clock.tick(60)
        cursor.update()
        screen.blit(pygame.transform.scale(background,(weight,height)),(0,0))
        screen.blit(pygame.transform.scale(logo,(400,200)),(250,50))

        #Update the text box
        due_input.update(screen,cursor)
            
        #Blit the text
        screen.blit(Inv_d,(150,300))
        screen.blit(C_name,(150,325))
        screen.blit(C_email,(150,350))

        screen.blit(Inv_n,(600,300))
        screen.blit(S_date,(600,325))
        screen.blit(D_date,(600,350))
        
        #Update Buttons
        bt_check.update(screen, cursor)

        #Update Display
        pygame.display.update()
        for event in pygame.event.get():
            #Update the text of the box
            due_input.text_update(event)
            
            if event.type == pygame.QUIT:
                #Exit
                exit_ = True
                pygame.quit()
                break

    pygame.quit()
    
make_invoice_window()
