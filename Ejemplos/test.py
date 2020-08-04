from datetime import datetime
date_list = ['2020-08-04', '2020-08-03', '2020-08-02', '2020-08-01', '2020-07-11', '2020-07-03']
now = datetime.now()
date = now.date()
day = now.day
month = now.month
year = now.year
if "2020/08/04" == str(f"{now.year}/{now.month:02d}/{now.day:02d}"):
    pass
for i in date_list:
    print(int(i[8:10]))
    print(i[:7])
    '''if str(f"{year}-{month:02d}") == i[:7] and int(i[8:10]) > 7:
        if day - 7 <= int((i[2])[8:10]) <= day:
            print('hola')
    elif str(f"{year}-{month:02d}") == i[:7] and int(i[8:10]) <= 7:
        resta = day - 7
        if resta <= 0:
            month2 = month - 1
            day2 = 31
            day2 += resta
            if month2 <= int(i[5:7]) and day2 <= int(i[8:10]):
                print('hola1')
            elif month >= int(i[5:7]) and day >= int(i[8:10]):
                print('hola2')'''

    if str(f"{year}") == i[:4]:
        month2 = month - 1
        print(0 <= int(i[8:10]) <= day)
        print(month == int(i[5:7]))
        if 0 <= int(i[8:10]) <= day and month == int(i[5:7]):
            print('hola3')
        if day <= int(i[8:10]) <= 31 and month2 == int(i[5:7]):
            print('hola3')