#!/usr/bin/env python
# coding: utf-8

# In[70]:


import mysql.connector as mc
import random as rd
con=mc.connect(host='127.0.0.1',user='root',password='1234')
cur=con.cursor()
cur.execute('Create Database if not exists ATM')
cur.execute('use atm')
cur.execute('create table if not exists CustomerRecord(AccNo int primary key auto_increment,Name text,Branch text,PIN int)')
cur.execute('create table if not exists TransactionRecord(AccNo int primary key,foreign key(AccNo) references CustomerRecord(AccNo),Name text,Amount decimal(7,2))')

def reg(name,branch,pin):
    query="Insert into CustomerRecord(Name,Branch,PIN) values(%s,%s,%s)"
    val=(name,branch,pin)
    cur.execute(query,val)
    con.commit()
    query='Select accno from customerRecord where name=%s and branch=%s and pin=%s'
    val=(name,branch,pin)
    cur.execute(query,val)
    accno=str(cur.fetchone()).strip("'(,)'")
    query='create table '+name+'(SNo int primary key auto_increment,Description text,Amount Decimal(7,2))'
    cur.execute(query)
    print('\n___________Registered Successfully___________')
    print(f'Acc.No:  {accno}')
    print(f'Name:    {name}')
    print(f'Branch:  {branch}')
    print(f'Pin:     {pin}\n')
        
def deposit(accno,amount):
    query='Select Name from CustomerRecord where AccNo=%s and Name not like %s'
    val=(accno,"")
    cur.execute(query,val)
    name=cur.fetchall()[0]
    query='Select Amount from TransactionRecord where AccNo=%s and Name not like %s'
    val=(accno,"")
    cur.execute(query,val)
    try:
        dep=amount
        prev_amount=cur.fetchone()
        prev_amount=str(prev_amount).strip("'(Decimal''),'")
        amount=amount+float(prev_amount)
    except:
        pass
    name=str(name)
    name=name.strip("('',)")
    try:
        query='Insert into TransactionRecord(AccNo,Name,Amount) values(%s,%s,%s)'
        val=(accno,name,amount)
        cur.execute(query,val)
    except:
        query='Update TransactionRecord set Amount=%s where accno=%s'
        val=(amount,accno)
        cur.execute(query,val)
    query='Insert into '+name+'(Description,Amount) values(%s,%s)'
    val=('Credit',amount)
    cur.execute(query,val)
    print(f"The amount {dep} has been deposited in the account {accno} successfully!")
    
def check_bal(accno):
    query='Select * from transactionrecord where accno=%s and name not like %s'
    val=(accno,'')
    cur.execute(query,val)
    details=cur.fetchall()
    name=str(details).strip("''('')''").split(',')[1]
    balance=str(details).strip("Decimal(''))]").split(',')[2]
    print('\n___________Account Balance___________')
    print(f'Account Number: {accno}')
    print(f'Name          : {name[2:-1]}')
    print(f'Balance       : {balance[10:]}')

def withdraw(accno,amount):
    query='Select Name from CustomerRecord where AccNo=%s and Name not like %s'
    val=(accno,"")
    cur.execute(query,val)
    name=cur.fetchall()[0]
    query='Select Amount from TransactionRecord where AccNo=%s and Name not like %s'
    val=(accno,"")
    cur.execute(query,val)
    dep=amount
    prev_amount=cur.fetchone()
    prev_amount=str(prev_amount).strip("'(Decimal''),'")
    if float(prev_amount)>amount:
        amount=float(prev_amount)-amount
        name=str(name)
        name=name.strip("('',)")
        query='Update TransactionRecord set Amount=%s where accno=%s'
        val=(amount,accno)
        cur.execute(query,val)
        query='Insert into '+name+'(Description,Amount) values(%s,%s)'
        val=('Debit',amount)
        cur.execute(query,val)
        print(f"The amount {dep} has been withdrawn from the account {accno} successfully!")    
    else:
        print('\n___________INSUFFICIENT BALANCE___________\n')

