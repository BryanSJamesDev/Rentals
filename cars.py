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

def add_car():
    '''Adds a car record to the car table'''
    mycon = mysql.connector.connect(host='localhost', database='car_rentals', user='csproject', password='2020')
    mycursor = mycon.cursor(buffered=True)
    while True:  # Checking whether car already exists in the table
        CAR_ID = input("Enter the number plate: ").upper()
        sql = 'Select * from cars where car_id = "%s"' % CAR_ID
        mycursor.execute(sql)
        if mycursor.rowcount:
            print('Error! Car already exists in the table')
            continue
        break
    COMPANY = input("Enter company name: ").upper()
    MODEL_NAME = input("Enter the model name: ").upper()
    while True:
        YEAR = input("Enter the year of production: ")
        if len(YEAR) == 4 and YEAR.isdigit():
            YEAR = int(YEAR)
        else:
            print("Invalid Value Entered! Please enter a 4 digit number")
            continue
        break
    while True:
        ENGINE = input("Enter the engine type [E/P/D]: ").upper()
        if ENGINE in ('E', 'P', 'D'):
            pass
        else:
            print("Invalid Value Entered! Please enter the specified values [E/P/D]")
            continue
        break
    while True:
        REAR_AC = input("Rear AC available? [Y/N]: ").upper()
        if REAR_AC in ('Y', 'N'):
            pass
        else:
            print("Invalid Value Entered! Please enter the specified values [Y/N]")
            continue
        break
    while True:
        NO_SEATS = input("Enter the number of seats: ")
        if NO_SEATS.isdigit() and int(NO_SEATS) <= 16:
            NO_SEATS = int(NO_SEATS)
            pass
        else:
            print("Invalid Value Entered! Please enter a number less than 17")
            continue
        break
    while True:
        IFOSYS = input("Infotainment system available? [Y/N]: ").upper()
        if IFOSYS in ('Y', 'N'):
            pass
        else:
            print("Invalid!!! Please enter specified values [Y/N]")
            continue
        break
    while True:
        try:
            COST_PDAY = float(input("Enter the cost per day (In KWD): ")
            if COST_PDAY <= 0:
                raise Exception  # Raises an error (goes to the except block) if the cost entered is negative
        except:
            print('Invalid value! Please enter a valid positive decimal number')
            continue
        break
    DATA = (CAR_ID, COMPANY, MODEL_NAME, YEAR, ENGINE, REAR_AC, NO_SEATS, IFOSYS, COST_PDAY, "A")
    sql = "insert into cars values('%s', '%s', '%s', %d, '%s', '%s', %d, '%s', %f, '%s')" % DATA
    mycursor.execute(sql)
    mycon.commit()
    mycon.close()
    print("Car added successfully")

def DEL_CAR():
    '''Deletes a car record from the table'''
    mycon = mysql.connector.connect(host='localhost', database='car_rentals', user='csproject', password='2020')
    mycursor = mycon.cursor(buffered=True)
    while True:
        sql = "select CAR_ID from cars where status != 'r'"  # Allows only Available/under maintenance cars to be deleted
        mycursor.execute(sql)
        caridlist = mycursor.fetchall()
        caridlist = [i[0] for i in caridlist]  # Extracts each carid from its tuple and generates a list of car ids
        sql = "select CAR_ID from cars where status = 'r'"
        mycursor.execute(sql)
        rented = mycursor.fetchall()
        rented = [i[0] for i in rented]
        while True:
            CAR_ID = input("Enter your CAR_ID: ").upper()
            if CAR_ID in caridlist:
                break
            elif CAR_ID in rented:
                print('You cannot delete this car as it is currently rented! Please try again')
            else:
                print("Invalid car ID! Please try again")
        while True:
            a = input("Are you sure you want to delete this car: [Y/N] ").upper()
            if a in ('Y', 'N'):
                pass
            else:
                print("Invalid choice entered, Enter specified value [Y/N]")
                continue
            break
        if a == 'Y':
            sql = "DELETE from cars WHERE car_id = '%s'" % CAR_ID
            mycursor.execute(sql)
            print("Car deleted successfully")
            mycon.commit()
            choice = input("Do you want to delete any more cars? [Y/N] ").upper()
            if choice == "N":
                mycon.close()
                break
            elif choice != 'Y':
                print('Invalid Choice! Your response is taken as a "No"')
                mycon.close()
                break

def change_price():
    '''To change the price of a car'''
    mycon = mysql.connector.connect(host='localhost', database='car_rentals', user='csproject', password='2020')
    mycursor = mycon.cursor(buffered=True)
    while True:
        sql = "select CAR_ID from cars"
        mycursor.execute(sql)
        caridlist = mycursor.fetchall()
        caridlist = [i[0] for i in caridlist]
        while True:
            CAR_ID = input("Enter your CAR_ID: ").upper()
            if CAR_ID in caridlist:
                break
            else:
                print("Invalid car ID! Please try again")
        while True:
            try:
                new_price = float(input('Enter new price: '))
                if new_price <= 0:
                    raise Exception
            except:
                print('Invalid value! Please enter a valid decimal number')
                continue
            break
        sql = 'update cars set cost_pday = %f where car_id = "%s"' % (new_price, CAR_ID)
        mycursor.execute(sql)
        mycon.commit()
        while True:
            choice1 = input("Do you wish to change the price of another car? [Y/N]: ").upper()
            if choice1 in ("Y", "N"):
                break
            else:
                print("Invalid Value Entered! Please enter specified values [Y/N]")
        if choice1 == "N":
            print("Changes made successfully")
            mycon.close()
            break

def change_status():
    '''To change the status of a car from Available to Maintenance and vice versa'''
    mycon = mysql.connector.connect(host='localhost', database='car_rentals', user='csproject', password='2020')
    mycursor = mycon.cursor(buffered=True)
    while True:
        sql = "select CAR_ID from cars"
        mycursor.execute(sql)
        caridlist = mycursor.fetchall()
        caridlist = [i[0] for i in caridlist]
        while True:
            CAR_ID = input("Enter your CAR_ID: ").upper()
            if CAR_ID in caridlist:
                break
            else:
                print("Invalid car ID! Please try again")
