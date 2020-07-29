import pygame
from CLASSES import *

#Creation of groups and cursor
buttons = pygame.sprite.Group()
cursor = Cursor()
FPS = 60

#Creation of buttons
'''img_bt_createPDF1 = pygame.image.load("Images/")
img_bt_createPDF2 = pygame.image.load("Images/")
img_bt_managerPDF1 = pygame.image.load("Images/")
img_bt_managerPDF2 = pygame.image.load("Images/")
img_bt_report1 = pygame.image.load("Images/")
img_bt_report2 = pygame.image.load("Images/")
img_bt_services1 = pygame.image.load("Images/")
img_bt_services2 = pygame.image.load("Images/")
img_bt_addUser1 = pygame.image.load("Images/")
img_bt_addUser2 = pygame.image.load("Images/")
img_bt_manageUser1 = pygame.image.load("Images/")
img_bt_manageUser2 = pygame.image.load("Images/")

bt_createPDF = Button(img_bt_createPDF1, img_bt_createPDF2, x, y, scale_x, scale_y)
bt_managerPDF = Button(img_bt_managerPDF1, img_bt_managerPDF2, x, y, scale_x, scale_y)
bt_report = Button(img_bt_report1, img_bt_report2, x, y, scale_x, scale_y)
bt_services = Button(img_bt_services1, img_bt_services2, x, y, scale_x, scale_y)
bt_addUser = Button(img_bt_addUser1, img_bt_addUser2, x, y, scale_x, scale_y)
bt_manageUser = Button(img_bt_manageUser1, img_bt_manageUser2, x, y, scale_x, scale_y)'''

def main_menu_window():
    global FPS

    pygame.init()
    width, height = 600, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()
    background = pygame.image.load("images/background.png")
    background = pygame.transform.scale(background, (width, height))
    logo = pygame.image.load("Logo.png")
    logo = pygame.transform.scale(logo, (400, 200))

    exit_ = False
    while exit_ != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit
                exit_ = True
                pygame.quit()
                break

        clock.tick(60)
        cursor.update()
        screen.blit(background, (0,0))
        print('screen blit')
        screen.blit(logo, (0,0))

    pygame.quit()

main_menu_window()