import re
import requests
from bs4 import BeautifulSoup
import mysql.connector


vk = ""
vin_list_database = []
cnx = mysql.connector.MySQLConnection(user='root', password="Parmis1388@", host='localhost',
                                              database='employees')

mycursor = cnx.cursor()
sql = "SELECT vin FROM mycars"

mycursor.execute(sql)

my_result = mycursor.fetchall()

for x in my_result:
    vk = x[0]
    vin_list_database.append(vk)
mycursor.close()
cnx.close()



def miles(x):
    c = ""
    b = x[0].split(',')
    for item in b:
        c = c + item

    d = int(c)
    return d


a = 'https://www.truecar.com/used-cars-for-sale/listings/?page='
#b = "bmw"
#b = input()
#c = b.split()
for i in range(1, 200):



    k = str(i)
    d = a + k
   # print(d)
    r = requests.get(d)
    de = r.text

    soup = BeautifulSoup(de, 'html.parser')
    agahi = soup.findAll("div", attrs = {"data-test":"cardContent"})

    for x in agahi:
         k = ""
         mile = []
         price_p = []
         kt = []
         vin_p = []
         owner_p = []
         accident_p = []
         name_p = []
         made_p = []

         soup1 = BeautifulSoup(str(x), 'html.parser')
         rde = soup1.findAll("div", attrs = {"data-test":"vehicleMileage"})
         price = soup1.findAll("div",  attrs = {"class":"vehicle-card-bottom-pricing-secondary"})
         vin = soup1.findAll("div",  attrs = {"class":"vehicle-card-vin-carousel mt-1 text-xs"})
         owner = soup1.findAll("div", attrs={"class": "vehicle-card-location mt-1 text-xs"})
         name = soup1.findAll("div", attrs={"data-test": "vehicleCardYearMakeModel"})

         for i in range(0, len(rde)):
            item = rde[i]
            rse = item.text
            regex = re.findall(r'(\d.*) ', rse)
            if regex != None and regex != []:
               m = miles(regex)
               mile.append(m)
            else:
               m = 10000000
               mile.append(m)

         for i in range(0, len(price)):
             item = price[i]
             ife = item.text
             regex = re.findall(r'.*No.*', ife)
             regex_1 = re.findall(r'.*\$(.*)', ife)

         if regex != None and regex != []:
             p = 0
             price_p.append(p)
             #print(p, "NO")
         elif regex_1 != None and regex_1 != []:
             p = miles(regex_1)
             price_p.append(p)

         for i in range(0, len(vin)):
             item = vin[i]
             vin_1 = item.text
             regex = re.findall(r'VIN(.*)', vin_1)
         if regex != None and regex != []:
             p = regex[0]
             vin_p.append(p)

         for i in range(0, len(owner)):
             item = owner[i]
             owner_1 = item.text
             regex = re.findall(r'(.{2})Owner', owner_1)
         if regex != None and regex != []:
             p = int(regex[0])
             k = owner_1[0:2]
             if k == "No":
                 n = 0
             else:
                 n = int(k)
             owner_p.append(p)
             accident_p.append(n)
         else:
            p = 1000
            n = 1000
            owner_p.append(p)
            accident_p.append(n)

         for i in range(0, len(name)):
             item = name[i]
             name_1 = item.text
             regex = re.findall(r'\d{4}\s.*', name_1)
         if regex != None and regex != []:
             p = (regex[0])

             name_a = ""
             l = p.split()
             made = int(l[0])
             for i in range(1, len(l)):
                 name_l = l[i]
                 name_a = name_a + " " + name_l
                 name_f = name_a.strip()
             name_p.append(name_f)
             made_p.append(made)


         for i in range(0, len(vin_p)):
             ja = (vin_p[i], name_p[i], made_p[i], mile[i], owner_p[i], accident_p[i], price_p[i])
             kt.append(ja)
            # print(ja)
         if kt != []:
             for i in range(0, len(kt)):
                jav = kt[i]
                vin_last = jav[0]
                name_last = jav[1]
                made_last = jav[2]
                milage_last = jav[3]
                owner_last = jav[4]
                accident_last = jav[5]
                price_last = jav[6]

             if vin_last not in vin_list_database:
                print()
                cnx = mysql.connector.MySQLConnection(user='root', password="Parmis1388@", host='localhost',
                                              database='employees')

                mycursor = cnx.cursor()
                sql = "INSERT INTO mycars (vin, name, made, milage, owner, accident, price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                value = (vin_last, name_last, made_last, milage_last, owner_last, accident_last, price_last)
                mycursor.execute(sql, value)

                cnx.commit()
                mycursor.close()
                cnx.close()