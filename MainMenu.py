import pygame
from datetime import datetime
from CLASSES import *


#Creation of groups and cursor
buttons_main = pygame.sprite.Group()
buttons_servicesGroup = pygame.sprite.Group()
buttons_box_s = pygame.sprite.Group()
box_group_s = pygame.sprite.Group()
buttons_invoiceGroup = pygame.sprite.Group()
buttons_box_i = pygame.sprite.Group()
box_group_i = pygame.sprite.Group()
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

bt_createInvoice = Button(img_bt_createPDF1, img_bt_createPDF2, (width/4) + 50, 400, scale_x, scale_y)
bt_manageInvoice = Button(img_bt_managerPDF1, img_bt_managerPDF2, (width/4) + 50 , 550, scale_x, scale_y)
bt_report = Button(img_bt_report1, img_bt_report2, (width/4) + 50, 700, scale_x, scale_y)
bt_services = Button(img_bt_services1, img_bt_services2, (width/2) + 25, 400, scale_x, scale_y)
bt_addUser = Button(img_bt_addUser1, img_bt_addUser2, (width/2) + 25, 550, scale_x, scale_y)
bt_manageUser = Button(img_bt_manageUser1, img_bt_manageUser2, (width/2) + 25, 700, scale_x, scale_y)
bt_exit = Button(img_bt_exit1, img_bt_exit2, width - 175, height - 100, scale_x, scale_y)
buttons_main.add(bt_createInvoice, bt_manageInvoice, bt_report, bt_services, bt_addUser, bt_manageUser, bt_exit)

bt_return_s = Button(img_bt_return1, img_bt_return2, width - 160 , 10, scale_x, scale_y)
bt_more_s = Button(more, more_b, 650, 210, 60, 60)
bt_less_s = Button(less, less_b, 650, 270, 60, 60)
buttons_servicesGroup.add(bt_return_s, bt_more_s, bt_less_s)

bt_return_i = Button(img_bt_return1, img_bt_return2, width - 160 , 10, scale_x, scale_y)
buttons_invoiceGroup.add(bt_return_i)


archive_csv = csv_class("Invoices.csv", "rt")
matrix_invoices = archive_csv.get_matrix()


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


def add_row_matrix_services(y):
    global matrix_services
    matrix_services += [["", ""]]
    draw_matrix_services_s(y)


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

        clock.tick(60)
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

def draw_matrix_invoices(y):
    global box_group_i, matrix_invoices, buttons_invoice

    #Matrix of the services
    x = 0
    row = 0
    box_group_i.empty()
    for line in matrix_invoices:
        row +=1
        colum = 0
        x = 0
        y += 30
        if True:
            for element in line:
                if colum == 0:
                    colum += 1
                    x += 50
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
                        box = text_box_invoices(x,y,150,30, element, row-1, colum-1)
                        box_group_i.add(box)
                    elif colum == 3:
                        colum += 1
                        x += 150
                        box = text_box_invoices(x, y, 150, 30, element, row - 1, colum - 1)
                        box_group_i.add(box)
                    elif colum == 4:
                        colum += 1
                        x += 150
                        bt_trash = Button_(img_trash1, img_trash2, x, y + 2, 25, 25, row - 1, colum - 1)
                        buttons_invoiceGroup.add(bt_trash)
                    else:
                        colum += 1
                        x += 30
                        bt_inspect = Button_(img_inspect1, img_inspect2, x, y + 2, 25, 25, row - 1, colum - 1)
                        buttons_invoiceGroup.add(bt_inspect)
def manage_invoices_window():
    global FPS, cursor, width, height, buttons_box_i, buttons_, matrix_invoices

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Services Window")
    clock = pygame.time.Clock()
    background = pygame.image.load("Images/background.png")
    background = pygame.transform.scale(background, (width, height))
    logo = pygame.image.load("Images/Logo.png")
    logo = pygame.transform.scale(logo, (300, 150))
    font = pygame.font.Font("times.ttf", 20)

    draw_matrix_invoices(210)
    number_box = text_box(50, 210, 150, 30, "Invoice Number")
    detail_box = text_box(200, 210, 300, 30, "Invoice Detail")
    date_box = text_box(500, 210, 150, 30, "Invoice Date")
    price_box = text_box(650, 210, 150, 30, "Invoice Total")

    services_txt = "Invoices Manager"
    services_txt = font.render(services_txt, True, (0, 0, 0))

    exit_ = False
    while exit_ != True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit
                exit_ = True
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(bt_return_i.rect):
                    archive_csv.write(matrix_invoices)
                    archive_csv.update_matrix("Invoices.csv", "w")
                    main_menu_window()
                    exit_ = True
                    pygame.quit()

        clock.tick(60)
        screen.blit(background, (0, 0))
        screen.blit(logo, (round((width / 2)) - 150, 25))
        screen.blit(services_txt, (round(width / 2 - 80), 185))
        cursor.update()
        number_box.update(screen, cursor, False, 210)
        detail_box.update(screen, cursor, False, 210)
        date_box.update(screen, cursor, False, 210)
        price_box.update(screen, cursor, False, 210)
        box_group_i.update(screen, cursor, False, 240)
        buttons_invoiceGroup.update(screen, cursor)
        pygame.display.update()

    pygame.quit()
def main_menu_window():
    global FPS, cursor, buttons_main, width, height

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
                    manage_invoices_window()
                    exit_ = True
                    pygame.quit()
                elif cursor.colliderect(bt_report.rect):
                    pass
                elif cursor.colliderect(bt_services.rect):
                    services_window()
                    exit_ = True
                    pygame.quit()
                    break
                elif cursor.colliderect(bt_addUser.rect):
                    pass
                elif cursor.colliderect(bt_manageUser.rect):
                    pass

        clock.tick(60)
        cursor.update()
        screen.blit(background, (0, 0))
        screen.blit(welcome_txt, (10, 5))
        screen.blit(function_txt, ((round(width/2)) - 210, 350))
        screen.blit(date, (750, 5))
        screen.blit(logo, (round((width/2)) - 200, 50))
        buttons_main.update(screen, cursor)

        pygame.display.update()

    pygame.quit()

main_menu_window()