from reportlab import *
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
import pygame
from CLASSES import *

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
    
    #Set initial clock
    clock = pygame.time.Clock()
    
    #Images of the screen
    background = pygame.image.load("background.png")
    
    #Create the buttons and cursor
    cursor = Cursor()
    #bt_credits = Button(img_credits,img_credits_b,(weight-bt_weight-10),0,bt_weight,bt_heigth)
    
    #While of the loop
    exit_ = False
    while exit_ != True:
        clock.tick(60)
        screen.blit(pygame.transform.scale(background,(weight,height)),(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            #Load the events
            if event.type == pygame.QUIT:
                #Exit
                exit_ = True
                pygame.quit()
                break
            #Define the actions of the mouse button
            """if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(bt_credits.rect):
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
