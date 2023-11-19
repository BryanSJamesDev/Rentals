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

    if ask_existing == 'N':
        c_id = customer_related_functions.ADD()
    else:
        sql = 'SELECT c_id, status from customer'
        mycursor.execute(sql)
        data = mycursor.fetchall()
        data1 = []
        data2 = []

        for i, j in data:
            if j == 'I':
                data1.append(i)
            else:
                data2.append(i)

        while True:
            c_id = input('Enter your customer ID: ').upper()
            if c_id in data2:
                print('Please close existing reservation before creating a new one')
                return
            elif c_id not in data1:
                print("Customer ID '%s' does not exist!" % c_id)
                continue
            break

        sql = 'Select company, model, year, car_id from cars where status = "a"'
        mycursor.execute(sql)
        data = mycursor.fetchall()

        if mycursor.rowcount == 0:
            print('No cars available')
            return

        main_dict = {}
        # data - [(company, model, year, car_id), (), ()]

        for i, j, k, l in data:
            if i in main_dict:
                if j in main_dict[i]:
                    if k in main_dict[i][j]:
                        main_dict[i][j][k].append(l)
                    else:
                        main_dict[i][j][k] = []
                        main_dict[i][j][k].append(l)
                else:
                    main_dict[i][j] = {}
                    main_dict[i][j][k] = []
                    main_dict[i][j][k].append(l)

            else:
                main_dict[i] = {}
                main_dict[i][j] = {}
                main_dict[i][j][k] = []
                main_dict[i][j][k].append(l)

        # main_dict = {Company:{Model:{Year:[car_id's],Year:[car_id's]}}}

        while True:
            while True:
                company_choice = input('Enter your company choice: %s ' % list(main_dict.keys())).upper()
                if company_choice not in main_dict:
                    print('Sorry, the company name does not exist, Enter another company')
                else:
                    break

            while True:
                model_choice = input('Enter the model of your choice: %s ' % list(main_dict[company_choice].keys())).upper()
                if model_choice not in main_dict[company_choice]:
                    print('Sorry, the model name does not exist, Enter another model')
                else:
                    break

            while True:
                year_choice = input("Enter your choice of year: %s " % list(main_dict[company_choice][model_choice].keys()))
                if not year_choice.isdigit():
                    print("You have not entered a digit")
                    continue
                year_choice = int(year_choice)
                if year_choice not in main_dict[company_choice][model_choice]:
                    print("Sorry, the year does not exist")
                else:
                    break

            print("\nThese are the specifications of your chosen car:\n")

            sql = "select * from cars where company = '%s' and model = '%s' and year = %d and status = 'a' order by rand()" % (company_choice, model_choice, year_choice)
            mycursor.execute(sql)
            car = mycursor.fetchall()[0]

            header = ['CAR_ID', 'COMPANY', 'MODEL', 'YEAR', 'ENGINE', 'REAR AC', 'NO OF SEATS', 'INFOTAINMENT SYSTEM', 'COST PER DAY', 'STATUS']
            engine = {'E': 'Electric', 'P': 'Petrol', 'D': 'Diesel'}
            status = {'A': 'Available', 'R': 'Rented', 'M': 'Maintenance'}
            choice = {'Y': 'Available', 'N': 'Not available'}

            for i in range(len(header)):
                if i in (0, 1, 2):
                    print('{:^21s}:{:^25s}'.format(header[i], car[i]))
                elif i in (3, 6):
                    print('{:^21s}:{:^25d}'.format(header[i], car[i]))
                elif i == 4:
                    print('{:^21s}:{:^25s}'.format(header[i], engine[car[4]))
                elif i in (5, 7):
                    print('{:^21s}:{:^25s}'.format(header[i], choice[car[i]))
                elif i == 8:
                    print('{:^21s}:{:^25.3f}'.format(header[i], car[8]))
                else:
                    print('{:^21s}:{:^25s}'.format(header[i], status[car[9]))

            while True:
                F = input("Do you wish to continue with this car? [y/n] ").upper()
                if F not in ['Y', 'N']:
                    print("Invalid choice entered")
                else:
                    break
                if F == 'Y':
                    break

            while True:
                days = input("How long (in days) do you want to keep the car? ")
                if days.isdigit():
                    days = int(days)
                    if days == 0:
                        print('Number should be greater than 0')
                        continue
                    break
                else:
                    print("Invalid data entered")

            total = days * car[8]

            sql = "select reservation_count from customer where c_id = '%s'" % c_id
            mycursor.execute(sql)
            discount_yn = mycursor.fetchone()[0]

            if discount_yn > 0:
                discount = (discount_yn * days) / 10
                print("You have received a discount of", discount, '%')
                total -= (discount * total) / 100

            print('Total Amount: KD', total)

            sql = "update cars set status = 'R' where car_id = '%s'" % car[0]
            mycursor.execute(sql)

            sql = "update customer set status = 'A' where c_id = '%s'" % c_id
            mycursor.execute(sql)

            sql = "select * from reservations"
            mycursor.execute(sql)
            mycursor.fetchall()
            R_id = mycursor.rowcount
            R_id = 'R' + str(R_id + 1)

            R_date = date.today()
            C_date = R_date + timedelta(days)
            R_date = R_date.strftime('%Y-%m-%d')
            C_date = C_date.strftime('%Y-%m-%d')

            sql = "insert into reservations values ('%s','%s','%s','%s','%s',%d,%f)" % (R_id, car[0], c_id, R_date, C_date, days, total)

            mycursor.execute(sql)
            mycon.commit()
            mycon.close()

            print('Reservation Completed Successfully, Your Reservation ID is', R_id)
