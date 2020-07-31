import csv
import pygame
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime
colide = False
matrix = [["Item", "Quantity","Price","Amount"],["","","",""],["","","",""],["","","",""]]

class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, 0,0,1,1)
    def update(self):
        pygame.init()
        self.left, self.top = pygame.mouse.get_pos()
        
#Class to create the buttons, require two images for animation
class Button(pygame.sprite.Sprite):
    def __init__(self, image1, image2, x, y,scale_x,scale_y):
        pygame.sprite.Sprite.__init__(self)
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image_normal = pygame.transform.scale(image1,(self.scale_x,self.scale_y))
        self.image_select = pygame.transform.scale(image2,(self.scale_x,self.scale_y))
        self.image_current = self.image_normal
        self.rect = self.image_current.get_rect()
        self.rect.left, self.rect.top = (x,y)
    def update(self, screen, cursor):
        if cursor.colliderect(self.rect):
            self.image_current = self.image_select
        else:
            self.image_current = self.image_normal
        #screen.blit(pygame.transform.scale(self.image_current,(self.scale_x,self.scale_y)),self.rect)
        screen.blit(self.image_current,self.rect)

class Button_(pygame.sprite.Sprite):
    def __init__(self, image1, image2, x, y,scale_x,scale_y, row, colum):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.colum = colum
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image_normal = pygame.transform.scale(image1,(self.scale_x,self.scale_y))
        self.image_select = pygame.transform.scale(image2,(self.scale_x,self.scale_y))
        self.image_current = self.image_normal
        self.rect = self.image_current.get_rect()
        self.rect.left, self.rect.top = (x,y)
    def update(self, screen, cursor):
        if cursor.colliderect(self.rect):
            self.image_current = self.image_select
        else:
            self.image_current = self.image_normal
        #screen.blit(pygame.transform.scale(self.image_current,(self.scale_x,self.scale_y)),self.rect)
        screen.blit(self.image_current,self.rect)
    def get_pos(self):
        return (self.row,self.colum)
        
class csv_class:
    def __init__(self, archive, method):
        self.archive = self.read(archive, method)
    #return the matrix in the csv
    def read(self, archive, method):
        f = open(archive, method)
        data = csv.reader(f)
        data = [row for row in data]
        #Delete the empty spaces in the matrix
        for i in data:
            if i == []:
                data.remove(i)
        return data

    #Modify the variable matrix
    def write(self, matrix):
        self.archive = matrix

    #return the matrix in the csv
    def get_matrix(self):
        return self.archive

    #Update the csv with the variable matrix
    def update_matrix(self, archive, method):
        a = self.archive
        f = open(archive, method)
        with f:
            writer = csv.writer(f)
            writer.writerows(a)
            
class text_box(pygame.sprite.Sprite):
    def __init__(self, x,y,w,h, text):
        self.y = y
        self.input = pygame.Rect(x,self.y,w,h)
        self.h = h
        self.w = w
        self.color_i = (0,0,0)
        self.color_a = (255,255,255)
        self.color = self.color_i
        self.active = False
        self.text = text
        self.txt = ""

    def update(self,screen,cursor, dynamic, y):
        self.input.y = y
        font = pygame.font.Font("times.ttf", 20)
        self.txt = font.render(self.text, True, (0,0,0))
        if dynamic:
            width = max(100, self.txt.get_width()+10)
            self.input.w = width
        pygame.draw.rect(screen, self.color, self.input, 1)
        screen.blit(self.txt, (self.input.x+2, self.input.y+1))
        
    def text_update(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input.collidepoint(event.pos):
                # Set the value of the variable
                self.active= not self.active
            else:
                self.active = False
            #Set the current color of the box
            self.color = self.color_a if self.active else self.color_i
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
    def edit_text(self, text):
        self.text = text
    def get_text(self):
        return self.text

class text_group(pygame.sprite.Sprite):
    global matrix
    pygame.init()
    def __init__(self, x,y,w,h, text, row, colum):
        pygame.init()
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.colum = colum
        self.y = y
        self.input = pygame.Rect(x,self.y,w,h)
        self.h = h
        self.w = w
        self.color_i = (0,0,0)
        self.color_a = (255,255,255)
        self.color = self.color_i
        self.active = False
        self.text = text
        self.txt = None
        
    def update(self,screen,cursor, dynamic, event):
            
        pygame.init()
        font = pygame.font.Font("times.ttf", 20)
        self.txt = font.render(self.text, True, (0,0,0))
        if dynamic:
            width = max(150, self.txt.get_width()+10)
            self.input.w = width
        pygame.draw.rect(screen, self.color, self.input, 1)
        screen.blit(self.txt, (self.input.x+2, self.input.y+1))
        if event != None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input.collidepoint(event.pos):
                    # Set the value of the variable
                    self.active= not self.active
                else:
                    self.active = False
                #Set the current color of the box
                self.color = self.color_a if self.active else self.color_i
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                        matrix[self.row][self.colum] = self.text
                    else:
                        self.text += event.unicode
                        matrix[self.row][self.colum] = self.text
                    
    def get_text(self):
        return self.text

class buttom_text(pygame.sprite.Sprite):
    global matrix
    def __init__(self, x,y,w,h, text, row):
        pygame.sprite.Sprite.__init__(self)
        self.y = y
        self.input = pygame.Rect(x,self.y,w,h)
        self.h = h
        self.w = w
        self.row = row
        self.color_i = (0,0,0)
        self.color_a = (255,255,255)
        self.color = self.color_i
        self.active = False
        self.text = text
        self.txt = None
        self.font = pygame.font.Font("times.ttf", 20)
    def update(self,screen,cursor, event,):
        self.txt = self.font.render(self.text, True, (0,0,0))
        pygame.draw.rect(screen, self.color, self.input, 1)
        screen.blit(self.txt, (self.input.x+2, self.input.y+1))
        if event!= None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input.collidepoint(event.pos):
                    pass
                    
    def get_text(self):
        return self.text

    
class pdf:
    def __init__(self, name, logo):
        self.text = None
        self.name = name
        self.canvas = Canvas(self.name + ".pdf")
        self.logo = logo
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        pdfmetrics.registerFont(TTFont('times','times.ttf'))
        pdfmetrics.registerFont(TTFont('timesb','timesbd.ttf'))
        if self.logo == "logo.png":
            self.canvas.drawImage(self.logo,50, 700, mask = "auto")

    def write_string(self,txt,x,y, font,size):
        self.canvas.setFont(font, size)
        self.canvas.drawString(x,y,txt)

    def write_text(self,txt,x,y, font,size):
        self.canvas.setFont(font, size)
        self.text = self.canvas.beginText(x,y)
        self.text.setFont(font, size)
        self.text.textLines(txt)
        self.canvas.drawText(self.text)
        
    def save(self):
        self.canvas.save()



#load the csv
#archive_csv = csv_class("ScoreBoard.csv","rt")
#matrix_csv = archive_csv.get_matrix()

"""To write matrix in the variable"""
# archivo_csv.write("Nueva matriz")
"""To save the matrix in the csv"""
# archivo_csv.update_matriz("matriz.csv","w")
"""NOTE"""
#First writes the variable and after saves the matrix in the csv

#Class to know the position of the cursor

