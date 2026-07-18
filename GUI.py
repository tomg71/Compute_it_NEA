# This file will contain the classes needed for each page needed for the program

# Importing Tkinter and Tkinter.ttk (submodule with complex widgets)
from tkinter import *
import tkinter.ttk as ttk

# Fonts used are created here as tuples in format ("font_name", size)
title_large = ("Algerian", 35)
title_medium = ("Algerian", 28)
title_small = ("Algerian", 20)
button_font = ("Segoe UI", 18)
label_small = ("Segoe UI", 12)
label_medium = ("Segoe UI", 18)
label_large = ("Segoe UI", 21)
question_text_font = ("Segoe UI", 14)
topic_font = ("Segoe UI", 11)

# Colours used are created here as strings with hexadecimal colour codes
title_colour = "#70C1B3"
button_colour = "#247BA0"
active_colour = "#B2DBBF"
option_selected = "#999999"
default = "#F0F0F0"

# Page classes are created below
# Home page class (inherits Tk class from Tkinter, so it is created as a window)
class Home_Page(Tk):
    # command_one and command_two are functions created in main.py
    def __init__(self, command_one, command_two):
        # Initialises window using contructor of Tkinter window
        super().__init__()
        # Set title and size
        self.title("Home page")
        self.geometry("900x540")

        # Add widgets
        self.name_label = Label(self, text = "Compute|it", relief = "solid", height = 3, width = 15, font = title_large, 
            bg = title_colour, pady = 4)
        self.login_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Login", font = button_font, 
            height = 2, width = 14, command = command_one)
        self.create_account_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Create Account", 
            font = button_font, height = 2, width = 14, command = command_two)
        # self.destroy will close entire Home_Page window
        self.quit_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Quit", font = button_font, 
            height = 1, width = 10, command = self.destroy, pady = 3)
        # Display widgets with spacing between them
        self.name_label.pack(pady = 15)
        self.login_button.pack(pady = 12)
        self.create_account_button.pack(pady = 12)
        self.quit_button.pack(pady = 12)


# Create account page class
class Create_Account_Page(Tk):
    # command_one and command_two are functions defined in main.py
    def __init__(self, command_one, command_two):
        super().__init__()
        # Hide page until use
        self.withdraw()
        self.title("Create Account")
        self.geometry("900x540")

        # Add widgets
        self.name_label = Label(self, text = "Compute|it", relief = "solid", height = 3, width = 14, font = title_medium, 
            bg = title_colour, pady = 4)
        self.back_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Back", font = button_font, 
            height = 1, width = 10, command = command_one)
        self.username_label = Label(self, text = "Username: 6-25 characters", height = 1, width = 20, font = label_small)
        self.username_entry = Entry(self, relief = "solid", width = 30, font = label_small)
        self.password_label = Label(self, text = "Password: 8-25 characters, use of at least 1 number", height = 1, width = 40, 
            font = label_small)
        # password_entry will show asterisks instead of characters typed by user
        self.password_entry = Entry(self, relief = "solid", width = 30, font = label_small, show = "*")
        self.attempt_result_label = Label(self, text = "", height = 1, width = 40, font = label_medium)
        self.attempt_create_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Submit", 
            font = button_font, height = 1, width = 14, pady = 5, command = command_two)
        
        # Display widgets in grid (padx and pady are used to position widgets in line with each other)
        self.name_label.grid(row = 0, column = 1, padx = 100, pady = 5)
        self.back_button.grid(row = 0, column = 0, padx = 20, pady = (4, 30))
        self.username_label.grid(row = 1, column = 1, pady = (35, 5), padx = (0, 100))
        self.username_entry.grid(row = 2, column = 1, padx = (0, 30))
        self.password_label.grid(row = 3, column = 1, pady = (35, 5), padx = (65, 0))
        self.password_entry.grid(row = 4, column = 1, padx = (0, 30))
        self.attempt_result_label.grid(row = 5, column = 1, pady = 30)
        self.attempt_create_button.grid(row = 6, column = 1)


