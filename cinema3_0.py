#!/usr/bin/env python3
import logging
import sqlite3
from sqlite3 import Error
from prettytable import PrettyTable
import datetime
import sys
 
class Database:
    tableColumn = {'admin': ('username', 'password', 'firstname', 'lastname', 'email'),
                   'customers': ('username', 'password', 'firstname', 'lastname', 'email'),
                   'booking': ('timeMark', 'username', 'filmID', 'date', 'time', 'seat'),
                   'film': ('filmID', 'film', 'description'),
                   'filmTime': ('date', 'time', 'filmID'), 
                   'seats': ('filmID', 'date', 'time', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5', 'E1', 'E2', 'E3', 'E4', 'E5')}
    def __init__(self, filename):
        self._filename = filename
        
    def getFilename(self):
        return self._filename
        
class Cursor:
    def __init__(self, Database):
        self._connection = sqlite3.connect(Database.getFilename()) # the connection to a database file
        self._cursor = self._connection.cursor()
     
    def getConnection(self):
        return self._connection
    
    def getCursor(self):
        return self._cursor
    
    def selectAll(self, tableName):
        """
        The function querys all rows in a table.
        
        Parameters:
            tableName (string): the table the user want to select
        """
        c = self.getCursor()
        s = 'SELECT * FROM ' + tableName + ';'
        c.execute(s)
        logging.info(s)
        return c.fetchall()
            
    def selectCondition(self, tableName, condition, *column):
        """
        The function selects the rows from a table that satisfy a specific condition.
        
        Parameters:
            tableName (string): the table the user want to select from
            condition (string): the condition the user specifies
            column (string): the column(s) that the user wants to select, blank if want to select all
        """
        c = self.getCursor()
        if len(column) == 0:
            columnList = '*'
        else:
            columnList = ', '.join(str(s) for s in column)
        s = 'SELECT ' +  columnList + ' FROM ' + tableName + ' WHERE ' + condition + ';'
        c.execute(s)
        logging.info(s)
        return c.fetchall()
    
    def select(self, tableName, *column):
        """
        The function selects the rows from a table.
        
        Parameters:
            tableName (string): the table the user want to select from
            column (string): the column(s) that the user wants to select
        """
        c = self.getCursor()
        columnList = ', '.join(str(s) for s in column)
        s = 'SELECT ' +  columnList + ' FROM ' + tableName + ';'
        c.execute(s)
        logging.info(s)
        return c.fetchall()
    
    def selectDistinct(self, tableName, *column):
        """
        The function selects the distinct rows from a table.
        
        Parameters:
            tableName (string): the table the user want to select from
            column (string): the column(s) that the user wants to select
        """
        c = self.getCursor()
        columnList = ', '.join(str(s) for s in column)
        s = 'SELECT DISTINCT ' +  columnList + ' FROM ' + tableName + ';'
        c.execute(s)
        logging.info(s)
        return c.fetchall()
    
    def selectMulti(self, condition, table, column, group):
        """
        The function selects mulitple columns from multiple tables
        
        Parameters:
            condition (tuple)
            table (tuple)
            column (tuple)
            group (tuple)
        """
        try:
            c = self.getCursor()
            tableList = ', '.join(str(s) for s in table)
            columnList = ', '.join(str(s) for s in column)
            if isinstance(group, tuple):
                groupList = ', '.join(str(s) for s in group)
                s = 'SELECT ' + columnList + ' FROM ' + tableList + ' WHERE ' + condition + ' GROUP BY ' + groupList + ';'
            else:
                if len(group) == 0:
                    s = 'SELECT ' + columnList + ' FROM ' + tableList + ' WHERE ' + condition + ';'
                else:
                    groupList = group
                    s = 'SELECT ' + columnList + ' FROM ' + tableList + ' WHERE ' + condition + ' GROUP BY ' + groupList + ';'
            c.execute(s)
            logging.info(s)
            return c.fetchall()
        except Error as e:
            logging.info(e)
    
    def insertCustomer(self, data):
        """
        The function inserts a new row to the table 'customers'.
        
        Parameters:
            data(tuple or list): the username, password, firstname, lastname and email of a customer
        """
        try:
            c = self.getCursor()
            columns = ', '.join(str(c) for c in Database.tableColumn['customers'])
            s = 'INSERT INTO customers (' + columns + ') VALUES (?, ?, ?, ?, ?);'
            c.execute(s, data)
            logging.info(s)
            self.getConnection().commit()
        except sqlite3.IntegrityError:
            print('Error: ID already exists!')
            logging.info('Error: ID already exists!')
    
    def insertBooking(self, data):
        """
        The function inserts a new row to the table 'booking'.
        
        Parameters:
            data(tuple or list): the time mark, username, filmID, screening date, screening time and booked seats
        """
        try:
            c = self.getCursor()
            columns = ', '.join(str(c) for c in Database.tableColumn['booking'])
            s = 'INSERT INTO booking (' + columns + ') VALUES (?, ?, ?, ?, ?, ?);'
            c.execute(s, data)
            logging.info(s)
            self.getConnection().commit()
        except Error as e:
            logging.info(e)
            return Error
        
    def insertFilm(self, data):
        """
        The function inserts a new row to the table 'film'.
        
        Parameters:
            data(tuple or list): the filmID, film, description
        """
        try: 
            c = self.getCursor()
            columns = ', '.join(str(c) for c in Database.tableColumn['film'])
            s = 'INSERT INTO film (' + columns + ') VALUES (?, ?, ?);'
            c.execute(s, data)
            logging.info(s)
            self.getConnection().commit()
            print('Film added!')
        except Error as e:
            logging.info(e)
            print('This film already exists!')
            return Error
        
    def insertScreenTime(self, data):
        """
        The function inserts a new row to the table ' filmTime'.
        
        Parameters:
            data(tuple or list): the filmID, film, description
        """
        try:
            c = self.getCursor()
            columns = ', '.join(str(c) for c in Database.tableColumn['filmTime'])
            s = 'INSERT INTO filmTime (' + columns + ') VALUES (?, ?, ?);'
            c.execute(s, data)
            logging.info(s)
            self.getConnection().commit()
            print('Screening time added!')
        except Error as e:
            logging.info(e)
            print('This time slot is occupied...')
            return Error
        
    def insertSeat(self, data):
        """
        The function inserts a new row to the table ' seats'.
        
        Parameters:
            data(tuple or list): the filmID, date, time (all seats all default to 'O')
        """
        try:
            c = self.getCursor()
            columns = ', '.join(str(c) for c in Database.tableColumn['seats'])
            s = 'INSERT INTO seats (' + columns + ') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
            c.execute(s, data)
            logging.info(s)
            self.getConnection().commit()
        except Error as e:
            logging.info(e)
            return Error
    
    def updateData(self, tableName, key, keyColumn, column, newValue):
        """
        The function update the data of an exsiting row
        
        Parameters:
            tableName (string): the table the user wants to select
            key (string): the key the user wants to update
            keyColumn (string): the primary key column name
            column (string): the column the user wants to update
            newValue (string): the new value to be updated
        """
        c = self.getCursor()
        s = 'UPDATE {} SET {} = (\'' + newValue + '\') WHERE {} = (\'' + key + '\');'
        c.execute(s.format(tableName, column, keyColumn))
        logging.info(s)
        self.getConnection().commit()
        
    def updateSeat(self, key, columnTable):
        """
        The function change the seats back to available in the talbe 'seats'
        when a customer cancels his or her booking.
        
        Parameters:
            key (tuple): (date, time) of the booking
            columnTable (list): the booked seats
        """
        date = key[0]
        time = key[1]
        p = []
        for i in columnTable:
            temp = '{} = \'O\''.format(i)
            p.append(temp)
        pair = ', '.join(str(i) for i in p)
        c = self.getCursor()
        s = 'UPDATE seats SET {} WHERE date = \'{}\' AND time = \'{}\';'
        c.execute(s.format(pair, date, time))
        logging.info(s)
        self.getConnection().commit()
        
    def countAll(self, tableName):
        """
        The function counts the rows from a table.
        
        Parameters:
            tableName (string): the table to count from
        """
        c = self.getCursor()
        s = 'SELECT count(*) FROM ' + tableName + ';'
        c.execute(s)
        logging.info(s)
        return c.fetchall()
    
    def deleteRow(self, table, condition):
        """
        The function deletes a row that meets a certain condition in a table.
        
        Parameters:
            table (string): the table to delete from
            condition (string): the condition 
        """
        try: 
            c = self.getCursor()
            s = 'DELETE FROM ' + table + ' WHERE ' + condition + ';'
            c.execute(s)
            logging.info(s)
            self.getConnection().commit()
        except Error as e:
            logging.info(e)
    
        
class CommandLine:
    def __init__(self, Cursor):
        self._cursor = Cursor
        
    def getCursor(self):
        return self._cursor 
    
    def start(self):
        """
        The function starts the command-line program.
        """
        while True:
            identity = input('\'A\' if you are an admin; \'C\' if you are a customer; \'N\' to create a new account; \'E\' to exit: ')
            if identity.upper() != 'A' and identity.upper() != 'C' and identity.upper() != 'N' and identity.upper() != 'E':
                print('Invalid input!')
            else:
                break
        if identity.upper() == 'E':
            return True # exitStatue = True
        elif identity.upper() == 'N':
            self.createNewCustomer()
        loginUser = self.login(identity.upper())
        if isinstance(loginUser, Customer):
            action = input('Enter \'B\' to book a seat; enter \'P\' to update your profile; enter \'M\' to maneage your booking; enter \'L\' to log out: ')
            actionValid = action.upper() == 'B' or action.upper() == 'P' or action.upper() == 'M' or action.upper() == 'L'
            while action.upper() != 'L':
                while not actionValid:
                    print('Invalid input! Please try again.')
                    logging.info('Invalid input!')
                    action = input('Enter \'B\' to book a seat; enter \'P\' to update your profile; enter \'M\' to maneage your booking; enter \'L\' to log out: ')
                    actionValid = action.upper() == 'B' or action.upper() == 'P' or action.upper() == 'M' or action.upper() == 'L'
                if action.upper() == 'B':
                    logging.info('Book')
                    while True:
                        selectedDate = self.displayFilms()
                        bookSuccess = loginUser.book(selectedDate, self)
                        if bookSuccess:
                            break
                elif action.upper() == 'P':
                    logging.info('Update profile')
                    loginUser.updateProfile(self)
                elif action.upper() == 'M':
                    logging.info('Manage booking')
                    loginUser.manageBooking(self)
                action = input('\nEnter \'B\' to book a seat; enter \'P\' to update your profile; enter \'M\' to maneage your booking; enter \'L\' to log out: ')
                actionValid = action.upper() == 'B' or action.upper() == 'P' or action.upper() == 'M' or action.upper() == 'L'
            self.logout(loginUser)
            return False
        else: # Admin
            print('\n------------------------------------------')
            print('   Welcome to the management system. ;)')
            print('------------------------------------------\n')
            action = input('Enter \'A\' to add films; enter \'O\' to output information; enter \'C\' to check booking; enter \'L\' to log out: ')
            actionValid = action.upper() == 'A' or action.upper() == 'O' or action.upper() == 'C' or action.upper() == 'L'
            while action.upper() != 'L':
                while not actionValid:
                    print('Invalid input! Please try again.')
                    logging.info('Invalid input!')
                    action = input('Enter \'A\' to add films; enter \'O\' to output information; enter \'C\' to check booking; enter \'L\' to log out: ')
                    actionValid = action.upper() == 'A' or action.upper() == 'O' or action.upper() == 'C' or action.upper() == 'L'
                if action.upper() == 'A':
                    logging.info('Add films')
                    loginUser.addFilm(self)
                elif action.upper() == 'O':
                    logging.info('Output information')
                    loginUser.output(self)
                elif action.upper() == 'C':
                    logging.info('Check booking')
                    while True:
                        checkSuccess = loginUser.checkBooking(self)
                        if checkSuccess:
                            break
                else:
                    break
                action = input('\nEnter \'A\' to add films; enter \'O\' to output information; enter \'C\' to check booking; enter \'L\' to log out: ')
                actionValid = action.upper() == 'A' or action.upper() == 'O' or action.upper() == 'C' or action.upper() == 'L'
            self.logout(loginUser)
            return False         
                
    def createNewCustomer(self):
        """
        The function creates a new customer account.
        """
        inputUsername = input('Username: ')
        occupied = Customer.checkUsername(inputUsername, self.getCursor())
        while occupied:
            inputUsername = input('Oops! The username is not available. Please try another one: ')
            occupied = Customer.checkUsername(inputUsername, self.getCursor())
        inputPassword = input('Password: ')
        passwordConfirm = input('Please confirm your password: ')
        confirm = False
        while not confirm:
            if inputPassword != passwordConfirm:
                print('Password does not match, please try again.')
                inputPassword = input('Password: ')
                passwordConfirm = input('Please confirm your password: ')
            else:
                break
        inputFirstname = input('Your first name: ')
        inputLastname = input('Your last name: ')
        inputEmail = input('Your email: ')
        data = (inputUsername, inputPassword, inputFirstname, inputLastname, inputEmail)
        self.getCursor().insertCustomer(data)
        print('Account created!')
        print('Please log in...')
        logging.info('New customer account %s is created.', inputUsername)
        
    def login(self, identity):
        """
        The function is called when a user attempts to log in.
        
        Parameters:
            identity (string): The user input. A if the user wants to log in as an admin;
                               C if the user wants to log in as a customer.
        Returns the User as loginUser
        """
        inputUsername = input('Username: ')
        inputPassword = input('Password: ')
        if identity.upper() == 'A':
            classID = Admin
        else:
            classID = Customer
        validUsername = classID.checkUsername(inputUsername, self.getCursor())
        while not validUsername:
            print('The username doesn\'t exist! Please try again.')
            logging.info('%s %s username does not exist.', classID.getTable(), inputUsername)
            inputUsername = input('Username: ')
            inputPassword = input('Password: ')
            validUsername = classID.checkUsername(inputUsername, self.getCursor())
        correctPassword = classID.checkPassword(inputUsername, inputPassword, self.getCursor())
        while not correctPassword:
            print('The password is not correct! Please try again.')
            logging.info('%s %s: incorrect password!', classID.getTable(), inputUsername)
            inputPassword = input('Password: ')
            correctPassword = classID.checkPassword(inputUsername, inputPassword, self.getCursor())
        loginUser = classID(inputUsername, inputPassword)
        logging.info('%s %s logged in successfully!', classID.getTable(), loginUser.getUsername())
        print('Logged in successfully!')
        return loginUser
    
    def displayFilms(self):
        """
        The function prompts the customer to select a date,
        and displays the film list of film title, screening time and description on a selected day.
        
        Returns the selected date as selectedDate
        """
        selectedDate = self.selectDate()
        condition = 'date = \'{}\''.format(selectedDate)
        tables = ('film', 'filmTime')
        columns = ('film.filmID', 'film', 'time', 'description')
        groups = ('')
        times = []
        for i in range(1, self.filmNum() + 1):
            conditionID = condition + ' AND filmID = {}'.format(i)
            times.append(self.getCursor().selectCondition('filmTime', conditionID, 'time'))
        formattedTimes = [] # each film in one [] in formattedTimes
        for i in times:
            temp = []
            for j in i:
                temp = temp + list(j)
            formattedTimes.append(temp)
        filmInfo = self.getCursor().selectAll('film')
        displayTable = PrettyTable(['Film ID', 'Film', 'Time', 'Description'])
        title = 'Films on {}'.format(selectedDate)
        displayTable.title = title
        for r1, r2 in zip(filmInfo, formattedTimes):
            displayTable.add_row([r1[0], CommandLine.formatMultipleLines(r1[1], 18), '\n'.join(r2), CommandLine.formatMultipleLines(r1[2], 35)])
        print(displayTable)
        logging.info('display films on {}'.format(selectedDate))
        logging.info('\n' + str(displayTable))
        return(selectedDate)
                     
    def logout(self, user):
        """
        The function logs out the user.
        Parameters:
            user (User)
        """
        print('{} logged out successfully!\n'.format(user.getUsername()))
        logging.info('{} logged out.'.format(user.getUsername()))
        self.getCursor().getConnection().commit()
        
    def countAvailable(self, filmID, date, time):
        """
        The function counts the available seats of the 'filmID' at 'time' on 'date'.
        
        Parameters:
            filmID (string)
            date (string)
            time (string)
        """
        condition = 'date = \'{}\' AND time = \'{}\''.format(date, time)
        film = self.getCursor().selectCondition('film', 'filmID = {}'.format(filmID), 'film')
        bookStatue = self.getCursor().selectCondition('seats', condition, 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5', 'E1', 'E2', 'E3', 'E4', 'E5')
        available = 0
        for i in bookStatue[0]:
            if i == 'O':
                available += 1
        booked = 25 - available
        return (available, booked)
    
    def displayFilm(self):
        """
        The function displays the films and their description.
        """
        filmList = self.getCursor().selectAll('film')
        filmTable = PrettyTable(['FilmID', 'Film', 'Description'])
        for r in filmList:
            filmTable.add_row([r[0], CommandLine.formatMultipleLines(r[1], 20), CommandLine.formatMultipleLines(r[2], 40)])
        print(filmTable)
        
    def displaySeats(self, seat):
        """
        The function returns the seat layout and available seats.
        
        Parameters:
            seat (list): the list returned from the database
        Returns:
            seatTable (PrettyTable): The seat layout
            available (int): the number of the available seats
        """
        count = 1
        available = 0
        row = []
        seatTable = PrettyTable([' ', '1', '2', '3', '4', '5'])
        seatTable.title = 'Screen'
        for i in seat[0]:
            row.append(i)
            if i == 'O':
                available += 1
            if count % 5 == 0:
                seatTable.add_row([chr(64 + int(count / 5)), row[0], row[1], row[2], row[3], row[4]])
                row = []
            count += 1
        print(seatTable)
        print('O: seats available; X: seats taken\n')
        logging.info('\n' + str(seatTable))
        logging.info('O: seats available; X: seats taken')
        return (seatTable, available)
        
    def checkFilmID(self, ipt):
        """
        The function checks if 'ipt' is a valid filmID
        
        Parameters:
            ipt (int): The user input filmID
        Returns False if it's invalid;
        returns True if it's valid.
        """
        totalFilms = self.getCursor().countAll('film') # return [(n,)]
        try:
            int(ipt)
        except:
            return False
        else:
            if int(ipt) <= totalFilms[0][0] and int(ipt) >= 1:
                return True
        return False
    
    def filmNum(self):
        """
        The function counts the total number of films.
        """
        totalFilms = self.getCursor().countAll('film') # return [(n,)]
        return totalFilms[0][0]
        
    def selectFilm(self):
        """
        The function prompts the user to select a filmID
        
        Returns the filmID
        """
        filmID = input('Please enter the film ID: ')
        validID = self.checkFilmID(filmID)
        while not validID:
            print('Invalid film ID. Please try again.')
            filmID = input('Please enter the film ID: ')
            validID = self.checkFilmID(filmID)
        return filmID
        
    def selectDate(self):
        """
        The function prompts the user to select a date
        
        Returns the date
        """
        dateAvailable = self.getCursor().selectDistinct('filmTime', 'date')
        days = CommandLine.printDate(dateAvailable)
        inputDate = input('Please select a date: ')
        try:
            int(inputDate)
        except:
            validDate = False
        else:
            validDate = int(inputDate) >= 1 and int(inputDate) <= days
        while not validDate:
            print('Invalid input! Please try again.')
            CommandLine.printDate(dateAvailable)
            inputDate = input('Please select a date: ')
            try:
                int(inputDate)
            except:
                validDate = False
            else:
                validDate = int(inputDate) >= 1 and int(inputDate) <= days
        selectedDate = dateAvailable[int(inputDate) - 1][0]
        return selectedDate
    
    def selectTime(self, date, filmID):
        """
        The function prompts the user to select a time slot
        
        Returns the time slot
        """
        timeSlots = self.getCursor().selectCondition('filmTime', 'date = \'{}\' AND filmID = {}'.format(date, filmID), 'time')
        cnt = CommandLine.printDate(timeSlots)
        if not cnt: # no available time slot
            print('No available time slot on this day...\nPlease try again.')
            return 
        timeNumber = input('Please select a time slot: ')
        try:
            int(timeNumber)
        except:
            validTime = False
        else:
            validTime = int(timeNumber) >= 1 and int(timeNumber) <= cnt
        while not validTime:
            print('Invalid input! Please try again.')
            CommandLine.printDate(timeSlots)
            timeNumber = input('Please select a time slot: ')
            try:
                int(timeNumber)
            except:
                validTime = False
            else:
                validTime = int(timeNumber) >= 1 and int(timeNumber) <= cnt
        timeSelected = timeSlots[int(timeNumber) - 1][0]
        return timeSelected
    
    @staticmethod
    def printDate(dateAvailable):
        """
        The function prints the date that a customer can book from
        
        Returns the the number of days
        """
        cnt = 0
        print('')
        for i in dateAvailable:
            cnt += 1
            print('{}: {}'.format(cnt, i[0]))
        return cnt
    
    @staticmethod
    def formatMultipleLines(text, maxLength):
        """
        The function formats a long text to pass into PrettyTable
        
        Parameters:
            text (string): the string to fromat
            maxLength (int): the max length per line
        
        Returns a text with \n
        """
        count = 0
        splitText = text.split(' ')
        formatted = ''
        for t in splitText:
            if count + len(t) + 1 <= maxLength:
                formatted = formatted + t + ' '
                count += len(t) + 1
            else:
                formatted = formatted + '\n' + t + ' '
                count = len(t) + 1
        return formatted
    
    @staticmethod
    def checkSeatInput(ipt):
        """
        The function checks if the input of a seat is in the range.
        
        Parameters:
            ipt (string): user input
        """
        if len(ipt) != 2:
            return False
        alphas = set('ABCDE')
        if set(ipt[0]) <= alphas and int(ipt[1]) >= 1 and int(ipt[1]) <= 5:
            return True
        return False
    
    @staticmethod
    def confirmInsert(columns, data, title):
        """
        The function prints the confirmation table when an admin tries to add a new screening time.
        
        Parameters:
            columns (list): the column name to pass to PrettyTable
            data (list): the data to put in the table
            title (string): the table title
        """
        confirm = PrettyTable(columns)
        confirm.add_row(data)
        confirm.title = title
        print(confirm)

class User:
    def __init__(self, un, pw):
        self._username = un
        self._password = pw
        self._pair = {un: pw}
        
    def getUsername(self):
        return self._username
        
    @classmethod
    def checkUsername(cls, un, table, cursor):
        """
        return True if the username exists
        """
        condition = 'username = \'' + un + '\''
        result = cursor.selectCondition(table, condition, 'username')
        if not result:
            return False
        return True
        
    @classmethod
    def checkPassword(cls, un, pw, table, cursor):
        condition = 'username = \'' + un + '\''
        result = cursor.selectCondition(table, condition, 'username', 'password')
        pair = dict(result) # transfer the (username, password) pair to dictionary
        if pair[un] == pw:
            return True
        return False
            
class Admin(User):
    table = 'admin'
    def __init__(self, un, pw):
        super().__init__(un, pw)
        
    def __str__(self):
        return self.getUsername()
    
    def addFilm(self, cml):
        """
        The function adds new film to the table 'film'
        
        Parameters:
            cml (CommandLine)
        """
        while True:
            addItem = input('Enter \'t\' to add a new screening time of an existing film; enter \'n\' to add a new film: ')
            if addItem.lower() != 't' and addItem.lower() != 'n':
                print('Invalid input! Please try again.')
            else:
                break
        if addItem.lower() == 't':
            cml.displayFilm()
            filmID = cml.selectFilm()
            result = cml.getCursor().selectCondition('film', 'filmID = {}'.format(filmID), 'film', 'description')
            film = result[0][0]
            description = result[0][1]
        elif addItem.lower() == 'n':
            filmNum = cml.getCursor().countAll('film')[0][0]
            film = input('Enter the film title: ')
            description = input('Enter the description of the film: ')
        date = input('Enter the screening date (e.g. 2019/01/01): ')
        time = input('Enter the screening time (e.g. 09:00): ')
        columns = ['Film', 'Description', 'Date', 'Time']
        data = [film, CommandLine.formatMultipleLines(description, 30), date, time]
        CommandLine.confirmInsert(columns, data, 'Insert Film Confirmation')
        confirm = input('Enter \'Y\' to confirm; enter \'N\' to start again: ')
        confirmValid = confirm.upper() == 'Y' or confirm.upper() == 'N'
        while not confirmValid:
            print('Invalid input! Please try again.')
            confirm = input('Enter \'Y\' to confirm; enter \'N\' to start again: ')
            confirmValid = confirm.upper() == 'Y' or confirm.upper() == 'N'
        if confirm.upper() == 'Y':
            if addItem.lower() == 't':
                timeError = cml.getCursor().insertScreenTime([date, time, filmID])
                if not timeError:
                    seatError = cml.getCursor().insertSeat([filmID, date, time, 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'])
                    errorExit = timeError or seatError
                else:
                    errorExit = True
            else:
                newFilmID = str(filmNum + 1)
                filmError = cml.getCursor().insertFilm([newFilmID, film, description])
                if not filmError:
                    timeError = cml.getCursor().insertScreenTime([date, time, newFilmID])
                    if not timeError:
                        seatError = cml.getCursor().insertSeat([newFilmID, date, time, 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'])
                    else:
                        errorExit = True
                else:
                    errorExit = True
                errorExit = filmError or timeError or seatError
            if errorExit:
                print('Something is wrong. Please try again.')
                self.addFilm(cml)
        else:
            self.addFilm(cml)
            
    def checkBooking(self, cml):
        """
        The function checks the available seats of a film.
        
        Parameters:
            cml (CommandLine)
        
        Returns False if there is no available time slot on the selected day;
        returns True when prints the information successfully.
        """
        cml.displayFilm()
        filmID = cml.selectFilm()
        date = cml.selectDate()
        time = cml.selectTime(date, filmID)
        if not time:
            return False
        condition = 'date = \'{}\' AND time = \'{}\''.format(date, time)
        film = cml.getCursor().selectCondition('film', 'filmID = {}'.format(filmID), 'film')
        bookStatue = cml.getCursor().selectCondition('seats', condition, 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5', 'E1', 'E2', 'E3', 'E4', 'E5')
        print('\nSeats of \'{}\' screening at {} on {}\n'.format(film[0][0], time, date))
        result = cml.displaySeats(bookStatue)
        statusTable = result[0]
        available = result[1]
        print('Total: 25; Booked: {}; Available: {}\n'.format(25 - available, available))
        logging.info('Seats of \'{}\' screening at {} on {}'.format(film[0][0], time, date))
        logging.info('Total: 25; Booked: {}; Available: {}\n'.format(25 - available, available))
        return True
    
    def output(self, cml):
        """
        The function ouputs the film information.
        
        Parameters:
            cml (CommandLine)
        """
        condition = 'film.filmID = filmTime.filmID'
        table = ('film', 'filmTime')
        column = ('film.filmID', 'film.film', 'filmTime.date', 'filmTime.time')
        group = ''
        result = cml.getCursor().selectMulti(condition, table, column, group)
        outputTime = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        s = '{}_filmsAndSeats.csv'.format(outputTime)
        file = open(s, 'w+') # w+ will create a new file if it doesn't exist
        file.write('filmID, film, date, time, available_seats, booked_seats\n')
        for row in result:
            count = cml.countAvailable(row[0], row[2], row[3])
            file.write('{}, {}, {}, {}, {}, {}\n'.format(row[0], row[1], row[2], row[3], count[0], count[1]))
        file.close()
        logging.info('File exported')
        print('File exported.')
    
    @classmethod
    def getTable(cls):
        return cls.table
        
    @classmethod
    def checkUsername(cls, un, cursor):
        return super().checkUsername(un, cls.table, cursor)
        
    @classmethod
    def checkPassword(cls, un, pw, cursor):
        return super().checkPassword(un, pw, cls.table, cursor)
    
class Customer(User):
    table = 'customers'
    def __init__(self, un, pw):
        super().__init__(un, pw)
        
    def __str__(self):
        return self.getUsername()
    
    def book(self, date, cml):
        """
        The function is called when a customer wants to book a seat.
        
        Parameters:
            date (string): the date the customer selected
            cml (CommandLine)
            
        Returns False when the seats are occupied;
        returns True when the booking succeed.
        """
        print('\n-----------------------------------------')
        print('    Welcome to the booking system. :D')
        print('-----------------------------------------\n')
        filmID = cml.selectFilm()
        timeSelected = cml.selectTime(date, filmID)
        if not timeSelected:
            return False
        condition = 'filmID = {} AND date = \'{}\' AND time = \'{}\''.format(filmID, date, timeSelected)
        seat = cml.getCursor().selectCondition('seats', condition, 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5', 'E1', 'E2', 'E3', 'E4', 'E5')
        cml.displaySeats(seat)
        bookSucceed = False
        while not bookSucceed:
            seatsWanted = input('Please enter the seats you want to book (e.g., B3 B4): ')
            splitInput = seatsWanted.split(' ')
            for i in splitInput:
                if not CommandLine.checkSeatInput(i):
                    print('Invalid input! Please enter A1 - E5.')
                    logging.info('Invalid input! Out of seat range.')
                    break
            else: # if all the seats wanted have the right format (doesn't break)
                occupied = False
                occupiedSeat = []
                for i in splitInput:
                    seatStatus = cml.getCursor().selectCondition('seats', condition, i)
                    if seatStatus[0][0] == 'X':
                        occupied = True
                        occupiedSeat.append(i)
                if occupied:
                    print(', '.join(i for i in occupiedSeat), end = '')
                    print(' is/are not available. Please try again.')
                    logging.info('Seat(s) is/are occupied')
                    continue
                else: # inputs are valid and not occupied
                    for i in splitInput:
                        cml.getCursor().updateData('seats', filmID, 'filmID', i, 'X') # update the booked seat
                    currentTime = datetime.datetime.now()
                    formattedCurrentTime = currentTime.strftime('%Y/%m/%d %H:%M')
                    data = (formattedCurrentTime, self.getUsername(), filmID, date, timeSelected, seatsWanted)
                    cml.getCursor().insertBooking(data)
                    logging.info('%s (filmID) on %s at %s %s is/are booked', filmID, date, timeSelected, seatsWanted)
                    bookSucceed = True
        print('Successfully booked!')
        bookingSummary = PrettyTable(['FilmID', 'Screening Date', 'Screening Time', 'Seat'])
        bookingSummary.title = 'Booking Summary'
        bookingSummary.add_row([filmID, date, timeSelected, seatsWanted])
        print(bookingSummary)
        return True
    
    def updateProfile(self, cml):
        """
        The function updates the profile of a customer.
        
        Parameters:
            cml (CommandLine)
        
        Returns if the customer enter 'r' to return.
        """
        username = self.getUsername()
        profile = cml.getCursor().selectCondition('customers', 'username = \'{}\''.format(username), 'firstname', 'lastname', 'email')
        userProfile = PrettyTable(['Username', 'First Name', 'Last Name', 'Email'])
        userProfile.title = 'User Profile'
        userProfile.add_row([username, profile[0][0], profile[0][1], profile[0][2]])
        print(userProfile)
        columns = Database.tableColumn['customers'][1:]
        print('')
        for cnt, i in zip(range(len(columns)), columns):
            print('{}: {}'.format(cnt + 1, i))
        section = input('Please enter the section you want to change (you cannot change your username), or enter \'r\' to return: ')
        if section.lower() == 'r':
            return
        else:
            try:
                sectionNum = int(section)
            except:
                validSection = False
            else:
                validSection = sectionNum >= 1 and sectionNum <= len(columns)
            while not validSection:
                print('Invalid input! Please try again.')
                section = input('Please enter the section you want to change (you cannot change your username): ')
                try:
                    sectionNum = int(section)
                except:
                    validSection = False
                else:
                    validSection = sectionNum >= 1 and sectionNum <= len(columns)
            newValue = input('Please enter your new {}: '.format(columns[sectionNum - 1]))
            confirmNewValue = input('Please confirm your new {}: '.format(columns[sectionNum - 1]))
            while newValue != confirmNewValue:
                print('Your inputs do not match! Please try again.')
                newValue = input('Please enter your new {}: '.format(columns[sectionNum - 1]))
                confirmNewValue = input('Please confirm your new {}: '.format(columns[sectionNum - 1]))
            cml.getCursor().updateData('customers', username, 'username', columns[sectionNum - 1], newValue)
            print('Profile updated successfully!')
            logging.info('Profile updated')
            keepUpdate = input('Enter \'u\' to update other information; enter \'r\' to return: ')
            validInput = keepUpdate.lower() == 'u' or keepUpdate.lower() == 'r'
            while not validInput:
                print('Invalid input! Please try again.')
                keepUpdate = input('Enter \'u\' to update other information; enter \'r\' to return: ')
                validInput = keepUpdate.lower() == 'u' or keepUpdate.lower() == 'r'
            if keepUpdate.lower() == 'u':
                self.updateProfile(cml)
                
    def bookingHistory(self, cml):
        """
        The function shows the booking history of a customer.
        
        Parameters:
            cml (CommandLine)
            
        Returns the list 'history' the database returned
        """
        username = self.getUsername()
        condition = 'username = \'{}\' AND film.filmID = booking.filmID'.format(username)
        table = ('film', 'booking')
        column = ('film.film', 'booking.date', 'booking.time', 'booking.seat')
        group = ''
        history = cml.getCursor().selectMulti(condition, table, column, group)
        historyTable = PrettyTable(['BookingID', 'Film', 'Screening Date', 'Screening Time', 'Seat'])
        historyTable.title = '{}\'s Booking History'.format(username)
        for cnt, i in zip(range(1, len(history) + 1), history):
            historyTable.add_row([cnt, i[0], i[1], i[2], i[3]])
        print(historyTable)
        return history
    
    def manageBooking(self, cml):
        """
        The function manages the booking history of a customer.
        
        Parameters:
            cml (CommandLine)
            
        Returns when the customer tries to cancel a past booking.
        """
        history = self.bookingHistory(cml)
        if history: # the customer has a booking 
            bookingID = input('Please enter the ID of the booking you want to cancel; \'r\' to return: ')
            if bookingID == 'r':
                return
            try:
                intBookingID = int(bookingID)
            except:
                validID = False
            else:
                validID = intBookingID >= 1 and intBookingID <= len(history)
            while not validID:
                print('Invalid input! Please try again.')
                bookingID = input('Please enter the ID of the booking you want to cancel; \'r\' to return: ')
                if bookingID == 'r':
                    return
                try:
                    intBookingID = int(bookingID)
                except:
                    validID = False
                else:
                    validID = intBookingID >= 1 and intBookingID <= len(history)
            date = history[intBookingID - 1][1]
            time = history[intBookingID - 1][2]
            dateInt = []
            for i in date.split('/'):
                dateInt.append(int(i))
            if datetime.date(dateInt[0], dateInt[1], dateInt[2]) <= datetime.date.today():
                print('You can only change a future booking.')
                return
            else:
                condition = 'username = \'{}\' AND date = \'{}\' AND time = \'{}\' AND seat = \'{}\''.format(self.getUsername(), date, time, history[intBookingID - 1][3])
                cml.getCursor().deleteRow('booking', condition)
                print('Booking deleted!')
                cml.getCursor().updateSeat((date, time), (history[intBookingID - 1][3].split(' ')))
        else: # no booking
            print('You have no booking history...')
    
    @classmethod
    def getTable(cls):
        return cls.table
        
    @classmethod
    def checkUsername(cls, un, cursor):
        return super().checkUsername(un, cls.table, cursor)
        
    @classmethod
    def checkPassword(cls, un, pw, cursor):
        return super().checkPassword(un, pw, cls.table, cursor)
 
def main():
    logging.basicConfig(filename = 'cinema.log', filemode = 'w', format = '%(asctime)s %(levelname)s %(message)s'
                        , level = logging.INFO)
    databaseFile = 'bookingSystem.db'
    bookingSystem = Database(databaseFile)
    cursor = Cursor(bookingSystem) # connect and create cursor
    logging.info('Connects to the database %s.', databaseFile)
    command = CommandLine(cursor)
    print('-----------------------------------')
    print('       Welcome to THE CINEMA')
    print('-----------------------------------\n')
    exitStatus = False
    while not exitStatus:
        exitStatus = command.start()
    print('\n-----------------------------------')
    print('    Bye Bye. See you next time!')
    print('-----------------------------------')
    command.getCursor().getConnection().close()

if __name__ == '__main__': main()
    
 
        
    
