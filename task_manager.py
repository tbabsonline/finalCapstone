#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass
# Read tasks from the tasks.txt file and return a list of task
def read_tasks():
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT).date()
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT).date()
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

    return task_list
# Write tasks to the task.txt file
def write_tasks(task_list):
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# Create user.txt if it doesn't exist
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")
# Read users from the user.txt file and return a dictionary of username-password credentials
def read_users():
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    return username_password
# Write users to the user.txt file
def write_users(username_password):
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_password:
            user_data.append(f"{k};{username_password[k]}")
        out_file.write("\n".join(user_data))
# Register a new user by adding their username and password credentials to the user.txt file
def reg_user():
    new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    username_password = read_users()

    if new_username in username_password:
        print("Username already exists. Please choose a different username.")
    elif new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        write_users(username_password)
    else:
        print("Passwords do not match")
# Add a new task by prompting for input from the user
def add_task():
    task_username = input("Name of person assigned to task: ")
    username_password = read_users()

    if task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = datetime.strptime(input("Due Date (YYYY-MM-DD): "), DATETIME_STRING_FORMAT).date()
            break
        except ValueError:
            print("Invalid date format. Please enter a valid date (YYYY-MM-DD)")

    task_assigned_date = date.today()

    new_task = {
        'username': task_username,
        'title': task_title,
        'description': task_description,
        'due_date': task_due_date,
        'assigned_date': task_assigned_date,
        'completed': False
    }

    task_list = read_tasks()
    task_list.append(new_task)
    write_tasks(task_list)
    print("Task added successfully")
