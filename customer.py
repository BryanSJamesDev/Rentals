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
    while True:
        try:
            mob1 = int(input('Enter mobile 1: '))
            if len(str(mob1)) != 8:
                print('Mobile number should have 8 digits only')
                continue
            sql = 'Select * from customer where mobile_1 = %d' % mob1
            mycursor.execute(sql)
            if mycursor.rowcount:
                print('Mobile Number already exists! Please try again')
                continue
        except:
            print('Invalid Mobile Number entered! Please try again')
            continue
        break

    while True:
        try:
            mob2 = int(input('Enter mobile 2: '))
            if len(str(mob2)) != 8:
                print('Mobile number should have 8 digits only')
                continue
        except:
            print('Invalid Mobile Number entered! Please try again')
            continue
        break

    while True:
        email = input('Enter email address: ').lower()
        sql = "select * from customer where email='%s'" % email
        mycursor.execute(sql)
        mycursor.fetchall()
        if mycursor.rowcount:
            print("This email already exists! Please try again!")
            continue
        break

    address = input('Enter address: ').upper()

    data = (c_id, name, mob1, mob2, email, address, 0, 'I')  # 0 refers to reservation count while I is for status
    sql = "insert into customer values ('%s', '%s', %d, %d, '%s', '%s', %d, '%s')" % data

    mycursor.execute(sql)
    mycon.commit()
    mycon.close()

    print('\nCustomer successfully added')
    print("Your Customer_id is", c_id)

    return c_id

def UPDATE():
    '''To update customer details'''
    mycon = mysql.connector.connect(host='localhost',
                                   database='car_rentals',
                                   user='csproject',
                                   password='2020')
    mycursor = mycon.cursor(buffered=True)

    c_id = input("Enter Customer ID: ")

    sql = "select mobile_1, mobile_2, email, address from customer where c_id = '%s'" % c_id

    mycursor.execute(sql)

    data = mycursor.fetchall()

    b = mycursor.rowcount