# Login page class
class Login_Page(Tk):
    def __init__(self, command_one, command_two):
        super().__init__()
        # Hide page until use
        self.withdraw()
        self.title("Login")
        self.geometry("900x540")

        # Add widgets
        self.name_label = Label(self, text = "Compute|it", relief = "solid", height = 3, width = 14, font = title_medium, 
            bg = title_colour, pady = 4)
        self.back_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Back", font = button_font, 
            height = 1, width = 10, command = command_one)
        self.username_label = Label(self, text = "Username:", height = 1, width = 20, font = label_small)
        self.username_entry = Entry(self, relief = "solid", width = 30, font = label_small)
        self.password_label = Label(self, text = "Password:", height = 1, width = 40, font = label_small)
        # password_entry will show asterisks instead of characters typed by user
        self.password_entry = Entry(self, relief = "solid", width = 30, font = label_small, show = "*")
        self.login_result_label = Label(self, text = "", height = 1, width = 40, font = label_medium)
        self.attempt_login_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Login", 
            font = button_font, height = 2, width = 14, command = command_two)
        
        # Display widgets in grid (padx and pady are used to position widgets in line with each other when needed)
        self.name_label.grid(row = 0, column = 1, padx = 100, pady = 5)
        self.back_button.grid(row = 0, column = 0, padx = 20, pady = (4, 30))
        self.username_label.grid(row = 1, column = 1, pady = (35, 5), padx = (0, 220))
        self.username_entry.grid(row = 2, column = 1, padx = (0, 30))
        self.password_label.grid(row = 3, column = 1, pady = (35, 5), padx = (0, 220))
        self.password_entry.grid(row = 4, column = 1, padx = (0, 30))
        self.login_result_label.grid(row = 5, column = 1, pady = 30)
        self.attempt_login_button.grid(row = 6, column = 1)


