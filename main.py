import mysql.connector
from tabulate import tabulate
from mysql.connector import FieldType

connected = False

print("\nWelcome Sir/Ma'am \nWith the help of this program we can Add/Delete/Update/View the Records of Issued Books in a Library using  SQL Database with MYSQL-Python Connectivity.")
print("\nThis  Program  is  Made by: \n1) Yajur Chatnani DPS GWALIOR XII-A(2023-24)  \n2) Nikush Sharma  DPS GWALIOR XII-A(2023-24)")
input("\nPress ENTER to Start: ")

def connect(connected):
            while not connected:
                print("\nGlad that you're here! Some Simple Steps before we proceed"  if  'host_name' not in locals() else  "\n  There might be a Typo, USERNAME and PASSWORD are case sensitive")
                host_name = input("Enter HOST for mysql (Generally \"localhost\"): ")
                user_name = input("Enter USERNAME for mysql (Generally \"root\"): ")
                password = input("Enter PASSWORD for mysql: (Should not be General):")


                try:
                    mydb = mysql.connector.connect(host=host_name,user=user_name,passwd=password)
                    cursor = mydb.cursor()
                    
                    print("\nConnection Succesfull !")
                    connected = True
                    
                except:print("\n----------------------------------\nThere was an error connecting, let's retry")
                
                if  connected ==  True:
                    cursor.execute("CREATE DATABASE IF NOT EXISTS LIBRARY;")
                    cursor.execute("USE LIBRARY;")
                    cursor.execute('''CREATE TABLE IF NOT EXISTS BOOKS_ISSUED(
                                ISSUE_ID INT PRIMARY KEY,
                                BOOK_NAME VARCHAR(200),
                                ISSUED_TO VARCHAR(50),
                                ISSUED_AT DATE,
                                ISSUED_TILL DATE
                    )''')
                    main_menu(cursor)
                else:pass

def add_record(cursor):
    #GETTING DATA FROM USER
    issue_id = int(input("\nEnter ISSUE ID(Unique Integer) :"))
    book_name = input("Enter Book Name: ")
    issued_to = input("The Book is issued to (Name): ")
    issued_at = input("Date of issuing (YYYY-MM-DD): ")
    issued_till = input("Issued till (YYYY-MM-DD): ")

    #ADDING RECORD TO TABLE
    try:
        cursor.execute("INSERT INTO BOOKS_ISSUED VALUES({},'{}','{}','{}','{}')".format(issue_id,book_name,issued_to,issued_at,issued_till))
        cursor.execute("COMMIT;")
        print("\nVOILA! record added")

    #HANDLING ERRORS
    except:
        print("\nOOPS! There was an error adding record")

    #DISPLAYING TABLE 
    finally:
        display_record(cursor)

def display_record(cursor):
    #GETTING DATA FROM SERVER
    cursor.execute("SELECT * FROM BOOKS_ISSUED;")
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()

    table_name = "BOOKS_ISSUED"
    print("\nTable {}:".format(table_name))
    
    #PRINTING TABLE
    print(tabulate(data, headers = columns, tablefmt="psql"))
    input("\n Press ENTER to show Main Menu:")
    main_menu(cursor)

def delete_record(cursor):

    #PRINTING TABLE
    cursor.execute("SELECT * FROM BOOKS_ISSUED;")
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    table_name = "BOOKS_ISSUED"
    print("\nTable {}:".format(table_name))
    print(tabulate(data, headers = columns, tablefmt="psql"))

    #DELETING RECORD
    try:
        delete_book_record = int(input("Enter ISSUE ID to be deleted:"))
        record_exist = False

        #CHECKING IF THE BOOK RECORD TO BE DELETED IS IN THE TABLE
        for rows in data:
            for records in rows:
                if rows[0] == delete_book_record:
                    record_exist = True
                else:
                    pass
        
        #CONFIRMATION & DELETION 
        if record_exist:
            cursor.execute("DELETE FROM BOOKS_ISSUED WHERE ISSUE_ID = {};".format(delete_book_record))

            confirm = input("\nConfirm deleting (y/n): ")

            if confirm.lower() == "y":
                cursor.execute("COMMIT;")
                print("\nVOILA! record deleted")

            else:
                cursor.execute("ROLLBACK;")
                print("\nDeletion Cancelled")

        #IF RECORD TO BE DELTED DOES NOT EXISTS IN THE TABLE
        else:
            print("\nRecord does not exists")
    
    #HANDLING ERRORS
    except:
        print("\nOOPS! there was an error deleting the record")
    finally:
        display_record(cursor)

def update_record(cursor):
    #PRINTING TABLE
    cursor.execute("SELECT * FROM BOOKS_ISSUED;")
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    table_name = "BOOKS_ISSUED"
    print("\nTable {}:".format(table_name))
    print(tabulate(data, headers = columns, tablefmt="psql"))

    #UPDATING RECORD
    try:
        update_book_record = int(input("Enter ISSUE ID to be updated:"))
        record_exist = False

        #CHECKING IF THE BOOK RECORD TO BE updated IS IN THE TABLE
        for rows in data:
            for records in rows:
                if rows[0] == update_book_record:
                    record_exist = True
                else:
                    pass
        
        #GETTING NEW DATA OF THE RECORD
        if record_exist:
            print("\nEnter NEW DATA")
            book_name = input("Enter Book Name: ")
            issued_to = input("The Book is issued to (Name): ")
            issued_at = input("Date of issuing (YYYY-MM-DD): ")
            issued_till = input("Issued till (YYYY-MM-DD): ")
            
            #RECORD UPDATION
            cursor.execute('''UPDATE BOOKS_ISSUED 
                               SET BOOK_NAME = '{}',ISSUED_TO = '{}',ISSUED_AT = '{}',ISSUED_TILL = '{}'
                               WHERE ISSUE_ID = {};'''.format(book_name,issued_to,issued_at,issued_till,update_book_record))
            
            #CONFIRM UPDATION
            confirm = input("\nConfirm updation (y/n): ")

            if confirm.lower() == "y":
                cursor.execute("COMMIT;")
                print("\nVOILA! record UPDATED")

            else:
                cursor.execute("ROLLBACK;")
                print("\nUpdation Cancelled")

        #IF RECORD TO BE DELTED DOES NOT EXISTS IN THE TABLE
        else:
            print("\nRecord does not exists")
    
    #HANDLING ERRORS
    except:
        print("\nOOPS! there was an error deleting the record")
    finally:
        display_record(cursor)

def main_menu(cursor):
    ask_operation = input("\nMAIN MENU\n TYPE 1 to Add Book record \n TYPE 2 to Display Book records\n TYPE 3 to Delete Book record\n TYPE 4 to Update Book record\n TYPE anything else to exit\nYour Input:  ")


    if ask_operation == "1":
        add_record(cursor)

        
    elif ask_operation == "2":
        display_record(cursor)
        
    elif ask_operation == "3":
        delete_record(cursor)
    
    elif ask_operation  == "4":
        update_record(cursor)

    else:
        print("Exiting...")
        cursor.close()
        exit()


connect(connected)
