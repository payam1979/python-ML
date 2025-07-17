import re
import requests
from bs4 import BeautifulSoup
import mysql.connector
from sklearn import tree

x = []
y = []

vk = ""
car_list_database = []
cnx = mysql.connector.MySQLConnection(user='root', password="Parmis1388@", host='localhost',
                                              database='employees')

mycursor = cnx.cursor()
sql = "DELETE  FROM mycars WHERE milage = 10000000 or owner = 1000 or accident = 1000 or price = 0"
mycursor.execute(sql)
cnx.commit()
sql1 = "select made, milage, owner, accident, price from mycars where name = "

a = input("please give me the name of car you searching for like the example:(toyota corolla or ford f-150 or Ford Super Duty F-250) = ")

d = ""
b = a.split()
for i in range(0, len(b)):
    c = b[i].capitalize()
    d = d + " " + c
d = d.strip()


b = '\'' + d + '\''
sql2 = sql1 + b
mycursor.execute(sql2)
my_result = mycursor.fetchall()
#print(my_result)
for item in my_result:
   car_list_database.append(item)

#print(car_list_database)
#print(len(car_list_database))
mycursor.close()
cnx.close()

new = []
year = 0
mile = 0
ow = 0
acc = 0


if len(car_list_database) == 0:
   print("Name is incorrect or I don`t have any data for it")


elif len(car_list_database) < 50:
   print("I have less than 50 of this car in my database, so there will be a big chance for misscalculation")
   year = int(input("which year was the car made? "))
   mile = int(input("how many miles does the car worked? "))
   ow = int(input("how many owner does the car had before? "))
   acc = int(input("how many accident does the car had before? "))

else:
   year = int(input("which year was the car made? "))
   mile = int(input("how many miles does the car worked? "))
   ow = int(input("how many owner does the car had before? "))
   acc = int(input("how many accident does the car had before? "))


new = [(year, mile, ow, acc)]

if new == [(0, 0, 0, 0)]:
   print("I am so sorry")
else:
   for item in car_list_database:
      x.append(item[0:4])
      y.append(item[4])

   clf = tree.DecisionTreeClassifier()
   clf = clf.fit(x, y)

   answer = clf.predict(new)
   print("answer is : ", answer[0])