def check_stmt(accno):
    query='Select Name from CustomerRecord where AccNo=%s and Name not like %s'
    val=(accno,"")
    cur.execute(query,val)
    name=cur.fetchall()[0]
    name=str(name)
    name=name.strip("('',)")
    query='Select * from '+name;
    cur.execute(query)
    stmt=cur.fetchall()
    print('\n___________BANK STATEMENT___________')
    print('\n____________________________________')
    print(' SNo  \t Description  \t Amount')
    print('____________________________________')
    for i in stmt:
        sno=int(i[0])
        descript=str(i[1])
        amount=str(i[2])
        amount.strip("Decimal(''))]")
        print(f'  {sno}   \t {descript}   \t {amount}')
        print('____________________________________')
    query='Select Amount from transactionrecord where AccNo=%s and Name not like %s'
    val=(accno,"")
    cur.execute(query,val)
    amount=cur.fetchone()
    amount=str(amount).strip("'(Decimal''),'")
    print('\tBALANCE  \t',amount,'\t\t')
    print('____________________________________\n')
    
def change_pin(accno):
    new_pin=int(input('Enter the New Pin: '))
    query='Update CustomerRecord set pin=%s where accno=%s'
    val=(new_pin,accno)
    cur.execute(query,val)
    print('\n___________PIN Changed Successfully___________\n')

flag=0
limit=3
accno=0
print('Welcome to ABC Bank')
while 1:
    print('---------------------')
    print('1. Register')
    print('2. Deposit')
    print('3. Check Balance')
    print('4. Withdraw')
    print('5. Check Statement')
    print('6. Change pin')
    print('7. Exit')
    print('---------------------')
    choice=int(input('Enter the choice: '))
    if (choice!=1 and choice!=7 and flag==0) or (limit>=0):
        if flag==0 and choice!=1 and choice!=7:
            accno=int(input('Enter the Acc No: '))
        if accno==0 and choice!=1 and choice!=7:
            accno=int(input('Enter the Acc No: '))
        if choice!=1 and choice!=7:
            pin=int(input('Enter the PIN number: '))
        flag=1
    match choice:
        case 1:
            name=input('Enter the Customer Name: ')
            branch=input('Enter the Branch Name: ')
            pin=input('Enter the PIN number: ')
            reg(name,branch,pin)
        case 2:
            try:
                query='Select pin from customerrecord where accno=%s and name not like %s'
                val=(accno,'')
                cur.execute(query,val)
                og_pin=str(cur.fetchone()).strip("'(,)'")
                if pin==int(og_pin):
                    amount=float(input('Enter the Amount to Deposit: '))
                    deposit(accno,amount)
                else:
                    if limit>0:
                        print('\n___________INVALID PIN !!___________\n')
                        print('Try Limit: ',limit)
                        limit-=1
                    else:
                        print('\n___________Limit Exceeded___________\n')
                        break
            except:
                print('\n___________The Entered Account Number is not registered yet___________\n')
                break
        case 3:
            try:
                query='Select pin from customerrecord where accno=%s and name not like %s'
                val=(accno,'')
                cur.execute(query,val)
                og_pin=str(cur.fetchone()).strip("'(,)'")
                if pin==int(og_pin):            
                    check_bal(accno)
                else:
                    if limit>0:
                        print('\n___________INVALID PIN !!___________\n')
                        print('Try Limit: ',limit)
                        limit-=1
                    else:
                        print('\n___________Limit Exceeded___________\n')
                        break
            except:
                print('\n___________The Entered Account Number is not registered yet___________\n')
                break
        case 4:
            try:
                query='Select pin from customerrecord where accno=%s and name not like %s'
                val=(accno,'')
                cur.execute(query,val)
                og_pin=str(cur.fetchone()).strip("'(,)'")
                if pin==int(og_pin):
                    amount=int(input('Enter the amount: '))
                    withdraw(accno,amount)
                else:
                    if limit>0:
                        print('\n___________INVALID PIN !!___________\n')
                        print('Try Limit: ',limit)
                        limit-=1
                    else:
                        print('\n___________Limit Exceeded___________\n')
                        break
            except:
                print('\n___________The Entered Account Number is not registered yet___________\n')
                break

        case 5:
            check_stmt(accno)
        case 6:
            try:
                query='Select pin from customerrecord where accno=%s and name not like %s'
                val=(accno,'')
                cur.execute(query,val)
                og_pin=str(cur.fetchone()).strip("'(,)'")
                if pin==int(og_pin):            
                    change_pin(accno)
                else:
                    if limit>0:
                        print('\n___________INVALID PIN !!___________\n')
                        print('Try Limit: ',limit)
                        limit-=1
                    else:
                        print('\n___________Limit Exceeded___________\n')
                        break
            except:
                print('\n___________The Entered Account Number is not registered yet___________\n')
                break
        case 7:
            break
con.commit()
con.close()

