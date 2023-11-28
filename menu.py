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

    elif choice == '1':
            while True:
                print('\n1. ADD A CAR')
                print('2. VIEW ONE')
                print('3. VIEW ALL')
                print('4. CHANGE CAR STATUS')
                print('5. CHANGE CAR PRICE')
                print('6. DELETE A CAR')
                print('7. BACK')
    
                while True:
                    choice1 = input('Enter your choice: ')
                    if not choice1.isdigit() or len(choice1) > 1 or choice1 not in '1234567':
                        print('Invalid Choice, Please try again')
                    else:
                        break
    
                if choice1 == '3':
                    car_related_functions.viewall()
                elif choice1 == '1':
                    car_related_functions.add_car()
                elif choice1 == '4':
                    car_related_functions.change_status()
                elif choice1 == '5':
                    car_related_functions.change_price()
                elif choice1 == '6':
                    car_related_functions.DEL_CAR()
                elif choice1 == '7':
                    break
                else:
                    car_related_functions.viewone()
        else:
            print('\nPROGRAM END')
            break
    
    print('Thank you for using this program, Have a great day!')