# Dashboard page class
class Dashboard(Tk):
    def __init__(self, command_one, command_two):
        super().__init__()
        # Hide page until use
        self.withdraw()
        self.title("Dasboard")
        self.geometry("900x540")

        # Add standard widgets (not in a frame)
        self.name_label = Label(self, text = "Compute|it", relief = "solid", height = 2, width = 14, font = title_small, 
            bg = title_colour, pady = 3)
        self.logout_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Logout", 
            font = button_font, height = 1, width = 10, command = command_one)
        self.start_session_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Start session", 
            font = button_font, height = 1, width = 14, pady = 2, command = command_two)
        # anchor="w" sets text to left side
        self.accuracy_label = Label(self, text = "Accuracy: ", height = 1, width = 15, font = label_medium, anchor = "w")
        # Use progressbar widget as part of tkinter.ttk library
        self.accuracy_bar = ttk.Progressbar(self, orient = HORIZONTAL, length = 200, value = 100)

        # Use multiple frames to outline multiple labels (for best/worst topics and milestones sidebar)
        # Frame for 'sidebar'
        self.sidebar_frame = Frame(self, bd = 1, relief = "solid")
        self.username_label = Label(self.sidebar_frame, relief = "solid", bd = 1, text = "", height = 2, width = 26, 
            font = label_small, padx = 5, pady = 10)
        self.milestones_label = Label(self.sidebar_frame, text = "Milestones:", height = 2, width = 15, font = label_medium, 
            anchor = "w")
        self.milestone_one = Label(self.sidebar_frame, text = "", height = 2, width = 15, font = label_medium)
        self.milestone_two = Label(self.sidebar_frame, text = "", height = 2, width = 15, font = label_medium)
        self.milestone_three = Label(self.sidebar_frame, text = "", height = 2, width = 15, font = label_medium)
        self.username_label.grid(row = 0, column = 0, pady = (0, 25))
        self.milestones_label.grid(row = 1, column = 0, pady = 20)
        self.milestone_one.grid(row = 2, column = 0, pady = 15)
        self.milestone_two.grid(row = 3, column = 0, pady = 15)
        self.milestone_three.grid(row = 4, column = 0, pady = (15, 50))

        # Frame for best topics
        self.best_topics_frame = Frame(self, bd = 1, relief = "solid")
        self.best_topics_label = Label(self.best_topics_frame, text = "Best topics:", height = 1, width = 15, font = label_medium)
        self.best_topic_one = Label(self.best_topics_frame, text = " -", height = 1, width = 30, font = label_small, anchor = "w", 
            pady = 5)
        self.best_topic_two = Label(self.best_topics_frame, text = " -", height = 1, width = 30, font = label_small, anchor = "w", 
            pady = 5)
        self.best_topic_three = Label(self.best_topics_frame, text = " -", height = 1, width = 30, font = label_small, anchor = "w", 
            pady = 5)
        self.best_topics_label.grid(row = 0, column = 0, pady = 18)
        self.best_topic_one.grid(row = 1, column = 0, pady = 12)
        self.best_topic_two.grid(row = 2, column = 0, pady = 12)
        self.best_topic_three.grid(row = 3, column = 0, pady = (12, 20))

        # Frame for topics to improve
        self.topics_to_improve_frame = Frame(self, bd = 1, relief = "solid")
        self.topics_to_improve_label = Label(self.topics_to_improve_frame, text = "Topics to improve:", height = 1, width = 15, 
            font = label_medium)
        self.topic_to_improve_one = Label(self.topics_to_improve_frame, text = " -", height = 1, width = 30, font = label_small, 
            anchor = "w", pady = 5)
        self.topic_to_improve_two = Label(self.topics_to_improve_frame, text = " -", height = 1, width = 30, font = label_small, 
            anchor = "w", pady = 5)
        self.topic_to_improve_three = Label(self.topics_to_improve_frame, text = " -", height = 1, width = 30, font = label_small, 
            anchor = "w", pady = 5)
        self.topics_to_improve_label.grid(row = 0, column = 0, pady = 18)
        self.topic_to_improve_one.grid(row = 1, column = 0, pady = 12)
        self.topic_to_improve_two.grid(row = 2, column = 0, pady = 12)
        self.topic_to_improve_three.grid(row = 3, column = 0, pady = (12, 20))

        # Display widgets using grid (including frames containing other widgets)
        self.name_label.grid(row = 0, column = 1, padx = 60, pady = 4)
        self.logout_button.grid(row = 0, column = 0, pady = 10)
        self.sidebar_frame.grid(row = 0, column = 2, rowspan = 4, pady = (0, 20))
        self.best_topics_frame.grid(row = 1, column = 0, pady = 35, padx = (20, 0))
        self.topics_to_improve_frame.grid(row = 1, column = 1, pady = 35)
        self.start_session_button.grid(row = 3, column = 1, pady = (5, 15))
        self.accuracy_label.grid(row = 2, column = 0, padx = (0, 30))
        self.accuracy_bar.grid(row = 3, column = 0)


# Start session page class
class Start_Session_Page(Tk):
    # topics is a list of topic names taken from the main program
    def __init__(self, command_one, command_two, topics):
        super().__init__()
        # Hide page until use
        self.withdraw()
        self.title("Start session")
        self.geometry("900x540")

        # Add widgets not in a frame
        self.name_label = Label(self, text = "Compute|it", relief = "solid", height = 2, width = 14, font = title_small, 
            bg = title_colour, pady = 5)
        self.back_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Back", font = button_font, 
            height = 1, width = 8, command = command_one)
        self.zero_topics_selected_label = Label(self, text = "", height = 1, width = 30, font = label_small)
        self.start_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Start", font = button_font, 
            height = 1, width = 10, command = command_two)
        
        # Use frame for checkbox grid 
        self.checkbox_frame = Frame(self, bd = 1, relief = "solid")
        # Dictionary to keep topic names and chosen state
        self.checkbox_vars = {}
        # Variables to track row/column for checkbox grid
        self.column_count = 0
        self.row_count = 0

        # Loop used to create 30 checkboxes
        for index in range(0, 30):
            self.state_var = BooleanVar(self.checkbox_frame)
            # text for checkbox taken from topics list, state of checkbox stored as a BooleanVar
            self.checkbox = Checkbutton(self.checkbox_frame, text = topics[index], font = topic_font, anchor = "w", width = 30, 
                variable = self.state_var)
            self.checkbox.grid(row = self.row_count, column = self.column_count, pady = 2, padx = 12, sticky = "w")
            # Store index and state in dictionary
            self.checkbox_vars[topics[index]] = self.state_var
            # Used to keep track of rows columns (10 columns, 3 rows)
            self.row_count += 1
            if self.row_count == 10:
                self.row_count = 0
                self.column_count += 1

        # Display widgets using grid method
        self.name_label.grid(row = 0, column = 1, padx = (0, 120), pady = 4)
        self.back_button.grid(row = 0, column = 0, pady = 10)
        self.checkbox_frame.grid(row = 1, column = 0, columnspan = 3, padx = 12, pady = 10)
        self.zero_topics_selected_label.grid(row = 2, column = 1, padx = (0, 120))
        self.start_button.grid(row = 3, column = 1, padx = (0, 120))


