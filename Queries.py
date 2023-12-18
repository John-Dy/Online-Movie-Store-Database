import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from Information import *

directory = os.path.dirname(os.path.abspath(__file__))
query1 = os.path.join(directory, "sqlscripts", "QUERY1.sql")
query2 = os.path.join(directory, "sqlscripts", "QUERY2.sql")
query3 = os.path.join(directory, "sqlscripts", "QUERY3.sql")
query4 = os.path.join(directory, "sqlscripts", "QUERY4.sql")

### FOR BONUS MARK FOR A9
def select(cursor, table, user_query):
    try:
        table = table.upper()
        if user_query != "":
            if user_query.isnumeric():
                variable = table
                if table == "CUSTOMER_OWNS":
                    variable = "CUSTOMER"
                elif table == "MOVIE_PURCHASED":
                    variable = "PURCHASE"
                elif table == "ACTED":
                    variable = "ACTOR"
                sql_query = f"SELECT * FROM {table} WHERE {variable}ID = {user_query}" #table = Dropdown, user_query = text bar
            else:
                if table == "MOVIE":
                    sql_query = f"SELECT * FROM {table} WHERE MOVIENAME LIKE '%{user_query}%'"
                elif table == "ACTOR" or table == "DIRECTOR" or table == "CUSTOMER":
                    sql_query = f"SELECT * FROM {table} WHERE FULLNAME LIKE '%{user_query}%'"
                elif table == "REVIEW":
                    sql_query = f"SELECT * FROM {table} WHERE COMMENTS LIKE '%{user_query}%'"
        else:
            sql_query = f"SELECT * FROM {table}"
        cursor.execute(sql_query)
        headers = [i[0] for i in cursor.description]
        result = cursor.fetchall()
        return [headers, result, "select"]
    except:
        tk.messagebox.showinfo("Error", "Please Verify Your Inputs")

def update(cursor, conn, table, user_query): #user query is the string id.
    try:
        table = table.upper()
        output = user_query.split(" ")
        id = output[-1]
        new_value = " ".join(output[:-1])
        column_name = table
        if table == "CUSTOMER" or table == "ACTOR" or table == "DIRECTOR":
            column_name = "FULLNAME"
        elif table == "MOVIE":
            column_name = "MOVIENAME"
        elif table == "REVIEW":
            column_name = "COMMENTS"
        sql_query = f"UPDATE {table} SET {column_name} = '{new_value}' WHERE {table}ID = {id}"
        cursor.execute(sql_query)
        conn.commit()
        tk.messagebox.showinfo("Success", f"{table}ID {id} Updated.")
        return None
    except:
        tk.messagebox.showinfo("Error", "Please Verify Your Inputs")

def delete(cursor, conn, table, user_query): #user query is id
    try:
        table = table.upper()
        if user_query.isnumeric():
            variable = table
            if table == "CUSTOMER_OWNS":
                variable = "CUSTOMER"
            elif table == "MOVIE_PURCHASED":
                variable = "PURCHASE"
            elif table == "ACTED":
                variable = "ACTOR"
            sql_query = f"DELETE FROM {table} WHERE {variable}ID = {user_query}"
        else:
            if table == "MOVIE":
                sql_query = f"DELETE FROM {table} WHERE MOVIENAME LIKE '%{user_query}%'"
            elif table == "ACTOR" or table == "DIRECTOR" or table == "CUSTOMER":
                sql_query = f"DELETE FROM {table} WHERE FULLNAME LIKE '%{user_query}%'"
            elif table == "REVIEW":
                sql_query = f"DELETE FROM {table} WHERE COMMENTS LIKE '%{user_query}%'"
        cursor.execute(sql_query)
        conn.commit()
        count = cursor.rowcount
        s = "s"
        if count == 1: s = ""
        tk.messagebox.showinfo("Success", f"{count} row{s} deleted")
        return None
    except:
        tk.messagebox.showerror("Error", "Please Verify Your Inputs")
    

def enter(cursor, conn, selectedOption, selectedTable, inputtedQuery):
    try:
        if selectedOption.upper() == 'VIEW':
            return select(cursor, selectedTable, inputtedQuery)
        if selectedOption.upper()  == 'UPDATE':
            return update(cursor, conn, selectedTable, inputtedQuery)
        if selectedOption.upper()  == 'DELETE':
            return delete(cursor, conn, selectedTable, inputtedQuery)
    except:
        tk.messagebox.showinfo("Error", "Please Verify Your Inputs")

def tableNames(cursor):
    with open(os.path.join(directory, "sqlscripts", "DROP_TABLES.sql")) as f:
        existing_tables = sorted([row[0] for row in cursor.execute("SELECT table_name FROM user_tables")])
        return existing_tables

def drop_tables(cursor):
    try:
        #CALL QUERIES
        with open(os.path.join(directory, "sqlscripts", "DROP_TABLES.sql")) as f:
            commands = f.read().split(';')
            commands = [s.replace('\n', '') for s in commands][:-1] #remove last element thats blank
            
            existing_tables = [row[0] for row in cursor.execute("SELECT table_name FROM user_tables")]
            if len(existing_tables) == 0:
                messagebox.showerror("Failure", "There Are No Tables To Drop.")
            else:
                for command in commands:
                    cursor.execute(command)
                tk.messagebox.showinfo("Success", "Tables Dropped.")
    except:
        tk.messagebox.showerror("Failure", "Query Failed.")


def create_tables(cursor):
    try:
        with open(os.path.join(directory, "sqlscripts", "CREATE_TABLES.sql")) as f:
            sql_script = f.read()

            # Check if each table already exists
            existing_tables = [row[0] for row in cursor.execute("SELECT table_name FROM user_tables")]
            if existing_tables == []:
                # Tables do not exist, proceed with creation
                for command in sql_script.split(';'):
                    command = command.strip()
                    if command and command.startswith("CREATE TABLE"):
                        cursor.execute(command)
                messagebox.showinfo("Success", "Tables Created.")
            else:
                # Tables already exist, show an error message
                messagebox.showerror("Error", "Tables already exist.")
    
    except:
        messagebox.showerror("Failure", "Query Failed.")


def populate_tables(cursor):
    try:
        with open(os.path.join(directory, "sqlscripts", "POPULATE_TABLES.sql")) as f:
            commands = f.read().split(';')
            commands = [s.replace('\n', '') for s in commands][:-1]
            for command in commands:
                cursor.execute(command)
        #CALL QUERIES
        tk.messagebox.showinfo("Success", "Tables Populated.")
    except:
        tk.messagebox.showerror("Failure", "Query Failed.")

def query(cursor, file):
    try:
        with open(file) as f:
            command = f.read().split(";")[0].replace("\n", " ")
            cursor.execute(command)
            headers = [i[0] for i in cursor.description]
            result = cursor.fetchall()
            return [headers, result]
    except:
        tk.messagebox.showerror("Failure", "Query Failed.")
        return None