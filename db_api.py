import mysql.connector
import csv

class db_operations: 
    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                                                user='root',
                                                password='cpsc408!',
                                                auth_plugin='mysql_native_password',
                                                database='TaskApp')

        # create cursor object
        self.cursor = self.connection.cursor()
        print('connection made...')

    def destroy(self):
        self.connection.close()
        self.cursor.close()


    #checking if the email already exists
    def check_email(self, emailToCheck):
        query = '''
        SELECT userID
        FROM users
        WHERE email = '%s';
        ''' %emailToCheck
        try:
            #find the userID
            self.cursor.execute(query)
            print(self.cursor.fetchone()[0])
            # email exists
            return 1
        except:
            # email does not exist
            return 0
    
    #checking if the given password matches
    def check_password(self, emailToCheck, passwordToCheck):
        query = '''
        SELECT password
        FROM users
        WHERE email = '%s';
        ''' %emailToCheck
        
        self.cursor.execute(query)
        passwordFound = self.cursor.fetchone()[0]
        if passwordToCheck == passwordFound:
            #return 1 if the passwords match
            print("the passwords match")
            return 1
        else:
            print("the passwords don't match")
            return 0
    
    #getting user id from email    
    def get_user_id(self, email):
        query = '''
        SELECT userID
        FROM users
        WHERE email = '%s'
        ''' % email
        self.cursor.execute(query)
        # print(self.cursor.fetchone()[0])
        return self.cursor.fetchone()[0]
    
    #getting user name from id
    def get_user_name(self, id):
        query = '''
        SELECT name
        FROM users
        WHERE userID = '%s'
        ''' % id
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    #insert a new user
    def new_user(self, nameToAdd, emailToAdd, passwordToAdd):
        print("Adding new user")
        print("name:", nameToAdd, '\nemail:', emailToAdd, '\npassword:', passwordToAdd)
        query = '''
        INSERT INTO users (name, email, password)
        VALUES ('%s','%s','%s');
        ''' %(nameToAdd, emailToAdd, passwordToAdd)
        self.cursor.execute(query)
        self.connection.commit()
        print("New User added!")
        
    #get group membership given an email
    def get_groups(self, lookUpID):
        print("Finding groups for:", lookUpID)
        query = '''
        SELECT g.groupID
        FROM groupMembers g
            INNER JOIN users u
            ON g.userID = u.userID
        WHERE g.userID = '%s';
        ''' % lookUpID
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        #create a list of groups
        group_list = []
        for i in results:
            group_list.append(i[0])
        print("group list is:", group_list)
        return group_list
    
    #get group names from id
    def get_group_names(self, groupID):
        query = '''
        SELECT name
        FROM userGroups
        WHERE groupID = '%s';
        ''' % groupID
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result
        
    #get all the tasks for each group user is in       
    def get_group_tasks(self, groupLookUp):
        print("getting tasks for group:", groupLookUp)
        query = '''
        SELECT t.taskID, t.title, t.dueDate, t.status, c.name AS category, c.priority AS priority
        FROM tasks t
            INNER JOIN category c
            ON t.categoryID = c.categoryID
        WHERE t.groupID = '%s'
        ORDER BY t.status ASC;
        ''' %groupLookUp
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results
    
    #get the subtasks for a given task  
    def get_subtasks(self, taskID):
        print("getting subtasks for task:", taskID)
        query = '''
        SELECT subTaskID, title, dueDate, status
        FROM subtasks
        WHERE taskID = '%s'
        ORDER BY status ASC;
        ''' %taskID
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        print(results)
        return results
    
    #edit groups functionality
    #change user group or task group
    def change_group(self, email, group):
        #change user group
        print("moving user to group:", group)
        query = '''
        SELECT userID
        FROM users
        WHERE email = '%s'
        ''' %email
        self.cursor.execute(query)
        userID = self.cursor.fetchone()[0]
        query = '''
        UPDATE groupMembers
        SET groupID = '%s'
        WHERE userID = '%s';
        ''' % (group, userID)
        self.cursor.execute(query)
        self.connection.commit()

    #insert new task into table
    def insert_new_task(self, title, dueDate, categoryName, groupName, userID):
        # get group ID
            # if it does not exist, create it
        query = '''
        SELECT groupID
        FROM userGroups
        WHERE name = '%s';
        ''' % groupName.lower()
        try:
            self.cursor.execute(query)
            groupID = self.cursor.fetchone()[0]
        except:
            #insert query
            query = '''
            INSERT into userGroups(name)
            VALUES('%s');
            ''' % groupName
            self.cursor.execute(query)
            self.connection.commit()
            #get groupID
            query = '''
            SELECT groupID
            FROM userGroups
            WHERE name = '%s';
            ''' % groupName
            self.cursor.execute(query)
            groupID = self.cursor.fetchone()[0]
            #insert both pieces of information
            query = '''
            INSERT into groupMembers
            VALUES('%i', '%i');
            ''' % (userID, groupID)
            self.cursor.execute(query)
            self.connection.commit()

        # get category ID
            # if it does not exist, create it
        query = '''
        SELECT categoryID
        FROM category
        WHERE name = '%s';
        ''' % categoryName.lower()
        try:
            self.cursor.execute(query)
            categoryID = self.cursor.fetchone()[0]
        except:
            #create new value if it doesn't exist
            query = '''
            INSERT into category(name)
            VALUES('%s');
            ''' % categoryName
            self.cursor.execute(query)
            self.connection.commit()
            #get the new cateogryID
            query = '''
            SELECT categoryID
            FROM category
            WHERE name = '%s';
            ''' % categoryName
            self.cursor.execute(query)
            categoryID = self.cursor.fetchone()[0]
        
        query = '''
        INSERT INTO tasks (title, dueDate, categoryID, groupID)
        VALUES ('%s','%s','%s','%s');
        ''' %(title, dueDate, categoryID, groupID)
        self.cursor.execute(query)
        self.connection.commit()

    #insert a new subtask into table
    def insert_new_subtask(self, title, dueDate, parent_task):
        query = '''
        INSERT into subTasks(title, dueDate, taskID)
        VALUES('%s', '%s', '%s');
        ''' % (title, dueDate, parent_task)
        self.cursor.execute(query)
        self.connection.commit()

    #delete just the subtask
    def delete_subtask(self, subTaskID):
        query = '''
        DELETE FROM subTasks
        WHERE subTaskID = '%s';
        ''' % subTaskID
        self.cursor.execute(query)
        self.connection.commit()

    #deleting a task and its subtasks
    def delete_task(self, taskID):
        query = '''
        DELETE FROM subTasks
        WHERE taskID = '%s';
        ''' % taskID
        self.cursor.execute(query)
        self.connection.commit()

        query = '''
        DELETE FROM tasks
        WHERE taskID = '%s';
        ''' % taskID
        self.cursor.execute(query)
        self.connection.commit()
    
    #delete tasks and its subtasks using transaction
    def delete_task_transaction(self, taskID):
        try:
            #start SQL transaction
            self.cursor.execute("START TRANSACTION")
            #delete subtasks associated with the given task ID
            self.cursor.execute("DELETE FROM subTasks WHERE taskID = %s", (taskID,))
            #delete the task with the given task ID
            self.cursor.execute("DELETE FROM tasks WHERE taskID = %s", (taskID,))
            self.connection.commit()
        except mysql.connector.Error as error:
            self.connection.rollback()

    #change the complete or incomplete status for task
    def set_task_status(self, taskID, newStatus):
        query = '''
        UPDATE tasks
        SET status = '%s'
        WHERE taskID = '%s';
        ''' % (newStatus, taskID)
        self.cursor.execute(query)
        self.connection.commit()

    #change the complete or incomplete status for subtask
    def set_subtask_status(self, taskID, newStatus):
        query = '''
        UPDATE subTasks
        SET status = '%s'
        WHERE subTaskID = '%s';
        ''' % (newStatus, taskID)
        self.cursor.execute(query)
        self.connection.commit()

    def get_taskname_from_id(self, taskID):
        query = '''
        SELECT title
        FROM tasks
        WHERE taskID = '%s';
        ''' % taskID
        self.cursor.execute(query)
        taskName = self.cursor.fetchone()[0]
        return taskName
    
    #creating a view of groups, tasks and users
    def get_view(self):
        #this is for all users not individual
        try: 
            query = '''
            CREATE VIEW vDetails AS
            SELECT g.name, t.title, t.dueDate, c.name AS category, u.name AS user
            FROM tasks AS t
            INNER JOIN userGroups AS g
                ON t.groupID = g.groupID
            INNER JOIN category AS c
                ON t.categoryID = c.categoryID
            INNER JOIN groupMembers AS gM 
                ON g.groupID = gM.groupID
            INNER JOIN users AS u 
                ON gM.userID = u.userID;
            '''
            self.cursor.execute(query)
            self.connection.commit()
        except:
            pass
        #print out values in view
        query = '''
        SELECT *
        FROM vDetails;
        '''
        self.cursor.execute(query)
        self.connection.fetchall()
        
    #aggregate - get total number of tasks
    def total_tasks(self, userID):
        query = '''
        SELECT COUNT(taskID)
        FROM tasks AS t
        INNER JOIN groupMembers AS g
            ON t.groupID = g.groupID
        WHERE g.userID = '%s'; 
        ''' %userID
        self.cursor.execute(query)
        total = self.cursor.fetchone()[0]
        return total
    
    #convert the view into a csv file  
    def convert_to_csv(self, userID):
        #need to make sure the create view function runs first
        query = '''
        SELECT *
        FROM vDetails
        '''
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        #getting column names
        column_names = [desc[0] for desc in self.cursor.description]

        info = {}
        info['column_names'] = column_names
        info['results'] = results
        print("done")
        return info