import pygame
from datetime import datetime
from CLASSES import *

#Creation of groups and cursor
buttons = pygame.sprite.Group()
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
img_bt_exit2 = pygame.image.load("Images/bt_exit1.png")

bt_createInvoice = Button(img_bt_createPDF1, img_bt_createPDF2, (width/4) + 50, 400, scale_x, scale_y)
bt_manageInvoice = Button(img_bt_managerPDF1, img_bt_managerPDF2, (width/4) + 50 , 550, scale_x, scale_y)
bt_report = Button(img_bt_report1, img_bt_report2, (width/4) + 50, 700, scale_x, scale_y)
bt_services = Button(img_bt_services1, img_bt_services2, (width/2) + 25, 400, scale_x, scale_y)
bt_addUser = Button(img_bt_addUser1, img_bt_addUser2, (width/2) + 25, 550, scale_x, scale_y)
bt_manageUser = Button(img_bt_manageUser1, img_bt_manageUser2, (width/2) + 25, 700, scale_x, scale_y)
bt_exit = Button(img_bt_exit1, img_bt_exit2, width - 175, height - 100, scale_x, scale_y)
buttons.add(bt_createInvoice, bt_manageInvoice, bt_report, bt_services, bt_addUser, bt_manageUser, bt_exit)


def main_menu_window():
    global FPS, cursor, buttons, width, height

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
                    pass
                elif cursor.colliderect(bt_manageInvoice.rect):
                    pass
                elif cursor.colliderect(bt_report.rect):
                    pass
                elif cursor.colliderect(bt_services.rect):
                    pass
                elif cursor.colliderect(bt_addUser.rect):
                    pass
                elif cursor.colliderect(bt_manageUser.rect):
                    pass

        clock.tick(60)
        cursor.update()
        screen.blit(background, (0, 0))
        screen.blit(welcome_txt, (10, 5))
        screen.blit(function_txt, ((width/2) - 210, 350))
        screen.blit(date, (750, 5))
        screen.blit(logo, ((width/2) - 200, 50))
        buttons.update(screen, cursor)

        pygame.display.update()

    pygame.quit()

main_menu_window()