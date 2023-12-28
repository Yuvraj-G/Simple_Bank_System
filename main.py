import mysql.connector as a
import details as d
import time

def main():
    print()
    def load(sec):
        print()
        for a in range(10):
            print(".",end="",flush=True)
            time.sleep(sec/10)
        print()
        print()


    cnx = a.connect(user = d.user, host = d.host, password = d.password, database = d.database)
    

    print("Welcome To The Modern Banking System!")
    print("Please choose an option:\n1)New User\n2)Existing User\n3)Exit")
    print()
    entry = input("1/2/3 --> ")
    
    def check(id):
        load(1)
        crsr = cnx.cursor()
        query = "SELECT * FROM personal WHERE Aadhar_No = %s"
        crsr.execute(query,(id,))
        a = crsr.fetchall()
        # print(a)
        if a != []:
            return True
        else:
            return False

    def new():
        load(1)
        crsr = cnx.cursor()
        try:
            id = input("Enter your aadhar number --> ")

            if len(id) != 12: #Raising error if aadhar number is not 12 digits long
                print("Aadhar Number should be 12 digits long!")
                raise ValueError
            
            if check(int(id)): #Checking If User exists, using int() so that user doesn't enter alphanumeric value
                print("You already have an account associated with this aadhar number.")
                print("Returning to main menu")
                load(1)
            else:   #Registering New User
                
                #Taking inputs
                name = input("Enter your full name --> ")
                age = int(input("Enter your age --> "))
                if age < 18 or age >= 100:
                    print("Age should be between 18 and 100 to open account.")
                    raise ValueError
                gender = input("Enter your gender (M/F/O) --> ")
                if len(gender) > 1 :
                    print("Please choose one of the valid options for gender.")
                    raise ValueError
                query = "INSERT INTO personal VALUES(%s,%s,%s,%s)"

                

                # Creating account and adding account details

                acc = 10000000001
                crsr.execute("SELECT * FROM accounts ORDER BY Account_No")
                a = crsr.fetchall()
                if a != []:
                    acc = a[-1][1] + 1

                type = int(input("Enter account type:\n1) Savings\n2) Current\n\n(1 or 2)--> "))

                if type == 1:
                    type = "Savings"
                elif type == 2:
                    type = "Current"
                else:
                    print("You didn't choose one of the given options!")
                    raise ValueError
                
                balance = int(input("Enter amount to be deposited (Minimum : 5000) --> "))
                if balance < 5000 :
                    print("Starting balance should be more than 5000!")
                    raise ValueError
                
                pin = int(input("Set a 4 digit PIN --> "))
                
                
                if pin < 1000 or pin > 9999 :
                    print("PIN Must be of 4 digits only!")
                    raise ValueError

                conf = int(input("Confirm your 4 digit PIN --> "))
                if conf != pin :
                    print("Both PINs didn't match!")
                    raise ValueError

                q = "INSERT INTO accounts VALUES(%s,%s,%s,%s,%s)"     

                crsr.execute(query,(id,name,age,gender)) # Personal Details Added
                crsr.execute(q,(id,acc,type,balance,pin)) # Account created

                a = time.localtime()
                date = time.strftime("%Y-%m-%d" , a )

                qu = "INSERT INTO transactions VALUES(%s,%s,%s,%s)"
                crsr.execute(qu,(date,acc,"Deposit",balance))

                cnx.commit()
                print("User registered and account opened succesfully!")


        except ValueError:
            print("Invalid Value Entered!")
            main()
        
        finally:
            
            cnx.close()
            
            print()

            que = input("Do you want to return to main menu? (Y/N) --> ")
            if que.upper() == "Y":
                load(1)
                main()
            elif que.upper() == "N":
                print("\nThank You")
                time.sleep(1)
                print("\nExiting....")
                time.sleep(5)
            else:
                print("\nThank You")
                time.sleep(1)
                print("\nExiting....")
                time.sleep(5)

    
    


    def logged(rec):
        load(1)
        print()
        print("What would you like to do?")
        print("1)Balance Enquiry\n2)Deposit Money\n3)Withdraw Money\n4)Terminate my account\n5)See transaction history\n6)Back to main menu")
        print()
        opt = int(input("Please type an option (1/2/3/4/5/6) --> "))
        print()

        def delete(rec):
            load(1)
            crsr = cnx.cursor()
            print("Are you sure you want to terminate your account?")
            print("This action cannot be undone.")
            a = int(input("1) Yes or 2) No (1/2) --> "))
            
            if a == 1:
                print(f"Your remaining balance ({rec[0][3]}) will be withdrawn after you enter your PIN")
                pin = int(input("Enter your 4 digit PIN --> "))
                if rec[0][4] == pin:
                    print("Terminating Account!")
                    crsr.execute("DELETE FROM personal WHERE Aadhar_No = %s",(rec[0][0],))
                    crsr.execute("DELETE FROM accounts WHERE Aadhar_No = %s",(rec[0][0],))
                    crsr.execute("DELETE FROM transactions WHERE Account_No = %s",(rec[0][1],))


                else:
                    print("Invalid PIN entered.")
                    print("Returning to previous menu.")
                    logged()


            elif a == 2:
                print("Returning to previous menu.")
                logged()
            else:
                raise ValueError
                
        def deposit(rec):
            load(1)
            crsr = cnx.cursor()
            amount = int(input("Enter amount to be deposited --> "))
            a = time.localtime()
            date = time.strftime("%Y-%m-%d" , a )

            
            crsr.execute("UPDATE accounts SET Balance = Balance + %s WHERE Account_No = %s",(amount,rec[0][1]))
            q = "INSERT INTO transactions VALUES(%s,%s,%s,%s)"
            crsr.execute(q,(date,rec[0][1],"Deposit",amount))
            print("Amount succesfully deposited")

        def withdraw(rec):
            load(1)
            crsr = cnx.cursor()
            amount = int(input("Enter amount to be withdrawed --> "))

            pin = int(input("Confirm your 4 digit PIN --> "))
            if rec[0][4] == pin:
                if amount > rec[0][3]:
                    print("Insufficient Balance")
                    print("Returning to previous menu")
                    logged(rec)
                
                a = time.localtime()
                date = time.strftime("%Y-%m-%d" , a )

                
                crsr.execute("UPDATE accounts SET Balance = Balance - %s WHERE Account_No = %s",(amount,rec[0][1]))
                q = "INSERT INTO transactions VALUES(%s,%s,%s,%s)"
                crsr.execute(q,(date,rec[0][1],"Withdraw",amount))
                print("Amount succesfully withdrawed")
                
            else:
                print("Incorrect PIN entered.")
                print("Returning to main menu")
                main()
        
        def transaction(rec):
            load(1)
            crsr = cnx.cursor()
            pin = int(input("Confirm your 4 digit PIN --> "))
            if rec[0][4] == pin:
                query = "SELECT * FROM transactions WHERE Account_No = %s ORDER BY Date DESC"
                crsr.execute(query,(rec[0][1],))
                row = crsr.fetchone()
                if row is None:
                    print(f"No transactions done. Remaining Balance --> {rec[0][3]}")
                else:
                    print(f"Remaining Balance --> {rec[0][3]}")

                    while row is not None:
                        if row[2] == "Withdraw":
                            print(f"{crsr.rowcount}\t{row[0]}\t{row[2]}\t-{row[3]}\t")
                        else:
                            print(f"{crsr.rowcount}\t{row[0]}\t{row[2]} \t+{row[3]}\t")
                        row = crsr.fetchone()
            else:
                print("Incorrect PIN entered.")
                print("Returning to main menu")
                main()

        def display(rec):
            load(1)
            crsr = cnx.cursor()
            query = "SELECT P.Aadhar_No, Name, Account_No, Account_Type, Balance FROM personal P, accounts A WHERE P.Aadhar_No = A.Aadhar_No AND P.Aadhar_No = %s"
            crsr.execute(query,(rec[0][0],))
            r = crsr.fetchone()
            print("Aadhar_No\tName\t\tAccount_No\tAccount_Type\tBalance")
            print()
            print(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]} \t{r[4]}")
            print()

        if opt == 1:
            # print(f"Account Number - {rec[0][1]}\nRemaining Balance - {rec[0][3]}")
            display(rec)
        elif opt == 2:
            deposit(rec)
        elif opt == 3:
            withdraw(rec)
        elif opt == 4:
            delete(rec)
        elif opt == 5:
            transaction(rec)
        elif opt == 6:
            main()

    def exist():
        load(1)
        crsr = cnx.cursor()
        try:
            id = input("Enter your aadhar number --> ")

            if len(id) != 12: #Raising error if aadhar number is not 12 digits long
                print("Aadhar Number should be 12 digits long!")
                raise ValueError
            
            if not check(int(id)): #Checking If User exists, using int() so that user doesn't enter alphanumeric value
                print("You don't have an account associated with this aadhar number.")
                print("Returning to main menu")
                load(1)
            
            else:   #Logging in
                query = "SELECT * FROM accounts WHERE Aadhar_No = %s"
                crsr.execute(query,(id,))
                rec = crsr.fetchall()
                print(f"Starting login process for Account No - {rec[0][1]}")

                pin = int(input("Enter your 4 digit PIN --> "))
                if rec[0][4] == pin:
                    print("User logged in succesfully!")
                    logged(rec)
                else:
                    print("Incorrect PIN entered.")
                    return

                
        except ValueError:
            print("Invalid Value Entered!")
            main()
        finally:
            cnx.commit()
            cnx.close()

            
            print()

            que = input("Do you want to return to main menu? (Y/N) --> ")
            if que.upper() == "Y":
                load(1)
                main()
            elif que.upper() == "N":
                print("\nThank You")
                time.sleep(1)
                print("\nExiting....")
                time.sleep(5)
            else:
                print("\nThank You")
                time.sleep(1)
                print("\nExiting....")
                time.sleep(5)

    if entry == "1" :
        new()
    elif entry == "2" :
        exist()
    elif entry == "3":
        print("\nThank you for visiting!")
        time.sleep(1)
        print("\nExiting....")
        time.sleep(2)
        quit()
    else:
        print("Invalid Value Entered!")
    
    

main()
