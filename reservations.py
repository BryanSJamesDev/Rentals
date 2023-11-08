from datetime import date, timedelta
import customer_related_functions
import mysql.connector

def overdue():
    '''To retrieve the reservations ids & Customer ids which are overdue'''
    mycon = mysql.connector.connect(host='localhost', user='csproject', password='2020', database='car_rentals')
    mycursor = mycon.cursor(True)

    sql = 'select c_id, max(c_date) from reservations group by c_id having max(c_date)<=curdate()'
    # retrieving reservations where the reservation has already been closed or is overdue
    mycursor.execute(sql)

    c_idlist = mycursor.fetchall()
    cdict = dict(c_idlist)
    clist = list(cdict.keys())
    rlist = []
