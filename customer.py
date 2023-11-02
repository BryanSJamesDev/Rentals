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

    if b == 0:
        print('Customer does not exist')
    else:
        data = data[0]  # Taking the tuple of the list
        mob1, mob2, email, address = data

        while True:
            print()
            print("What do you wish to change?")
            print("1. Mobile 1")
            print("2. Mobile 2")
            print("3. Email")
            print("4. Address")
            print('5. Save Changes')

            while True:
                choice = input("Enter your choice: ")
                if len(choice) != 1 or not choice.isdigit() or choice not in "12345":
                    print("Invalid choice! Please try again")
                else:
                    break

            if choice == "1":
                while True:
                    try:
                        mob1 = int(input('Enter mobile 1: '))
                        if len(str(mob1)) != 8:
                            raise Exception
                        sql = 'select * from customer where mobile_1 = %d' % mob1
                        mycursor.execute(sql)
                        mycursor.fetchall()
                        if mycursor.rowcount:
                            print("This number already exists! Please try again!")
                            continue
                    except:
                        print('Invalid Mobile Number entered! Please try again')
                        continue
                    break

            elif choice == "2":
                while True:
                    try:
                        mob2 = int(input('Enter mobile 2: '))
                        if len(str(mob2)) != 8:
                            raise Exception
                    except:
                        print('Invalid Mobile Number entered! Please try again')
                        continue
                    break

            elif choice == "3":
                while True:
                    email = input('Enter email address: ').lower()
                    sql = "select email from customer where email = '%s'" % email
                    mycursor.execute(sql)
                    mycursor.fetchall()
                    if mycursor.rowcount:
                        print("This email already exists! Please try again!")
                        continue
                    break

            elif choice == '4':
                address = input('Enter address: ').upper()
            else:
                break

            database = (mob1, mob2, email, address, c_id)
            sql = "UPDATE customer SET mobile_1 = %d, mobile_2 = %d, email = '%s', address = '%s' WHERE c_id = '%s'" % database
            mycursor.execute(sql)
            mycon.commit()

            print("Customer details updated")

    mycon.close()

def DELETE():
    '''To delete customer from table'''
    mycon = mysql.connector.connect(host='localhost',
                                   database='car_rentals',
                                   user='csproject',
                                   password='2020')
    mycursor = mycon.cursor(buffered=True)

    while True:
        c_id = input("Enter your customer id: ").upper()

        sql = "select * from customer where c_id = '%s'" % c_id

        mycursor.execute(sql)

        data = mycursor.fetchall()

        h = mycursor.rowcount

        if h == 0:
            print("The customer id does not exist")
        else:
            while True:
                a = input("Do you want to remove '%s' from Customer table?: [Y/N] " % data[0][1]).upper()
                if a not in ('Y', 'N'):
                    print("Invalid choice entered, Enter specified value [Y/N]")
                    continue
                break

            if a == 'Y':
                sql = "DELETE from customer WHERE c_id = '%s'" % c_id
                mycursor.execute(sql)
                mycon.commit()
                print('Customer successfully deleted')

        while True:
            choice = input('Do you wish to delete another customer? [y/n]').upper()
            if choice not in ('Y', 'N'):
                print('Invalid choice entered, Enter the specified choice [y/n]')
                continue
            break

        if choice == 'N':
            break

    mycon.close()

def VIEWONE():
    '''To view the details of a particular customer'''
    mycon = mysql.connector.connect(host='localhost',
                                   database='car_rentals',
                                   user='csproject',
                                   password='2020')
    mycursor = mycon.cursor(buffered=True)

    c_id = input('Enter Customer ID: ').upper()
    sql = 'Select * from customer where c_id="%s"' % c_id
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print()
    header = ['CUSTOMER ID', 'NAME', 'MOBILE 1', 'MOBILE 2', 'EMAIL', 'ADDRESS', 'RESERVATION COUNT', 'STATUS']

    if mycursor.rowcount:
        data = data[0]
        status = {'I': 'Inactive', 'A': 'Active'}
        for i in range(8):
            if i in (0, 1, 4, 5):
                print('{:^19s}:{:^50s}'.format(header[i], data[i]))
            elif i in (2, 3, 6):
                print('{:^19s}:{:^50d}'.format(header[i], data[i]))
            else:
                print('{:^19s}:{:^50s}'.format(header[i], status[data[i]))
    else:
        print('Invalid Customer ID, please try again later')

    mycon.close()
