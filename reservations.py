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