# Classes for questions pages: multiple choice (including grid) and written (including multiline entry)
class MC_Question_Page(Tk):
    def __init__(self, command_one, command_two, command_three):
        super().__init__()
        # Hide page until use
        self.withdraw()
        self.title("Question")
        self.geometry("900x540")

        # Create widgets outside of any frames
        self.end_session_button = Button(self, activebackground = button_colour, bg = active_colour, text = "End session", 
            font = button_font, height = 1, width = 13, command = command_one)
        self.name_label = Label(self, text = "Compute|it", relief = "solid", height = 2, width = 14, font = title_small, 
            bg = title_colour)
        self.question_number = Label(self, text = "", relief = "solid", bd = 1, height = 1, width = 4, font = label_medium, pady = 2)
        self.question_correct_label = Label(self, text = "", height = 1, width = 25, font = label_medium)
        self.explain_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Explain", 
            font = button_font, height = 1, width = 10, pady = 3, command = command_three)
        self.submit_answer_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Submit", 
            font = button_font, height = 1, width = 15, pady = 3, command = command_two)

        # Frame for question and options
        self.question_options_frame = Frame(self)
        # Label for question text
        self.question_text_label = Label(self.question_options_frame, text = "", relief = "solid", bd = 1, height = 4, width = 60, 
            pady = 5, font = question_text_font)
        self.question_text_label.grid(row = 0, column = 0, columnspan = 2)
        # list to store individual radiobuttons
        self.options = []
        # This will the store the radiobutton selected("1"->"4") or "0" if no button is selected
        self.option_chosen = StringVar(self.question_options_frame, "0")
        self.option_row = 1
        self.option_column = 0
        # Create 4 radiobuttons
        for i in range(1, 5):
            self.question_option = Radiobutton(self.question_options_frame, text = "", relief = "solid", bd = 1, height = 4, width = 35,
                font = label_small, anchor = "w", indicator = 0, variable = self.option_chosen, value = i, justify = "left", 
                selectcolor = option_selected)
            self.question_option.grid(row = self.option_row, column = self.option_column, pady = 5)
            # Add radiobutton to options list
            self.options.append(self.question_option)
            # Update colums/rows (2 columns, 2 rows)
            self.option_column += 1
            if self.option_column == 2:
                self.option_column = 0
                self.option_row += 1

        # Frame for 'sidebar'
        self.sidebar_frame = Frame(self, relief = "solid", bd = 1)
        self.username_label = Label(self.sidebar_frame, relief = "solid", bd = 1, text = "", height = 2, width = 24, font = topic_font, 
            pady = 10)
        # "\n" used to split text over two lines
        self.questions_answered = Label(self.sidebar_frame, text = "Questions\nanswered:", height = 2, width = 10, font = label_medium, 
            pady=10)
        self.no_questions_answered = Label(self.sidebar_frame, text = "", height = 2, width = 3, font = label_large, pady=12)
        self.questions_correct = Label(self.sidebar_frame, text = "Questions\ncorrect:", height = 2, width = 10, font = label_medium, 
            pady=10)
        self.no_questions_correct = Label(self.sidebar_frame, text = "", height = 2, width = 3, font = label_large, pady = 12)
        self.accuracy_label = Label(self.sidebar_frame, text = "Accuracy: ", height = 1, width = 15, font = label_medium, pady = 6)
        self.accuracy_bar = ttk.Progressbar(self.sidebar_frame, orient = HORIZONTAL, length = 180, value = 100)
        self.username_label.grid(row = 0, column = 0, columnspan = 2, pady = (0, 40))
        self.questions_answered.grid(row = 1, column = 0, pady = 20)
        self.no_questions_answered.grid(row = 1, column = 1, pady = 20)
        self.questions_correct.grid(row = 2, column = 0, pady = 20)
        self.no_questions_correct.grid(row = 2, column = 1, pady = 20)
        self.accuracy_label.grid(row = 3, column = 0, columnspan = 2, pady = 20)
        self.accuracy_bar.grid(row = 4, column = 0, columnspan = 2, pady = 20)
        
        # Display widgets in grid (including frames)
        self.end_session_button.grid(row = 0, column = 0, pady = 10)
        self.name_label.grid(row = 0, column = 1)
        self.question_number.grid(row = 0, column = 2)
        self.question_options_frame.grid(row = 1, column = 0, columnspan = 3, padx = 20)
        self.question_correct_label.grid(row = 2, column = 0, columnspan = 3, pady = 10)
        self.explain_button.grid(row = 3, column = 0)
        self.submit_answer_button.grid(row = 3, column = 1, padx = (0, 60))
        self.sidebar_frame.grid(row = 0, column = 3, rowspan = 4)


