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