# Display all tasks in a formatted way
def view_all():
    task_list = read_tasks()

    if len(task_list) == 0:
        print("No tasks found.")
        return

    print("All Tasks:")
    print("------------------------")

    for i, t in enumerate(task_list, start=1):
        print(f"Task {i}:")
        print(f"Title: {t['title']}")
        print(f"Assigned to: {t['username']}")
        print(f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Completed: {'Yes' if t['completed'] else 'No'}")
        print(f"Description:\n{t['description']}")
        print("------------------------")
# Display tasks for current user
def view_mine(curr_user):
    task_list = read_tasks()
    user_tasks = []

    for t in task_list:
        if t['username'] == curr_user:
            user_tasks.append(t)

    if len(user_tasks) == 0:
        print("No tasks found for the current user.")
        return

    print("My Tasks:")
    print("------------------------")

    for i, t in enumerate(user_tasks, start=1):
        print(f"Task {i}:")
        print(f"Title: {t['title']}")
        print(f"Assigned to: {t['username']}")
        print(f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Completed: {'Yes' if t['completed'] else 'No'}")
        print(f"Description:\n{t['description']}")
        print("------------------------")

    task_choice = input("Enter the number of the task to select it (or -1 to return to the main menu): ")
    if task_choice == '-1':
        return
    task_choice = int(task_choice) - 1
    if task_choice < 0 or task_choice >= len(user_tasks):
        print("Invalid task number. Please try again.")
        return

    selected_task = user_tasks[task_choice]

    print(f"Selected Task: Task {task_choice + 1}")
    print("------------------------")
    print(f"Title: {selected_task['title']}")
    print(f"Assigned to: {selected_task['username']}")
    print(f"Date Assigned: {selected_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Due Date: {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Completed: {'Yes' if selected_task['completed'] else 'No'}")
    print(f"Description:\n{selected_task['description']}")
    print("------------------------")

    sub_choice = input("Choose an action: 'c' to mark as complete, 'e' to edit, or 'b' to go back: ")

    if sub_choice == 'c':
        if selected_task['completed']:
            print("Task is already marked as complete.")
        else:
            selected_task['completed'] = True
            write_tasks(task_list)
            print("Task marked as complete.")

    elif sub_choice == 'e':
        if selected_task['completed']:
            print("Cannot edit a completed task.")
        else:
            edit_choice = input("Choose what to edit: 'u' to edit the assigned user, 'd' to edit the due date, or 'b' to go back: ")

            if edit_choice == 'u':
                new_username = input("Enter the new username for the task: ")
                selected_task['username'] = new_username
                write_tasks(task_list)
                print("Task username updated successfully.")
            elif edit_choice == 'd':
                while True:
                    try:
                        new_due_date = datetime.strptime(input("Enter the new due date (YYYY-MM-DD): "), DATETIME_STRING_FORMAT).date()
                        selected_task['due_date'] = new_due_date
                        write_tasks(task_list)
                        print("Task due date updated successfully.")
                        break
                    except ValueError:
                        print("Invalid date format. Please enter a valid date (YYYY-MM-DD)")
            elif edit_choice == 'b':
                return
            else:
                print("Invalid choice.")

    elif sub_choice == 'b':
        return

    else:
        print("Invalid choice.")

# Mark a task complete
def mark_task_complete():
    task_list = read_tasks()

    if len(task_list) == 0:
        print("No tasks found.")
        return

    view_all()

    task_index = int(input("Enter the task number to mark as complete: ")) - 1

    if task_index < 0 or task_index >= len(task_list):
        print("Invalid task number. Please try again.")
        return

    task = task_list[task_index]

    if task['completed']:
        print("Task is already marked as complete.")
    else:
        task['completed'] = True
        write_tasks(task_list)
        print("Task marked as complete.")
# Generate user_overview.txt and task_overview.txt report in a user friendly manner
def generate_report():
    username_password = read_users()  # get the dictionary of usernames and passwords
    total_users = len(username_password)  # get the total number of users
    task_list = read_tasks()  # get the list of tasks
    total_tasks = len(task_list)  # get the total number of tasks

    # Create user_overview.txt
    with open("user_overview.txt", "w") as user_file:
        user_file.write(f"The total number of users: {total_users}\n")
        user_file.write(f"The total number of tasks: {total_tasks}\n")

        for username in username_password:  # loop through each username
            assigned_tasks = 0  # initialize the number of assigned tasks
            completed_tasks = 0  # initialize the number of completed tasks
            uncompleted_tasks = 0  # initialize the number of uncompleted tasks
            overdue_tasks = 0  # initialize the number of overdue tasks
            today = date.today()  # get today's date

            for task in task_list:  # loop through each task
                if task["username"] == username:  # if the task is assigned to that user
                    assigned_tasks += 1  # increment the number of assigned tasks
                    if task["completed"]:  # if the task is completed
                        completed_tasks += 1  # increment the number of completed tasks
                    else:  # if the task is not completed
                        uncompleted_tasks += 1  # increment the number of uncompleted tasks
                        if task["due_date"] < today:  # if the task is overdue
                            overdue_tasks += 1  # increment the number of overdue tasks

            # calculate the percentages of different types of tasks for that user
            assigned_percentage = round(assigned_tasks / total_tasks * 100, 2)
            completed_percentage = round(completed_tasks / assigned_tasks * 100, 2) if assigned_tasks > 0 else 0
            uncompleted_percentage = round(uncompleted_tasks / assigned_tasks * 100, 2) if assigned_tasks > 0 else 0
            overdue_percentage = round(overdue_tasks / assigned_tasks * 100, 2) if assigned_tasks > 0 else 0

            # write the data for that user in the file
            user_file.write(f"\nFor user {username}:\n")
            user_file.write(f"The total number of tasks assigned: {assigned_tasks}\n")
            user_file.write(f"The percentage of the total number of tasks assigned: {assigned_percentage}%\n")
            user_file.write(f"The percentage of the tasks completed: {completed_percentage}%\n")
            user_file.write(f"The percentage of the tasks uncompleted: {uncompleted_percentage}%\n")
            user_file.write(f"The percentage of the tasks overdue: {overdue_percentage}%\n")

            # Create task_overview.txt
            completed_tasks = sum(task["completed"] for task in task_list)
            uncompleted_tasks = total_tasks - completed_tasks
            overdue_tasks = sum(task["due_date"] < date.today() and not task["completed"] for task in task_list)
            incomplete_percentage = round(uncompleted_tasks / total_tasks * 100, 2)
            overdue_percentage = round(overdue_tasks / total_tasks * 100, 2)

            with open("task_overview.txt", "w") as task_file:
                task_file.write(f"The total number of tasks: {total_tasks}\n")
                task_file.write(f"The total number of completed tasks: {completed_tasks}\n")
                task_file.write(f"The total number of uncompleted tasks: {uncompleted_tasks}\n")
                task_file.write(f"The total number of overdue tasks: {overdue_tasks}\n")
                task_file.write(f"The percentage of uncompleted tasks: {incomplete_percentage}%\n")
                task_file.write(f"The percentage of overdue tasks: {overdue_percentage}%\n")

# Display statistics of tasks
def display_statistics():
    # read from the task_overview.txt file
    with open("task_overview.txt", "r") as file:
        task_overview = file.read() # get the content as a string
    # read from the user_overview.txt file
    with open("user_overview.txt", "r") as file:
        user_overview = file.read() # get the content as a string
    # display the content in a user-friendly manner
    print("Task Overview:")
    print(task_overview)
    print("User Overview:")
    print(user_overview)
# Prompts the user to enter username and password and check if the credentials provided exists in the user.txt file
def main():
    username_password = read_users()
    while True:
        user = input("Enter your username: ")
        password = input ("Enter your password: ")
        if user in username_password and password == username_password[user]:
            print ("Login successful")
            break
        else:
            print("Invalid username or password. Please try again")
    while True:
        print("\nTask Manager Menu:")
        print("r - Register User")
        print("a - Add Task")
        print("va - View All Tasks")
        print("vm - View My Tasks")
        print("gr - Generate Reports")
        print("ds - Display Statistics")
        print("e - Exit")

        choice = input("Enter your choice: ")

        if choice == "r":
            reg_user()
        elif choice == "a":
            add_task()
        elif choice == "va":
            view_all()
        elif choice == "vm":
            username_password = read_users()
            current_user = input("Enter your username: ")

            if current_user in username_password:
                view_mine(current_user)
            else:
                print("Invalid username. Please register as a user.")

        elif choice == "m":
            mark_task_complete()
        elif choice == "gr":
            generate_report()
        elif choice == "ds":
            display_statistics()
        elif choice == "e":
            print("Exiting Task Manager...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
