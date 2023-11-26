import customer_related_functions, reservation_related_functions, car_related_functions

print('Welcome to Tess Rentals')
print('\nTo exit the program at any point, hit CTRL + C')

while True:
    print('\nMENU')
    print('1. CARS')
    print('2. CUSTOMERS')
    print('3. RESERVATIONS')
    print('4. EXIT')

    while True:
        choice = input('Enter your choice: ')
        if not choice.isdigit() or len(choice) > 1 or choice not in '1234':
            print('Invalid Choice, Please try again')
        else:
            break

    if choice == '3':
        while True:
            print('\n1. CREATE NEW RESERVATION')
            print('2. VIEW ALL RESERVATIONS')
            print('3. CLOSE EXISTING RESERVATION')
            print('4. BACK')

            while True:
                choice1 = input('Enter your choice: ')
                if not choice1.isdigit() or len(choice1) > 1 or choice1 not in '1234':
                    print('Invalid Choice, Please try again')
                else:
                    break

            if choice1 == '2':
                reservation_related_functions.viewall()
            elif choice1 == '1':
                reservation_related_functions.new_reservation()
            elif choice1 == '3':
                reservation_related_functions.close_reservation()
            else:
                break

    elif choice == '2':
        while True:
            print('\n1. ADD NEW CUSTOMER')
            print('2. VIEW ONE CUSTOMER')
            print('3. VIEW ALL CUSTOMERS')
            print('4. UPDATE CUSTOMER DETAILS')
            print('5. BACK')

            while True:
                choice1 = input('Enter your choice: ')
                if not choice1.isdigit() or len(choice1) > 1 or choice1 not in '12345':
                    print('Invalid Choice, Please try again')
                else:
                    break

            if choice1 == '3':
                customer_related_functions.VIEWALL()
            elif choice1 == '1':
                customer_related_functions.ADD()
            elif choice1 == '4':
                customer_related_functions.UPDATE()
            elif choice1 == '5':
                break
            else:
                customer_related_functions.VIEWONE()
