# Basem Alqusaimi
# Student number: 010840925

import csv
import datetime

# W-1_ChainingHashTable_zyBooks_Key-Value.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
# hashtable with chaining
class HashTable:
    def __init__(self, size=10):
        self.main_table = []
        for i in range(size):
            self.main_table.append([])

    # B3: O(1)
    # insert method
    def insert(self, key, value):
        bucket = self.main_table[hash(key) % len(self.main_table)]
        bucket.append([key, value])

    # B3: O(1)
    # search method
    def search(self, key):
        bucket = self.main_table[hash(key) % len(self.main_table)]

        for i in bucket:
            if i[0] == key:
                return i[1]


# B3: O(1)
# package class
class Package:
    def __init__(self, package_id_number, delivery_address, delivery_city, delivery_zip_code, delivery_deadline, package_weight):
        self.package_id_number = package_id_number
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_zip_code = delivery_zip_code
        self.delivery_deadline = delivery_deadline
        self.package_weight = package_weight
        self.delivery_status = ""
        self.time_left_hub = None
        self.time_delivered = None

    def __str__(self):
        return "package ID number:{}, delivery address:{}, delivery city:{}, delivery zip code:{}," \
               "  delivery deadline:{}, " \
               "package weight:{}, delivery status:{}".format(self.package_id_number, self.delivery_address,
                                                              self.delivery_city, self.delivery_zip_code,
                                                              self.delivery_deadline,
                                                              self.package_weight, self.delivery_status)

    def __eq__(self, other):
        if isinstance(other, Package):
            return self.package_id_number == other.package_id_number
        return False


class Truck:
    def __init__(self, current_location, time_left_hub):
        self.current_location = current_location
        self.packages = []
        self.time_left_hub = time_left_hub
        self.mileage = 0

# B3: O(n)
# method to load the packages from the csv file to the hash table
# Ref: W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
def loadPackageData(hashtable):
    with open('packageCSV.csv', encoding='utf-8-sig') as package_CSV:
        package_data = csv.reader(package_CSV)
        for row in package_data:
            id = int(row[0])
            delivery_address = row[1]
            delivery_city = row[2]
            delivery_deadline = row[5]
            delivery_zip_code = row[4]
            package_weight = row[6]

            my_package = Package(id, delivery_address, delivery_city, delivery_zip_code, delivery_deadline, package_weight)

            hashtable.insert(id, my_package)


# B3: O(n)
# method to read distance data
def loadDistanceData():
    distanceData = []
    with open("distanceCSV.csv", encoding='utf-8-sig') as distance_CSV:
        distance_data = csv.reader(distance_CSV)
        for row in  distance_data:
            distanceData.append(row)

    return distanceData


# B3: O(n)
# method to read address data
def loadAddressData():
    addressData = []
    with open("addressCSV.csv", encoding='utf-8-sig') as address_CSV:
        address_data = csv.reader(address_CSV)
        for row in address_data:
            addressData.append(row[2])

    return addressData


# B3: O(n^2)
# returns the distance between two address switches the address if the distance is blank
def distanceBetween(address1, address2):
    distanceData = loadDistanceData()
    #print(distanceData)
    addressData = loadAddressData()
    #print(addressData)
    first_address = addressData.index(address1)
    second_address = addressData.index(address2)

    if distanceData[first_address][second_address] == "":
        return distanceData[second_address][first_address]
    else:
        return distanceData[first_address][second_address]

'''def minDistanceFromTruck(truck):
    closest_package = None
    closest_distance = float("inf")

    for package in truck.packages:
        #print(package)
        package_distance = float(distanceBetween(truck.current_location, package.delivery_address))
        if package_distance < closest_distance:
            closest_package = package
            closest_distance = package_distance

    return closest_package'''


# B3: O(n)
# loads a truck based of given package list
def loadPackages(truck, package_list):
    for package_id in package_list:
        #print(package_id)
        package = package_hashtable.search(package_id)
        #print(package)
        package.time_left_hub = truck.time_left_hub
        truck.packages.append(package)


# B3: O(n^2)
# implementation of a nearest neighbor algorithm where the next closest package gets delivered first
# ref: https://www.geeksforgeeks.org/k-nearest-neighbor-algorithm-in-python/#
def truckDeliverPackages(truck):
    # Get the current time, current location, and packages to deliver
    current_time = truck.time_left_hub
    current_location = truck.current_location
    packages_to_deliver = truck.packages.copy()

    # Deliver the packages until all of them have been delivered
    while packages_to_deliver:
        # Find the closest package to the current location
        closest_package = None
        closest_distance = float("inf")

        for package in packages_to_deliver:
            miles_to_package = float(distanceBetween(current_location, package.delivery_address))
            if miles_to_package < closest_distance:
                closest_distance = miles_to_package
                closest_package = package
        # Deliver the closest package
        mileage = float(closest_distance)
        # print("miles_to_package", miles_to_package)
        time_to_package = datetime.timedelta(minutes=mileage / 0.3)
        # print("time_to_package", time_to_package)
        current_time += time_to_package
        # print("current_time", current_time)
        truck.mileage += mileage
        # print("truck.mileage", truck.mileage)

        # closest_package.delivery_status = "DELIVERED at {}".format(current_time)
        closest_package.time_delivered = current_time
        # print(current_time)

        current_location = closest_package.delivery_address
        packages_to_deliver.remove(closest_package)

    # Set the truck's packages to an empty list to indicate that they have all been delivered
    truck.packages = []


# B3: O(1)
# update package status based on time
def update_package(package, time):
    if package.time_delivered < time:
        package.delivery_status = "DELIVERED at {}".format(package.time_delivered)
    elif package.time_left_hub > time:
        package.delivery_status = "ON TRUCK"
    else:
        package.delivery_status = "AT HUB"


def print_menu():
    print("Western Governors University Parcel Service package tracker\n")


def print_all_package():
    time_in = input("Enter the time in format HH:MM: ")
    t = datetime.datetime.strptime(time_in, '%H:%M')
    status_time = datetime.timedelta(hours=t.hour, minutes=t.minute)
    total_mileage = 0

    for package_id in range(1, 41):
        package = package_hashtable.search(package_id)
        update_package(package, status_time)
        print(str(package))

    for truck in [truck1, truck2, truck3]:
        total_mileage += truck.mileage
    print("\nTotal Mileage {}".format(total_mileage))


'''def print_single_package(package_id):
    time_in = input("Enter the time in format HH:MM: ")
    status_time = datetime.datetime.strptime(time_in, '%H:%M')
    package = package_hashtable.search(package_id)
    update_package(package, status_time)
    print(package)'''


package_hashtable = HashTable()
loadPackageData(package_hashtable)


truck1_package_list = [15, 13, 14, 16, 19, 20, 1, 29, 30, 31, 34, 37, 40]
truck2_package_list = [3, 18, 36, 38, 6, 25, 28, 32, 33, 35, 39]
truck3_package_list = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27]

truck1 = Truck("4001 South 700 East", datetime.timedelta(hours=8, minutes=0))
truck2 = Truck("4001 South 700 East", datetime.timedelta(hours=9, minutes=5))
truck3 = Truck("4001 South 700 East", datetime.timedelta(hours=12, minutes=0))

loadPackages(truck1, truck1_package_list)
loadPackages(truck2, truck2_package_list)
loadPackages(truck3, truck3_package_list)

truckDeliverPackages(truck1)
truckDeliverPackages(truck2)
truckDeliverPackages(truck3)



print_menu()
print_all_package()

# B3: O(n^2)

