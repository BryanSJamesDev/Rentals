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

    if len(clist):
        sql = 'select c_id from customer where c_id IN %s and status = "A" order by length(c_id),c_id' % str(tuple(clist))
        mycursor.execute(sql)

        clist = mycursor.fetchall()
        clist = [i[0] for i in clist]
        temp = list(cdict.keys())
        for i in temp:
            if i not in clist:
                del cdict[i]

        for i in cdict:
            sql = 'select r_id from reservations where c_id = "%s" and c_date = "%s" order by length(r_id), r_id' % (i, cdict[i])
            mycursor.execute(sql)
            a = mycursor.fetchone()[0]
            rlist.append(a)

    mycon.close()
    return rlist, clist

def viewall():
    '''View all reservations'''
    print()
    mycon = mysql.connector.connect(host='localhost', database='car_rentals', user='csproject', password='2020')
    mycursor = mycon.cursor(buffered=True)

    sql = "select * from reservations order by length(r_id),r_id"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    if mycursor.rowcount:
        header = ["Reservation ID", "Car ID", "Customer ID", "Starting date", "Closing date", "Duration", "Total Amount"]

        print('{:^16s}|{:^15s}|{:^13s}|{:^15s}|{:^14s}|{:^10s}|{:^14s}'.format(*header))
        print('{:^16s}|{:^15s}|{:^13s}|{:^15s}|{:^14s}|{:^10s}|{:^14s}'.format('', '', '', '', '', '', ''))

        for i in data:
            print('{:^16s}|{:^15s}|{:^13s}|{:^15s}|{:^14s}|{:^10d}|{:^14.2f}'.format(*i[:3], i[3].strftime('%d-%m-%Y'), i[4].strftime('%d-%m-%Y'), *i[5:]))

    od_r = overdue()[0]

    if len(od_r):
        print('The following are overdue:', *od_r)
    else:
        print('No records exist')
    mycon.close()

def unique(L):
    uniq = []
    for i in L:
        if i not in uniq:
            uniq.append(i)
    return uniq

def new_reservation():
    '''To make a new car reservation'''
    mycon = mysql.connector.connect(host='localhost', database='car_rentals', user='csproject', password='2020')
    mycursor = mycon.cursor(buffered=True)

    while True:
        ask_existing = input('Are you an existing customer? [y/n]: ').upper()
        if ask_existing in ('Y', 'N'):
            break
        else:
            print('Invalid choice entered! Enter the specified choice [y/n]')