class Written_Question_Page(Tk):
    def __init__(self, command_one, command_two, command_three):
        super().__init__()
        # Hide page until use
        self.withdraw()
        self.title("Question")
        self.geometry("900x540")
        
        # Create widgets outside of frame
        self.end_session_button = Button(self, activebackground = button_colour, bg = active_colour, text = "End session", 
            font = button_font, height = 1, width = 13, command = command_one)
        self.name_label = Label(self, text = "Compute|it", relief = "solid", height = 2, width = 14, font = title_small, 
            bg = title_colour)
        self.question_number = Label(self, text = "", relief = "solid", bd = 1, height = 1, width = 4, font = label_medium, pady = 2)
        self.question_text_label = Label(self, text = "", relief = "solid", bd = 1, height = 5, width = 60, pady = 8, 
            font = question_text_font)
        # use advanced text entry (multiline) for answer input
        self.user_question_answer = Text(self, font = label_small, height = 3, width = 60, pady = 8, padx = 8)
        self.question_status_label = Label(self, text = "", height = 5, width = 60, font = label_small)
        self.explain_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Explain", 
            font = button_font, height = 1, width = 10, pady = 3, command = command_three)
        self.submit_answer_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Submit", 
            font = button_font, height = 1, width = 15, pady = 3, command = command_two)
        
        # Frame for 'sidebar'
        self.sidebar_frame = Frame(self, relief = "solid", bd = 1)
        self.username_label = Label(self.sidebar_frame, relief = "solid", bd = 1, text = "", height = 2, width = 24, font = topic_font, 
            pady = 10)
        # "\n" used to split text over two lines
        self.questions_answered = Label(self.sidebar_frame, text = "Questions\nanswered:", height = 2, width = 10, font = label_medium, 
            pady=10)
        self.no_questions_answered = Label(self.sidebar_frame, text = "", height = 2, width = 3, font = label_large, pady=12)
        self.questions_correct = Label(self.sidebar_frame, text = "Questions\ncorrect:", height = 2, width = 10, font = label_medium, 
            pady=10)
        self.no_questions_correct = Label(self.sidebar_frame, text = "", height = 2, width = 3, font = label_large, pady = 12)
        self.accuracy_label = Label(self.sidebar_frame, text = "Accuracy: ", height = 1, width = 15, font = label_medium, pady = 6)
        self.accuracy_bar = ttk.Progressbar(self.sidebar_frame, orient = HORIZONTAL, length = 180, value = 100)
        self.username_label.grid(row = 0, column = 0, columnspan = 2, pady = (0, 40))
        self.questions_answered.grid(row = 1, column = 0, pady = 20)
        self.no_questions_answered.grid(row = 1, column = 1, pady = 20)
        self.questions_correct.grid(row = 2, column = 0, pady = 20)
        self.no_questions_correct.grid(row = 2, column = 1, pady = 20)
        self.accuracy_label.grid(row = 3, column = 0, columnspan = 2, pady = 20)
        self.accuracy_bar.grid(row = 4, column = 0, columnspan = 2, pady = 18)

        # Display widgets and 'sidebar' frame
        self.end_session_button.grid(row = 0, column = 0, pady = 10)
        self.name_label.grid(row = 0, column = 1)
        self.question_number.grid(row = 0, column = 2)
        self.question_text_label.grid(row = 1, column = 0, columnspan = 3, pady = 10, padx = 5)
        self.user_question_answer.grid(row = 2, column = 0, columnspan = 3, pady = 10)
        self.question_status_label.grid(row = 3, column = 0, columnspan = 3, pady = 10)
        self.explain_button.grid(row = 4, column = 0)
        self.submit_answer_button.grid(row = 4, column = 1, padx = (0, 60))
        self.sidebar_frame.grid(row = 0, column = 3, rowspan = 5, padx = (20, 0))


