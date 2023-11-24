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
