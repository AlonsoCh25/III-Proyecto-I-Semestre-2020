from reportlab import *
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
import pygame
from CLASSES import *
from datetime import datetime

##La parte superior en y es 800
##El limite izquierdo en y es 50
##El limite derecho en y es 500

def create_pdf(name):
    canvas = Canvas(name + ".pdf")
    canvas.save()
    
def edit_pdf(name, txt):
    posx = 0
    posy = 0 
    pygame.font.init()
    font = pygame.font.Font("triforce.ttf",35)
    canvas = Canvas(name + ".pdf")
    write_pdf(txt,canvas, posx,posy)
    canvas.drawImage("logo.png",150, 600, mask = "auto")
    canvas.save()

def write_pdf(txt,canvas, posx, posy):
    def update(line):
        canvas.drawString(posx, posy, line)
    text = txt.strip().replace('\r','').split('\n')
    for line in text:
        update(line)
        y -= 10
        
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
    due_input = pygame.Rect(645, 350, 140, 25)

    #Color of the box
    color_i_due = (0,0,0)
    color_a_due = (255,255,255)
    color_due = color_i_due

    #Set the initial active of the box
    active_due = False

    
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
    
    #dynamic text
    due_date = ""

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

        #Render text
        txt = font.render(due_date, True, (0,0,0))

        #Scale the box of the text
        width = max(100, txt.get_width()+10)
        due_input.w = width
        
        #Blit the text
        screen.blit(Inv_d,(150,300))
        screen.blit(C_name,(150,325))
        screen.blit(C_email,(150,350))
        screen.blit(txt, (due_input.x+2, due_input.y+1))

        screen.blit(Inv_n,(600,300))
        screen.blit(S_date,(600,325))
        screen.blit(D_date,(600,350))

        #Blits of the box text
        pygame.draw.rect(screen, color_due, due_input, 1)
        
        #Update Buttons
        bt_check.update(screen, cursor)

        #Update Display
        pygame.display.update()
        for event in pygame.event.get():
            #Load the events
            if event.type == pygame.QUIT:
                #Exit
                exit_ = True
                pygame.quit()
                break
            #Define the actions of the mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if due_input.collidepoint(event.pos):
                    # Set the value of the variable
                    active_due = not active_due
                else:
                    active_due = False
                #Set the current color of the box
                color_due = color_a_due if active_due else color_i_due
            
            #Write text in the box of the screen
            #Add the text to a variable
            if event.type == pygame.KEYDOWN:
                if active_due:
                    if event.key == pygame.K_BACKSPACE:
                        due_date = due_date[:-1]
                    else:
                        due_date += event.unicode
                """if cursor.colliderect(bt_credits.rect):
                    print("Push credits")
                    exit_ = True
                    pygame.quit()
                    credits_window()
                    break
                if cursor.colliderect(bt_exit.rect):
                    print("push_exit")
                    csv_scoreboard.write(matrix)
                    csv_scoreboard.update_matrix("ScoreBoard.csv","w")
                    exit_ = True
                    pygame.quit()
                    break"""
    pygame.quit()
    
make_invoice_window()