# Class for end session page: displays details about finished session
class End_Session_Page(Tk):
    def __init__(self, command_one):
        super().__init__()
        # Hide page until use
        self.withdraw()
        self.title("End session")
        self.geometry("900x540")

        # Create widgets
        self.back_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Back to\ndashboard", 
            font = question_text_font, height = 2, width = 13, pady = 3, command = command_one)
        self.name_label = Label(self, text = "Compute|it", relief = "solid", height = 2, width = 14, font = title_small, 
            bg = title_colour)
        self.username_label = Label(self, relief = "solid", bd = 1, text = "", height = 2, width = 26, font = topic_font, 
            pady = 10)
        self.questions_answered = Label(self, text = "Questions\nanswered:", font = label_medium, height = 2, width = 12)
        self.no_questions_answered = Label(self, relief = "solid", bd = 1, text = "", font = label_medium, height = 1, 
            width = 5, pady = 5)
        self.questions_correct = Label(self, text = "Questions\ncorrect:", font = label_medium, height = 2, width = 12)
        self.no_questions_correct = Label(self, relief = "solid", bd = 1, text = "", font = label_medium, height = 1, 
            width = 5, pady = 5)
        self.accuracy_label = Label(self, text = "Accuracy:", font = label_medium, height = 2, width = 12)
        self.no_accuracy_label = Label(self, relief = "solid", bd = 1, text = "", font = label_medium, height = 1, 
            width = 5, pady = 5)
        self.accuracy_bar = ttk.Progressbar(self, orient = HORIZONTAL, length = 200, value = 100)
        self.session_time_label = Label(self, text = "Session time: ", font = label_medium, height = 1, width = 20)
        
        # Display widgets in grid
        self.back_button.grid(row = 0, column = 0, pady = 20, padx = (20, 40))
        self.name_label.grid(row = 0, column = 1, pady = 10, padx = (45, 25))
        self.username_label.grid(row = 0, column = 3, pady = (0, 40), padx = (100, 0))
        self.questions_answered.grid(row = 1, column = 1, pady = 15)
        self.no_questions_answered.grid(row = 1, column = 2, pady = 15)
        self.questions_correct.grid(row = 2, column = 1, pady = 15)
        self.no_questions_correct.grid(row = 2, column = 2, pady = 15)
        self.accuracy_label.grid(row = 3, column = 1, pady = 15)
        self.no_accuracy_label.grid(row = 3, column = 2, pady = 15)
        self.accuracy_bar.grid(row = 4, column = 1, columnspan = 2, pady = 10)
        self.session_time_label.grid(row = 5, column = 1, pady = 10)


# Window used for question explanation
class Question_Explanation_Window(Tk):
    def __init__(self):
        super().__init__()
        # Hide page until use
        self.withdraw()
        self.title("Question explanation")
        self.geometry("900x600")

        # Create any labels used
        self.question_label = Label(self, text = "", font = label_medium, height = 2, width = 60, relief = "solid", bd = 1)
        self.question_explanation = Label(self, text = "", font = label_small, height = 22, width = 120, anchor = "n", justify = "left")
        self.back_button = Button(self, activebackground = button_colour, bg = active_colour, text = "Back", 
            font = question_text_font, height = 1, width = 8, pady = 1, command = self.withdraw)
        
        # Display any labels used using pack function
        self.question_label.pack()
        self.question_explanation.pack()
        self.back_button.pack()