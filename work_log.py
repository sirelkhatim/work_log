# import packages
import sys
import csv
import re
import datetime

##### Helper functions #####

def print_elements_list(list1):
    """
    Takes a list and prints out it's elements line by line
    Args:
        list1: list to be printed
    """

    if list1 == []  :
        print("No matches were found")
    else:
        print('These are the records found:\n')
        for elem in list1:
            print(elem)

def insert_work_log(date, name, minutes, notes):
    """
    Function to insert the input from the user
    Args:
        date: The date of the task in the format dd/mm/yyyy
        name: Name of the task (string)
        minutes: number of minutes used for the task (int)
        notes: Any extra description or notes on the task (string)
    """

    row = [date, name, minutes, notes]

    with open('work_log.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

def find(index,query):
    """
    Finds relevant records in the task logger csv using an index and a query
    Args:
        index: the index of the row that the query is based on
        query: this is either the date, minutes, ...
    Returns:
        result: these are the records that match the query on the respective index
    """
    result = []
    with open('work_log.csv', encoding='utf8') as infile:
        reader = csv.reader(infile,delimiter=',')
        for row in reader:
            if row!=[]:
                if row[index] == query:
                    result.append(row)
    return result

def find_by_date(date):
    """
    Function to find record by specific date
    Args:
        date: date to search work tasks on
    Returns:
        match: records that match the date in the work log csv
    """
    match = find(0,date)
    return match

        
def find_by_time(minutes):
    """
    """
    match = find(2,minutes)
    return match

def find_by_string(desc):
    """
    """
    match1 = find(1,desc)
    match2 = find(3,desc)
    if match1 is not []:
        return match1
    elif match2 is not []:
        return match2
    return None

def find_by_pattern(pattern):
    """
    Finds 
    """
    with open('work_log.csv', encoding='utf8') as infile:
        results = []
        reader = csv.reader(infile,delimiter=',')
        for row in reader:
            if row!=[]:
                if re.findall(pattern,row[1])!=[]:
                    results.append(row)
                elif re.findall(pattern,row[3]):
                    results.append(row)

        return results

def find_by_date_range(date1,date2):
    """
    Function that finds date according to a range
    """
    date1 = date1.split('/')
    date2 = date2.split('/')
    start_d1 = datetime.datetime(int(date1[2]),int(date1[1]),int(date1[0]))
    end_d2 = datetime.datetime(int(date2[2]),int(date2[1]),int(date2[0]))
    result = []
    with open('work_log.csv', encoding='utf8') as infile:
        reader = csv.reader(infile,delimiter=',')
        for row in reader:
            if row!=[]:
                date_list = row[0].split('/')
                if len(date_list)==3:
                    date = datetime.datetime(int(date_list[2]),int(date_list[1]), int(date_list[0]))
                    if (date >= start_d1) and (date<= end_d2):
                        result.append(row)
                else:
                    continue
    return result

def check_minutes(minutes):
    """
    """

    if minutes.isdigit():
        return True
    return False

def check_date(date):
    """
    Function to do basic checks to verify the validity of the minutes inputted
    Args:
        date: date to check. Format is by default dd/mm/yyyy
    Returns
        True/False: A boolean indicating whether the minutes is inputted correctly

    """

    split_date = date.split('/')
    if len(split_date)!=3:
        return False
    if not split_date[0].isdigit() or not split_date[1].isdigit() or not split_date[2].isdigit():
        return False
    if int(split_date[2])<2000:
        return False
    if int(split_date[0])>31:
        return False
    if int(split_date[1])>=13:
        return False
    return True


def quit_program(command):
    """
    """

    if command == "exit":
        sys.exit()
        


def insert_option():
    """
    """

    date =input('What is the date? [Please enter in the format dd/mm/yyyy] ')
    name = input('What is the name of the task? ')
    minutes = input('How many minutes did you spend on the task? ')
    notes = input('Any further notes to add? ')
    insert_work_log(date,name,minutes, notes)

def search_option():
    """
    """
    search_by = input("Do you want to search by: \n \
                        1) date \n \
                        2) minutes\n \
                        3) string \n \
                        4) pattern\n \
                        5) find by date range\n \
                        Enter '1','2','3', '4', or '5': ")
    while search_by not in ['1','2','3','4','5']:
        search_by = input("Do you want to search by: \n \
                        1) date \n \
                        2) minutes\n \
                        3) string \n \
                        4) pattern\n \
                        5) find by date range\n \
                        Enter '1','2','3', '4', or '5': ")

    if search_by == '1':
        date = input("What is the date that you are search for? ")
        matches = find_by_date(date)
        print_elements_list(matches)
    if search_by == '2':
        minutes = input("What is number of minutes that you want to search for? ")
        matches = find_by_time(minutes)
        print_elements_list(matches)
    if search_by == '3':
        query = input("What is string that you want to search for? ")
        matches = find_by_string(query)
        print_elements_list(matches)

    if search_by =='4':
        query = input("Please insert the regex pattern that you want to use to search with? ")
        matches = find_by_pattern(query)
        print_elements_list(matches)
    
    if search_by == '5':
        date1, date2 = input("Please insert the start and end dates that you want to search between? [make sure the dates are followed by a space]  ").split()
        matches = find_by_date_range(date1,date2)
        print_elements_list(matches)

def intro_work_log():
    """
    """
    # Get input from user
    option = input(" \
    What would you like to do? \n \
    a) Add new entry \n \
    b) Search in existing entries \n \
    c) Quit Program\n\
    Enter 'a', 'b', or 'c': ")

    option = option.lower()
    while option not in ["a","b","c"]:
        option = input("\
        Please enter a valid option \
        Work LOG \n \
        What would you like to do? \n \
        a) Add new entry \n \
        b) Search in existing entries \n \
        c) Quit Program\n \
        Enter 'a', 'b', or 'c': ")

    if option == 'a':
        insert_option()
    if option == 'b':
        search_option()
    if option =='c':
        quit_program('exit')




# Weclome the user
print('####################################################################')
print('################ Welcome to your personal work log #################')
print('####################################################################')
while True:  
    intro_work_log()
    return_menu= input("Do you want to return to the main menu or exit? Press 'exit' to exit and press 'return' to return to the main menu: ")
    while return_menu not in ['exit','return']:
        return_menu= input("You have entered a wrong command: Do you want to return to the main menu or exit? \
         Press 'exit' to exit and press 'return' to return to the main menu: ")
    if return_menu == 'exit':
        quit_program('exit')
    elif return_menu == 'return':
        intro_work_log()