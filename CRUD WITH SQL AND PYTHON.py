
from http import server
from msilib import Table
import os
import sys
from tkinter import Y
from colorama import Cursor
import pypyodbc as podbc
import pyodbc
import sqlalchemy as sa
from sqlalchemy import event, create_engine, table
from sqlalchemy.engine.url import URL


##AN INTERACTIVE Create Read Update Delete SQL TABLES USING PYTHON SQL DATA MANIPULATION, GOOD FOR BUILDING PYTHON APIs
##Created for fun and to refresh my SQL skills using python, 

class SQLConnection ():
    TblName = input(str("Enter Table Name\n"))         
    
    server= ''; #Enter Username/Server Name  e.g. admin/SQLEXPRESS
    database=''; #Enter Database Name here

    conn2_string = ('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;') #IF YOU ARE USING DIFFERENT DRIVERS, CHANGE THE PARAMETERS BASED ON YOUR SERVER CONFIGS
    conn2 = pyodbc.connect (conn2_string)
    cursor = conn2.cursor()

    
    def GetTables(self): # to get all tables in a given database

        try:
            GetTablesPrompt = input (str("Do you want to get all tables Y/N?")) 
            if GetTablesPrompt == "Y":
                TablesString = "SELECT name FROM sys.tables"
                self.cursor.execute (TablesString)
            
                num = 0

                tablesresult=self.cursor.fetchall()

                for table in tablesresult:
                    
                    print (num, ":", table[0])
                    num=num+1
            if GetTablesPrompt == "N":
                pass
        except:
            pass
        

    def Read(self,TName): #For Reading data in specific tables 
        try:
       
            TName = self.TblName
            QueryString = "SELECT * FROM {}".format(TName)
            
            self.cursor.execute (QueryString)
        
            columns = [column[0] for column in self.cursor.description]

            print (columns)

            result = self.cursor.fetchall()
            

            for row in result:
                print (row)
        except Exception as r:
            print (r)
            pass
  
    def Create(self): #Creating New Table in SQL Database
        

        self.cursor = self.conn2.cursor()
        NewTbl = self.TblName
        CreateTblQry = "CREATE TABLE {} (ID int)".format(NewTbl)
        self.cursor.execute(CreateTblQry)
        try:
            ColumnsNo = int(input("Enter Number of Colums\n"))
            count = 0
            colNames = []
            DType = []

            while ColumnsNo >= count:

                columnName = input (str("enter name of column {}\n".format(count)))
                DataType = input(str("enter data type of {}\n".format(columnName)))
                colNames.append(columnName)
                DType.append(DataType)
                cNM = colNames[count]
                DTy = DType[count]
                cNMDTy = str(cNM) +' '+ str(DTy)
                count = count+1

                QueryString = "ALTER TABLE {} ADD {}".format(NewTbl,cNMDTy)

                self.cursor.execute (QueryString) 
                self.conn2.commit()

                print ("Columns for the NEWLY created table {}\n".format(NewTbl))
                self.Read (TName=NewTbl)
            
        except Exception as e:
            print (e)

    def Insert (self): #Insert Data into Tables
        insTbl = self.TblName
        try:
            self.cursor.execute("SELECT * FROM {}".format(insTbl))
            noCols = self.cursor.arraysize

           
            print ("ENTER DATA TO INSERT TO THE {} COLUMNS OF {}\n".format(noCols,insTbl))

            colfield = [column[0] for column in self.cursor.description]
            IdEnt = int(input("Enter RowID"))
            IdQry = "INSERT INTO {} (ID) VALUES ({}) ".format(insTbl,(IdEnt))
            self.cursor.execute(IdQry)
            self.conn2.commit()



            for name in colfield:
                
                
                entry = input('Enter Data for:'+name) 
                try:

                    UpdtQry =  "UPDATE {} SET {} = '{}' WHERE ID = {}".format(insTbl,name,entry,IdEnt) 
                    self.cursor.execute(UpdtQry)
                    self.conn2.commit()
                    print ("DATA Inserted Succesfully")  
                except Exception as insq:
                    print(insq)  
                    pass    
        except Exception as ins:
            print (ins)
            pass



    def Delete(self):
        Dname = self.TblName
        DelCfrm = input(str("DO YOU WANT TO DELETE {}\n".format(Dname)))
        try:
            if DelCfrm == 'Y':
                DelString = "DROP TABLE {} ".format(Dname)
                self.cursor.execute(DelString)
                print ("Table {} DELETED".format (Dname))
                self.conn2.commit()
            if DelCfrm == 'N':
                pass
            else:
                pass
        except Exception as d:
            print (d)
    def SelectAction(self): #Interactive entry to decide the CRUD option to excecute
        print ("SELECT DATABASE ACTION")
        try:
            ActionChoice = input("Enter:\n A - to get All Tables\n R - to read a Table \n C - to create a table \n I - Insert data to table \n D - to delete a table \n E to exit\n ")
            if ActionChoice == 'A':
                self.GetTables()
            if ActionChoice == 'R':
                self.Read(TName=self.TblName)
            if ActionChoice == 'C':
                self.Create()
            if ActionChoice == 'D':
                self.Delete()
            if ActionChoice == 'I':
                self.Insert()
            if ActionChoice == 'E':
                quit()

        except Exception as sA:
            print (sA)
            pass
 

Exec2 = SQLConnection()
Exec2.SelectAction()















