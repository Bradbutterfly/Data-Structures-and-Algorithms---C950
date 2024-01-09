# Name: Brad Butterfly
# ID: 001425632
import csv
import datetime
from WGUPS_Truck import Truck
from WGUPS_HashTable import HashTable
from WGUPS_Package import Package

# Constants
CSV_DIRECTORY = "CSV/"
DISTANCE_FILENAME = "DistanceFile.CSV"
ADDRESS_FILENAME = "AddressFile.CSV"
PACKAGE_FILENAME = "PackageFile.CSV"


# Loads CSV data from a given filename
def load_csv(filename):
    with open(CSV_DIRECTORY + filename) as csvfile:
        data = csv.reader(csvfile)
        return list(data)


# Load CSV data
CSV_Distance = load_csv(DISTANCE_FILENAME)
CSV_Address = load_csv(ADDRESS_FILENAME)
CSV_Package = load_csv(PACKAGE_FILENAME)


# Load package data into a hash table
def load_package_data(filename, package_hash_table):
    data = load_csv(filename)
    for package in data:
        if int(package[0]) == 9:
            package[1] = "300 State St"
            package[2] = "Salt Lake City"
            package[3] = "UT"
            package[4] = "84103"
        p = Package(
            int(package[0]),
            package[1],
            package[2],
            package[3],
            package[4],
            package[5],
            package[6]
        )
        package_hash_table.insert(p.ID, p)


# Returns distance between two locations
def distance_in_between(x_value, y_value):
    distance = CSV_Distance[x_value][y_value]
    return float(distance) if distance else float(CSV_Distance[y_value][x_value])


# Extracts address ID from CSV_Address
def extract_address(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])


# Delivers packages and updates truck and package details
def delivering_packages(truck):
    not_delivered = [package_hash_table.lookup(packageID) for packageID in truck.packages]
    truck.packages.clear()

    while not_delivered:
        next_address = 2000
        next_package = None

        for package in not_delivered:
            distance = distance_in_between(extract_address(truck.address), extract_address(package.address))

            if distance <= next_address:
                next_address, next_package = distance, package

        if truck.last_delivery_time:
            truck.time += datetime.timedelta(seconds=30)

        truck.packages.append(next_package.ID)
        not_delivered.remove(next_package)
        truck.mileage += next_address
        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

        truck.last_delivery_time = truck.time


# Prints the mileage for all trucks
def view_mileage(truck1, truck2, truck3):
    mileage_truck1 = truck1.mileage
    mileage_truck2 = truck2.mileage
    mileage_truck3 = truck3.mileage
    total_mileage = mileage_truck1 + mileage_truck2 + mileage_truck3

    print("\nMileage Details:")
    print(f"Truck 1: {mileage_truck1:.2f} miles")
    print(f"Truck 2: {mileage_truck2:.2f} miles")
    print(f"Truck 3: {mileage_truck3:.2f} miles")
    print(f"Total mileage for all trucks: {total_mileage:.2f} miles\n")
    input("Press any key to return to the main menu...")
    main_menu()


# Offers viewing options for packages
def view_by_time():
    choice = input("\nPlease choose an option:\n"
                   "1: View single package\n"
                   "2: View all packages\n"
                   "Enter your choice: ")

    if choice == '1':
        view_single_package()
    elif choice == '2':
        view_all_packages()
    else:
        print("Invalid choice. Returning to the main menu.")
        main_menu()


# Prints details of a single package at a given time
def view_single_package():
    try:
        user_time = input("Please enter a time to check the status of a package (HH:MM:SS): ")
        h, m, s = user_time.split(":")
        convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        package_id = input("Enter the numeric package ID: ")
        package = package_hash_table.lookup(int(package_id))

        # Check and update address for package 9
        if package.ID == 9 and convert_timedelta >= datetime.timedelta(hours=10, minutes=20):
            package.address = "410 S. State St."
            package.city = "Salt Lake City"
            package.state = "UT"
            package.zipcode = "84111"
        elif package.ID == 9:
            # Reverting to old address for times before the update
            package.address = "300 State St"
            package.city = "Salt Lake City"
            package.state = "UT"
            package.zipcode = "84103"

        package.update_status(convert_timedelta)
        print(str(package))
        main_menu()

    except ValueError:
        print("Entry invalid. Returning to the main menu.")
        main_menu()


# Prints details of all packages at a given time
def view_all_packages():
    try:
        user_time = input("Please enter a time to check the status of all packages (HH:MM:SS): ")
        h, m, s = user_time.split(":")
        convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        for packageID in range(1, 41):  # Assuming there are 40 packages in total
            package = package_hash_table.lookup(packageID)
            if package.ID == 9 and convert_timedelta >= datetime.timedelta(hours=10, minutes=20):
                package.address = "410 S. State St."
                package.city = "Salt Lake City"
                package.state = "UT"
                package.zipcode = "84111"
            elif package.ID == 9:
                # Reverting to old address for times before the update
                package.address = "300 State St"
                package.city = "Salt Lake City"
                package.state = "UT"
                package.zipcode = "84103"

            package.update_status(convert_timedelta)
            print(str(package))
        main_menu()

    except ValueError:
        print("Entry invalid. Returning to the main menu.")
        main_menu()


# Corrects address for package 9 based on current_time
def correct_address_for_package_9(current_time, package):
    if package.ID == 9 and not package.corrected_address and current_time >= datetime.timedelta(hours=10, minutes=20):
        package_8 = package_hash_table.lookup(8)
        package.address = package_8.address if current_time < datetime.timedelta(hours=10,
                                                                                 minutes=20) else "410 S. State St."
        package.city = package_8.city if current_time < datetime.timedelta(hours=10, minutes=20) else "Salt Lake City"
        package.state = package_8.state if current_time < datetime.timedelta(hours=10, minutes=20) else "UT"
        package.zipcode = package_8.zipcode if current_time < datetime.timedelta(hours=10, minutes=20) else "84111"
        package.corrected_address = True


# Exits program with farewell message
def exit_program():
    """Exit the program with a farewell message."""
    print("Thank you for using WGUPS! Goodbye.")
    exit()


# Main menu logic
def main_menu():
    print("Western Governors University Parcel Service (WGUPS)")
    print("Please choose an option:")
    print("1: View mileage")
    print("2: View by time")
    print("3: Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        view_mileage(truck1, truck2, truck3)
    elif choice == "2":
        view_by_time()
    elif choice == "3":
        exit_program()
    else:
        print("Invalid choice. Exiting program.")
        exit()


if __name__ == "__main__":
    # Initialization code
    truck1 = Truck(16, 18, None,  [15, 13, 16, 14, 19, 20, 40, 37, 30, 31, 25, 29, 27], 0.0, "4001 South 700 East",
                   datetime.timedelta(hours=8))
    truck2 = Truck(16, 18, None, [33, 12, 17, 18, 2, 21, 22, 23, 26, 3, 35, 36, 38, 39], 0.0,
                   "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
    truck3 = Truck(16, 18, None, [1, 24   , 6, 7, 8, 10, 11, 4, 32, 28, 9, 5, 34], 0.0, "4001 South 700 East",
                   datetime.timedelta(hours=9, minutes=5))
    package_hash_table = HashTable()
    load_package_data(PACKAGE_FILENAME, package_hash_table)
    delivering_packages(truck1)
    delivering_packages(truck2)
    truck3.depart_time = min(truck1.time, truck2.time)
    delivering_packages(truck3)

    main_menu()
