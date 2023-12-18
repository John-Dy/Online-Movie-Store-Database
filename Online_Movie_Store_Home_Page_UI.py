import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from Queries import *
import Information
import oracledb

class OnlineMovieStore:

    global buttonParams
    buttonParams =  {'width': 400, 'height': 30, 'font': ('Roboto', 16)}  # Adjusted button size parameters and font size
    ctk.set_appearance_mode("dark")

    def __init__(self):
        self.conn = oracledb.connect(user=Information.username, password=Information.password, dsn=Information.dsn)
        self.cursor = self.conn.cursor()

        self.root = ctk.CTk()
        self.root.title("Online Movie Store DBMS")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)

        #DECLARE ALL UI FRAMES
        self.queryFrame = None
        self.recordsFrame = None
        
        self.mainPage()

    def mainPage(self):
        if self.queryFrame != None: self.queryFrame.destroy()
        if self.recordsFrame != None: self.recordsFrame.destroy()

        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.pack(fill="both", expand=True)

        self.title = ctk.CTkLabel(master=self.frame, text="Online Movie Store Database", font=("Roboto",32))
        self.title.pack(pady=20,padx=10)

        self.credits = ctk.CTkLabel(master=self.frame, text="Credits: Maxim Piorischin, Teo Mesrkhani, and John Dy", font=("Roboto",18))
        self.credits.pack(pady=20,padx=10)

        self.createTablesButton = ctk.CTkButton(master=self.frame, text="Create Tables", command=lambda: create_tables(self.cursor), **buttonParams)
        self.createTablesButton.pack(pady=20,padx=10)

        self.populateTablesButton = ctk.CTkButton(master=self.frame, text="Populate Tables", command=lambda: populate_tables(self.cursor), **buttonParams)
        self.populateTablesButton.pack(pady=10,padx=10)

        self.dropTablesButton = ctk.CTkButton(master=self.frame, text="Drop Tables", command=lambda: drop_tables(self.cursor), **buttonParams)
        self.dropTablesButton.pack(pady=20,padx=10)

        self.query = ctk.CTkButton(master=self.frame, text="Queries", command=self.queryUI, **buttonParams)
        self.query.pack(pady=10,padx=10)
        
        self.records = ctk.CTkButton(master=self.frame, text="Manage Records", command=self.recordsUI, **buttonParams) # Read/Update/Delete Tables
        self.records.pack(pady=20,padx=10)
        
        self.exit = ctk.CTkButton(master=self.frame, text="Exit", command = self.__del__, **buttonParams)
        self.exit.pack(pady=10,padx=10)

        self.root.mainloop()
    
    def queryUI(self):
        self.frame.destroy()

        # Create a new frame for queries
        self.queryFrame = ctk.CTkFrame(master=self.root)
        self.queryFrame.pack(fill="both", expand=True)

        # Add widgets for queries to the new frame
        self.queryLabel = ctk.CTkLabel(master=self.queryFrame, text="Queries", font=("Roboto", 32))
        self.queryLabel.pack(pady=20, padx=10)

        # Add buttons for specific queries
        self.query1 = ctk.CTkButton(master=self.queryFrame, text="Query: Customers who own Mulitple Movies", command=lambda: self.updateTable(query(self.cursor, query1), self.table), **buttonParams)
        self.query1.pack(pady=10,padx=10)

        self.query2 = ctk.CTkButton(master=self.queryFrame, text="Query: Purchases and Movies", command=lambda: self.updateTable(query(self.cursor, query2), self.table), **buttonParams)
        self.query2.pack(pady=10,padx=10)

        self.query3 = ctk.CTkButton(master=self.queryFrame, text="Query: Actors and their Movies", command=lambda: self.updateTable(query(self.cursor, query3), self.table), **buttonParams)
        self.query3.pack(pady=10,padx=10)

        self.query4 = ctk.CTkButton(master=self.queryFrame, text="Query: The average score for all movies", command=lambda: self.updateTable(query(self.cursor, query4), self.table), **buttonParams)
        self.query4.pack(pady=10,padx=10)

        self.clear = ctk.CTkButton(master=self.queryFrame, text="Clear Table", command=lambda: self.clearTable(self.table), **buttonParams)
        self.clear.pack(pady=10,padx=10)
 
        # Add frame for table containing data
        self.tableFrame = tk.Frame(master=self.queryFrame)
        self.tableFrame.pack(fill="both", expand=True)
        for i in range(10):
            self.tableFrame.rowconfigure(i, weight=1)
        for j in range(1):
            self.tableFrame.columnconfigure(j, weight=1)

        # Create an empty table initially
        self.headers = ()
        self.table = ttk.Treeview(self.tableFrame, columns=self.headers, show="headings")
        for c in self.headers:
            self.table.heading(c, text=c, command=lambda: None)
            self.table.column(c, width=100)
        self.table.pack(fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self.table, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.backButton = ctk.CTkButton(master=self.queryFrame, text="Back", command=self.mainPage)
        self.backButton.pack(pady=20, padx=10)
    
    # Function for updating data with query results
    def updateTable(self, result, table):
        if result != None:
            self.clearTable(table)
            self.headers = tuple(result[0])
            table['columns'] = self.headers
            self.results = result[1]
            for i in self.headers:
                table.heading(i, text=i)
                table.column(i, width=100)
            for j in self.results:
                table.insert("", "end", values=j)
    
    #Function for clearing table and table headers
    def clearTable(self, table):
        table.delete(*table.get_children())
        table['columns'] = ("")

    def recordsUI(self):

        self.frame.destroy()

        # Create a new frame for queries
        self.recordsFrame = ctk.CTkFrame(master=self.root)
        self.recordsFrame.pack(fill="both", expand=True)

        # Add widgets for queries to the new frame
        self.queryLabel = ctk.CTkLabel(master=self.recordsFrame, text="Manage Records", font=("Roboto", 32)) # Read/Update/Delete Records
        self.queryLabel.pack(pady=20, padx=10)

        # StringVar to store the selected option
        self.selectedOptionVar = ctk.StringVar()
        self.selectedTableVar = ctk.StringVar()
        self.queryTextVar = ctk.StringVar()

        # Radio buttons for view, add, and delete
        self.viewRadio = ctk.CTkRadioButton(master=self.recordsFrame, text="View", variable=self.selectedOptionVar, value="View")
        self.viewRadio.pack(pady=5, padx=10)

        self.addRadio = ctk.CTkRadioButton(master=self.recordsFrame, text="Update", variable=self.selectedOptionVar, value="Update")
        self.addRadio.pack(pady=5, padx=10)

        self.deleteRadio = ctk.CTkRadioButton(master=self.recordsFrame, text="Delete", variable=self.selectedOptionVar, value="Delete")
        self.deleteRadio.pack(pady=5, padx=10)

        # Dropdown for which table user wants to select
        self.optionMenu = ctk.CTkOptionMenu(master=self.recordsFrame, values=tableNames(self.cursor), variable=self.selectedTableVar)
        self.optionMenu.pack(pady=10, padx=10)
        
        # Textbox for queries
        self.queryTextbox = ctk.CTkEntry(master=self.recordsFrame, textvariable=self.queryTextVar)
        self.queryTextbox.pack(pady=10, padx=10, fill="x")
        
        # Enter Button
        self.enterButton = ctk.CTkButton(master=self.recordsFrame, text="Enter", command=lambda: self.manage(enter(self.cursor, self.conn, self.selectedOptionVar.get(), self.selectedTableVar.get(), self.queryTextVar.get()), self.table))
        self.enterButton.pack(pady=10, padx=10)

        self.tableFrame = tk.Frame(master=self.recordsFrame)
        self.tableFrame.pack(fill="both", expand=True)
        for i in range(5):
            self.tableFrame.rowconfigure(i, weight=1)
        for j in range(1):
            self.tableFrame.columnconfigure(j, weight=1)
        self.headers = ()
        self.table = ttk.Treeview(self.tableFrame, columns=self.headers, show="headings")
        for c in self.headers:
            self.table.heading(c, text=c, command=lambda: None)
            self.table.column(c, width=100)
        self.table.pack(fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self.table, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.clear = ctk.CTkButton(master=self.recordsFrame, text="Clear Table", command=lambda: self.clearTable(self.table))
        self.clear.pack(pady=10,padx=10)

        self.backButton = ctk.CTkButton(master=self.recordsFrame, text="Back", command=self.mainPage)
        self.backButton.pack(pady=10, padx=10)

        self.root.mainloop()
    
    def manage(self, enter, table):
        try:
            if enter[2] == "select":
                self.updateTable(enter[0:2], table)
        except:
            pass


    def __del__(self):
        self.cursor.close()
        self.conn.close()
        exit()

if __name__ == "__main__":
    OnlineMovieStore()
