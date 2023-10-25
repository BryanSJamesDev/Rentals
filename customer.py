import mysql.connector

def ADD():
    '''To add a customer to the customer table'''
    mycon = mysql.connector.connect(host='localhost',
                                   database='car_rentals',
                                   user='csproject',
                                   password='2020')
    mycursor = mycon.cursor(buffered=True)

    sql = 'Select c_id from customer order by length(c_id),c_id'
    mycursor.execute(sql)
    cgen = mycursor.fetchall()
    if mycursor.rowcount:
        cgen = int(cgen[-1][0][1:])
        c_id = 'C' + str(cgen + 1)
    else:
        c_id = 'C1'

    name = input('Enter your name: ').upper()
