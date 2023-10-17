import mysql.connector

def viewall():
    """To view the details of all cars stored in the car table"""
    print()
    mycon = mysql.connector.connect(host='localhost', database='car_rentals', user='csproject', password='2020')
    mycursor = mycon.cursor(buffered=True)
    sql = 'Select car_id, company, model, year, cost_pday from cars order by company, model, year, car_id'
    mycursor.execute(sql)
    data = mycursor.fetchall()
    if mycursor.rowcount:
        header = ['CAR ID', 'COMPANY', 'MODEL', 'YEAR', 'COST/DAY']
        print('{:^15s}|{:^25s}|{:^25s}|{:^6s}|{:^10s}'.format(*header))
        # Headings of the table
        print('%15s|%25s|%25s|%6s|%10s' % ('', '', '', '', ''))  # Leave a line after showing the headings
        for i in data:
            print('{:^15s}|{:^25s}|{:^25s}|{:^6d}|{:^10.3f}'.format(*i))
        # Printing each record
        # To show the number of cars available, rented and under maintenance
        sql = 'select count(*) from cars where status = "A"'
        mycursor.execute(sql)
        no_available = mycursor.fetchall()[0][0]
        sql = 'select count(*) from cars where status = "R"'
        mycursor.execute(sql)
        no_rented = mycursor.fetchall()[0][0]
        sql = 'select count(*) from cars where status = "M"'
        mycursor.execute(sql)
        no_main = mycursor.fetchall()[0][0]
        total = no_available + no_rented + no_main
        print()
        print('Number of Available cars =', no_available)
        print('Number of Rented cars =', no_rented)
        print('Number of cars under maintenance =', no_main)
        print('Total Number of cars =', total)
    else:
        print('No records available')
    mycon.close()

def viewone():
    '''To display the record of a particular car'''
    mycon = mysql.connector.connect(host='localhost', database='car_rentals', user='csproject', password='2020')
    mycursor = mycon.cursor(buffered=True)
    car_id = input("Enter the car_id: ").upper()
    print()
    sql = "select * from cars where car_id = '%s'" % car_id
    mycursor.execute(sql)
    data = mycursor.fetchall()
    if mycursor.rowcount:
        data = data[0]
        header = ['CAR_ID', 'COMPANY', 'MODEL', 'YEAR', 'ENGINE', 'REAR AC', 'NO OF SEATS', 'INFOTAINMENT SYSTEM', 'COST PER DAY', 'STATUS']
        engine = {'E': 'Electric', 'P': 'Petrol', 'D': 'Diesel'}
        status = {'A': 'Available', 'R': 'Rented', 'M': 'Maintenance'}
        choice = {'Y': 'Available', 'N': 'Not available'}
        for i in range(len(header)):
            if i in (0, 1, 2):
                print('{:^21s}:{:^25s}'.format(header[i], data[i]))
            elif i in (3, 6):
                print('{:^21s}:{:^25d}'.format(header[i], data[i]))
            elif i == 4:
                print('{:^21s}:{:^25s}'.format(header[i], engine[data[4]])
            elif i in (5, 7):
                print('{:^21s}:{:^25s}'.format(header[i], choice[data[i]])
            elif i == 8:
                print('{:^21s}:{:^25.3f}'.format(header[i], data[8])
            else:
                print('{:^21s}:{:^25s}'.format(header[i], status[data[9]])
    else:
        print("CAR_ID does not exist")
