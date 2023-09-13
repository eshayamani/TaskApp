# CPSC 408 Final Project

### Student Info
* Esha Yamani
    * email: yamani@chapman.edu
    * ID: 2377310
* Lucas Gaudet
    * email: lgaudet@chapman.edu
    * ID: 2377818

### Known Errors:
* None

### Instructions

The only dependency should be flask, to install run:
```
pip install Flask
```
Before starting the program, first create the tables and views by running the .SQL file.

The database file is included, be sure to load that so you have data in the database.

To start the program run:
```
flask run
```
This should launch a development server and show a URL to localhost (127.0.0.1) in the terminal. To access the app, hold control (command if you're on mac) and then click the url. This will launch the app in your default web browser.

From here you should be greeted with a login screen, if you don't have login information you can click the 'sign up here!' link. 

Once logged in, you will land at the dashboard. The dashboard will show you all your tasks, which are grouped by group. You can create new tasks and assign an existing group or create a new one. Then it will show up in your dashboard. 

To access or create subtasks, click the title of the task. This will take you to a subtask page. 

To change the status of a task, check or uncheck the checkbox. This will automatically update the status of your task.

To delete tasks or subtasks click the delete button.

To export all tasks, click the 'Export CSV' button.

To logout, click the logout button. This will reset the session userID and return you to the login page.