# Main code
# Import other python files to main
import database_connection as DB_actions
from queue_function import Queue
import GUI

# Import time module for use as part of login process
import time
import math
import random

# Import PasswordHasher from argon2 module for hashing use
from argon2 import PasswordHasher

# hasher object created here for use in other functions
hasher = PasswordHasher()

# Import google genai module for use in question explanation
from google import genai

# Client used for question explanation (api key should be hidden)
client = genai.Client(api_key = "AIzaSyCru3pgG9AKqEI6hsq0EU6a0sXZqy0aXjQ")

# Values used in more than 1 function are stored here in a data structure
current_username = []
current_topics_selected = []
current_question_count = [0]
current_questionID = [0]
current_session_results = {"Answered": 0, "Correct": 0}
recent_session_results = Queue()
current_user_milestones = {"Questions answered": 0, "Questions answered in row": 0}
session_times = [0, 0]

# Function to unpack lists with tuples inside into normal list (utility function)
def unpack_list(input_list):
    output_list = []
    # Iterate through each tuple in the input list
    for tuple in input_list:
        # Append the item inside each tuple to the list
        output_list.append(tuple[0])
    return output_list


# Functions used to change page
def home_to_login():
    '''Withdraw home page, display login page'''
    home_page.withdraw()
    login_page.deiconify()
    # Clear text from login_result_label
    login_page.login_result_label.config(text = "")
    # Remove all text in entry boxes
    login_page.username_entry.delete(0, GUI.END)
    login_page.password_entry.delete(0, GUI.END)
    # Set attempt_login_button's state to active
    login_page.attempt_login_button.config(state = "active")

def home_to_create_account():
    '''Withdraw home page, display create account page'''
    home_page.withdraw()
    create_account_page.deiconify()
    # Clear label and entry boxes
    create_account_page.attempt_result_label.config(text = "")
    create_account_page.username_entry.delete(0, GUI.END)
    create_account_page.password_entry.delete(0, GUI.END)

def login_to_home():
    '''Withdraw login page, display home page'''
    login_page.withdraw()
    home_page.deiconify()

def create_account_to_home():
    '''Withdraw create account page, display home page'''
    create_account_page.withdraw()
    home_page.deiconify()
    # Return button to allowing for account creation attempts
    create_account_page.attempt_create_button.config(text = "Submit", command = create_account_attempt)

def create_account_to_login():
    '''Withdraw create account page, display login page'''
    create_account_page.withdraw()
    login_page.deiconify()
    # Clear labels and entry boxes
    login_page.login_result_label.config(text = "")
    login_page.username_entry.delete(0, GUI.END)
    login_page.password_entry.delete(0, GUI.END)
    # Set buttons to active
    login_page.attempt_login_button.config(state = "active")

def login_to_dashboard():
    '''Withdraw login page, display dashboard page'''
    login_page.withdraw()
    dashboard.deiconify()
    # Call set_dashboard function, which will add user-specific information
    set_dashboard(current_username[0])

def dashboard_to_home():
    '''Withdraw dashboard page, display home page'''
    dashboard.withdraw()
    home_page.deiconify()
    # Remove username from current_username list (as user has logged out) and remove milstones
    current_username.pop()
    current_user_milestones["Questions answered"] = 0
    current_user_milestones["Questions answered in row"] = 0

def dashboard_to_start_session():
    '''Withdraw dashboard page, display start session page'''
    dashboard.withdraw()
    start_session_page.deiconify()
    # Iterate through each checkbox state and set it to false (so no checkboxes are selected when starting)
    for var in start_session_page.checkbox_vars.values():
        var.set(False)

def start_session_to_dashboard():
    '''Withdraw start session page, display dashboard page'''
    start_session_page.withdraw()
    dashboard.deiconify()
    start_session_page.zero_topics_selected_label.config(text = "")
    # Call set_dashboard function
    set_dashboard(current_username[0])

def end_session_to_dashboard():
    '''Withdraw end session page, display dashboard'''
    end_session_page.withdraw()
    dashboard.deiconify()
    set_dashboard(current_username[0])


# Main function related to creating an account
def create_account_attempt():
    attempt_is_fail = False
    # Temporary disable button to create account
    create_account_page.attempt_create_button.config(state = "disabled")
    # Get username and password from their labels
    username_provided = create_account_page.username_entry.get()
    password_provided = create_account_page.password_entry.get()
    # Check is username, password are valid
    if not validate_password(password_provided):
        attempt_is_fail = True
    if not validate_username(username_provided):
        attempt_is_fail = True
    # Only attempt to create record is username and password are valid
    if attempt_is_fail == False:
        # use hash method to create password hash
        password_hash = hasher.hash(password_provided)
        try:
            DB_actions.insert_new_user(username_provided, password_hash)
            userID = DB_actions.retrieve_userID(username_provided)
            topicIDs = []
            # use list of numbers 1->30 to add record to topic_results for each topic
            for topicID in range (1, 31):
                topicIDs.append(topicID)
            DB_actions.new_user_records(userID, topicIDs)
            # Display message and change button function to allow for user to go to login page
            create_account_page.attempt_result_label.config(text = "Account creation successful, proceed to login")
            create_account_page.attempt_create_button.config(text = "Go to Login", command = create_account_to_login)
        # If non-unique username is entered:
        except DB_actions.sqlite3.IntegrityError:
            create_account_page.attempt_result_label.config(text = "Username used is already taken")
    # Re-activate button
    create_account_page.attempt_create_button.config(state = "active")
        
def validate_username(username):
    #Return True if length of username if between 6-25, otherwise return False
    # Display message if username is too long/short
    if len(username) > 25 or len(username) < 6:
        create_account_page.attempt_result_label.config(text = "Username must be 6-25 characters long")
        return False
    return True

def validate_password(password):
    #Return True if password is between 8-25 characters and contains a number
    if len(password) > 25 or len(password) < 8:
        create_account_page.attempt_result_label.config(text = "Password must be 8-25 characters long")
        return False
    else:
        # Check for at least 1 numerical digit in the password
        numerical_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        number_present = False
        for character in password:
            if character in numerical_digits:
                number_present = True
        # Display message to user if no number in password
        if not number_present:
            create_account_page.attempt_result_label.config(text = "Password must contain at least 1 number")
            return False
        else:
            return True


def login_attempt():
    # Temporary disables login button
    login_page.attempt_login_button.config(state = "disabled")
    # Get username and password inputted from labels
    username_provided = login_page.username_entry.get()
    password_provided = login_page.password_entry.get()
    # Gets login_time as an epoch value
    login_time = time.time()
    # Retrieves password_hash stored in user_details table
    stored_hash = DB_actions.retrieve_password_hash(username_provided)
    if stored_hash == "no entries found":
        login_page.login_result_label.config(text = "This username does not exist")
        login_page.attempt_login_button.config(state = "active")
    # compare lock_until time in user_detais to login_time
    elif DB_actions.get_lock_until(username_provided) > login_time:
        # If lock_until time is greater than login_time then lock account
        # Find the rounded up number of minutes the account is locked for
        account_locked_until = math.ceil((DB_actions.get_lock_until(username_provided) - login_time) / 60)
        account_locked_message = "This account is locked for " + str(account_locked_until) + " minutes"
        login_page.login_result_label.config(text = account_locked_message)
        login_page.attempt_login_button.config(state = "active")
    else:
        if password_hashes_match(password_provided, stored_hash):
            # Reset failed attempts and lock until time for a user if they login successfully
            DB_actions.reset_failed_attempts(username_provided)
            # Add username to current_username list
            current_username.append(username_provided)
            # Take user to dashboard page
            login_to_dashboard()
        else:
            login_page.login_result_label.config(text = "Password is incorrect")
            login_page.attempt_login_button.config(state = "active")
            # Call function to change failed attempts and lock until time for user
            failed_login(username_provided)

def password_hashes_match(password_provided, stored_hash):
    # verify method causes exception if password entered is incorrect
    try:
        hasher.verify(stored_hash, password_provided)
        # Return True if no error occurs
        return True
    except:
        return False

def failed_login(username):
    # Increment failed_attempts field in user_details table
    DB_actions.change_failed_attempts(DB_actions.get_failed_attempts(username) + 1, username)
    user_failed_attempts = DB_actions.get_failed_attempts(username)
    if user_failed_attempts >= 3:
        # Calculate time for account to be locked if 3 or more failed login attempts in a row
        lock_until_time = 10 * (2 ** (user_failed_attempts - 3))
        # Update lock_until field in table
        DB_actions.change_lock_until((lock_until_time * 60) + time.time(), username)
        # Display message with how long the account is locked for
        login_fail_text = "Login failed, account locked for " + str(lock_until_time) + " minutes"
        login_page.login_result_label.config(text = login_fail_text)


def set_dashboard(username):
    # Display username is top right corner label
    dashboard.username_label.config(text = username)
    # Get userID from username
    userID = DB_actions.retrieve_userID(username)
    # Get details of the strongest, weakest topics of a user using get_dashboard details
    best_topics = DB_actions.get_dashboard_details("Highest", userID)
    topics_to_improve = DB_actions.get_dashboard_details("Lowest", userID)
    # Set 3 strongest, weakest topics using loop at separate functions
    for index in range(0, 3):
        set_best_topic(best_topics, index)
        set_topics_to_improve(topics_to_improve, index)
    # Call function to set overall accuracy
    set_overall_accuracy(userID)
    set_dashboard_milestones(userID)

def set_best_topic(best_topics, index):
    # If no questions have been answered on a topic display 'n/a' instead of a percentage
    if best_topics[index][2] == 0:
        text_to_display = "- " + best_topics[index][0] + ": n/a"
    # Otherwise display in form '- topic_name: %' where percentage is rounded to 1dp
    else:
        text_to_display = "- " + best_topics[index][0] + ": " + str(round(best_topics[index][1] * 100, 1)) + "%"
    # Display on correct label depending on index parameter (0 -> 1, 1 -> 2, ..)
    if index == 0:
        dashboard.best_topic_one.config(text = text_to_display)
    elif index == 1:
        dashboard.best_topic_two.config(text = text_to_display)
    else:
        dashboard.best_topic_three.config(text = text_to_display)

def set_topics_to_improve(topics_to_improve, index):
    # If no questions have been answered on a topic display 'n/a' instead of a percentage
    if topics_to_improve[index][2] == 0:
        text_to_display = "- " + topics_to_improve[index][0] + ": n/a"
    # Otherwise display in form '- topic_name: %' where percentage is rounded to 1dp
    else:
        text_to_display = "- " + topics_to_improve[index][0] + ": " + str(round(topics_to_improve[index][1] * 100, 1)) + "%"
    # Display on correct label depending on index parameter like in set_best_topic subroutine
    if index == 0:
        dashboard.topic_to_improve_one.config(text = text_to_display)
    elif index == 1:
        dashboard.topic_to_improve_two.config(text = text_to_display)
    else:
        dashboard.topic_to_improve_three.config(text = text_to_display)

def set_overall_accuracy(userID):
    # Get list of accuracy, questions_answered for each topic
    topic_accuracys = DB_actions.get_accuracy_details(userID)
    # Initially set questions_correct to 0
    questions_correct = 0
    for topic in topic_accuracys:
        # Find questions correct for each topic by multipling questions answered by accuracy, then add it to a total
        questions_correct += topic[0] * topic[1]
    # Get overall questions answered for a user
    questions_answered = DB_actions.no_of_questions_answered(userID)
    # Display accuracy as n/a with 'generic' progressbar amount if no questions have been answered to prevent dividing by 0
    if questions_answered == 0:
        accuracy = "Accuracy: n/a"
        dashboard.accuracy_label.config(text = accuracy)
        # 70% set as 'default' value before any questions are answered.
        dashboard.accuracy_bar.configure(value = 70)
    # Otherwise find overall accuracy as a percentage rounded to 2dp and fill accuracy bar to correct amount
    else:
        accuracy_percent = round((questions_correct / questions_answered) * 100, 2)
        accuracy = "Accuracy: " + str(accuracy_percent) + "%"
        dashboard.accuracy_label.config(text = accuracy)
        dashboard.accuracy_bar.configure(value = accuracy_percent)


def set_dashboard_milestones(userID):
    milestones_to_check = [10, 50, 100, 500, 1000, 5000]
    # Call function in DB_actions to get number of questions answered by the user
    user_questions_answered = DB_actions.no_of_questions_answered(userID)
    best_number = 0
    # Compare questions answered by user with set milestones
    for number in milestones_to_check:
        if user_questions_answered >= number:
            best_number = number
    # Add biggest questions answered milestone to dictionary
    current_user_milestones["Questions answered"] = best_number
    text_to_display = str(best_number) + " questions\nanswered"
    # Only do not display milestone if no milestones have been reached
    if best_number != 0:
        dashboard.milestone_one.config(text = text_to_display)
    else:
        dashboard.milestone_one.config(text = "")
    # Check longest user session in database and display if not 0 minutes
    longest_session = DB_actions.get_longest_session(current_username[0])
    if longest_session != 0:
        # Use '\n' to display over multiple lines
        text_to_display = "Longest session:\n" + str(int(longest_session)) + " mins"
        dashboard.milestone_two.config(text = text_to_display)
    else:
        dashboard.milestone_two.config(text = "")
    # Display number of questions correct in a row
    if current_user_milestones["Questions answered in row"] != 0:
        text_to_display = "Questions correct \nin a row: " + str(current_user_milestones["Questions answered in row"])
        dashboard.milestone_three.config(text = text_to_display)
    else:
        # Display as blank
        dashboard.milestone_three.config(text = "")


def get_topics():
    # Clear overall topics selected list
    current_topics_selected.clear()
    # Use count to track topicID looking at
    count = 1
    for checkbox_state in start_session_page.checkbox_vars.values():
        # Get BooleanVar for each topic
        topic_chosen = checkbox_state.get()
        if topic_chosen:
            # Add any selected topics to list
            current_topics_selected.append(count)
        # Increment count
        count += 1
    # Call check_topics_selected
    check_topics_selected()

def check_topics_selected():
    # Reset label on start session page
    start_session_page.zero_topics_selected_label.config(text = "")
    # Check to make sure at least 1 topic is selected.
    if len(current_topics_selected) == 0:
        start_session_page.zero_topics_selected_label.config(text = "You must select at least one topic")
    else:
        # Otherwise start a session by setting current_question_count to 0 and calling choose_next_topic
        current_question_count[0] = 0
        choose_next_topic()
        # Get and store epoch time for start of session
        session_times[0] = time.time()


def choose_next_topic():
    # If only 1 topic is selected, choose that topic without running algorithm
    if len(current_topics_selected) == 1:
        next_question_topic = current_topics_selected[0]
    else:
        userID = DB_actions.retrieve_userID(current_username[0])
        possible_topics = []
        total_contribution = 0
        for topicID in current_topics_selected:
            topic_accuracy = DB_actions.get_accuracy(userID, topicID)
            questions_for_topic = DB_actions.num_of_questions(topicID)
            # If accuracy for topic is 0.2 or less, use line below to calculate 'contribution'
            if topic_accuracy <= 0.2:
                topic_contribution = round(questions_for_topic / (0.2 ** 2), 3)
            # Otherwise use same calculation with topic_accuracy replacing 0.2
            else:
                topic_contribution = round(questions_for_topic / (topic_accuracy ** 2), 3)
            # Add topic_contribution to total_contribution
            total_contribution += topic_contribution
            # Append tuple with topicID and cumulative contribution to list
            possible_topics.append((topicID, total_contribution))
        # Generate random float value between 0 to the value of total_contribution at end of list
        topic_value = random.uniform(0, total_contribution)
        topic_found = False
        index = 0
        while topic_found == False:
            # If value generated less than cumulative value in list, the topic associated with that cumulative value is chosen
            if topic_value <= possible_topics[index][1]:
                next_question_topic = possible_topics[index][0]
                topic_found = True
            # Otherwise increment to next value is list
            else:
                index += 1
    # Call choose_question_type to decide the type of the next question based on the user's accuracy for the topic
    choose_question_type(next_question_topic)

def choose_question_type(topicID):
    # Withdraw start_session page
    start_session_page.withdraw()
    userID = DB_actions.retrieve_userID(current_username[0])
    # Get user accuracy for the topic chosen previously
    topic_accuracy = DB_actions.get_accuracy(userID, topicID)
    # This acts as a partial random 'modifier' to allow both question types to be used for accuries between 0.6->0.8
    change_accuracy_value = (random.randint(-10, 10)) / 100
    topic_accuracy_used = topic_accuracy + change_accuracy_value
    if topic_accuracy_used > 0.7:
        # Call choose_question function with topicID and type
        choose_question(topicID, "WRITTEN")
        # Add username to corner of mutliple choice question label
        written_question_page.username_label.config(text = current_username[0])
    else:
        # Call choose_question function with topicID and type
        choose_question(topicID, "MCQ")
        mc_question_page.username_label.config(text = current_username[0])

def choose_question(topicID, question_type):
    # Call DB_actions function get_possible question to get list of questionIDs
    possible_questions = DB_actions.get_possible_questions(topicID, question_type)
    # Use unpack_list to turn list of 1 element tuples in a single 1D list
    possible_questions = unpack_list(possible_questions)
    # Randomly choose a questionID from the possible_questions list
    questionID_chosen = random.choice(possible_questions)
    # Add questionID chosen to current_questionID list
    current_questionID[0] = questionID_chosen
    # call function to display question (depending on type)
    if question_type == "MCQ":
        display_mc_question(questionID_chosen)
    elif question_type == "WRITTEN":
        display_written_question(questionID_chosen)

def display_mc_question(questionID):
    written_question_page.withdraw()
    # Call subroutine to 'reset' the MCQ page so it is ready to be updated for a new question
    reset_mcq()
    # Call DB_actions get_options function to retrieve 4 options for a MCQ
    question_options = DB_actions.get_options(questionID)
    # Use make_multiline_text function to store questionn text with '\n's to allow for multiline questions
    question_to_display = make_multiline_text(question_options[0][0], "question")
    mc_question_page.question_text_label.config(text = question_to_display)
    for i in range(0, 4):
        # Choose random option from question_options list (so options are displayed in random order)
        question_option = random.choice(question_options)
        # Use make_multiline_text for formatting over more than 1 line (if needed) and display text on radiobutton
        text_to_display = make_multiline_text(question_option[1], "option")
        mc_question_page.options[i].config(text = text_to_display)
        # remove question_option from question_options so the option is not displayed again
        question_options.remove(question_option)
    mc_question_page.deiconify()

def reset_mcq():
    # Set radiobutton option chosen StringVar to '0' so no option is selected)
    mc_question_page.option_chosen.set("0")
    mc_question_page.explain_button.config(state = "active")
    # Iterate through each option and set colour of each radiobutton to default
    for option in mc_question_page.options:
        option.config(selectcolor = GUI.option_selected, background = GUI.default)
    # Change text/command for submit_answer_button so it is used for checking an answer
    mc_question_page.submit_answer_button.config(text = "Submit", command = check_option_selected)
    mc_question_page.question_correct_label.config(text = "")
    # Update questions_answered and questions_correct
    mc_question_page.no_questions_answered.config(text = current_session_results["Answered"])
    mc_question_page.no_questions_correct.config(text = current_session_results["Correct"])
    # Use calculate_session_accuracy() to update overall session accuracy (including accuracy progress bar)
    accuracy_text, accuracy_value = calculate_session_accuracy()
    mc_question_page.accuracy_label.config(text = accuracy_text)
    mc_question_page.accuracy_bar.config(value = accuracy_value)
    # Update current_question_count and display updated count
    current_question_count[0] += 1
    mc_question_page.question_number.config(text = current_question_count)

def display_written_question(questionID):
    mc_question_page.withdraw()
    # Call subroutuine to 'reset' the page so it is ready to be updated for a new question
    reset_written_question()
    # Display written questions over multiple lines if necessary
    question = DB_actions.get_question_text(questionID)
    question_to_display = make_multiline_text(question, "question")
    written_question_page.question_text_label.config(text = question_to_display)
    written_question_page.deiconify()

def reset_written_question():
    # Delete any user answer of a previous question
    written_question_page.user_question_answer.delete("1.0", "end")
    written_question_page.explain_button.config(state = "active")
    # Clear question status label and change colour to default
    written_question_page.question_status_label.config(text = "", fg = "#000000")
    # Reset button to check question
    written_question_page.submit_answer_button.config(text = "Submit", command = check_written_text)
    # Update questions_answered and questions_correct
    written_question_page.no_questions_answered.config(text = current_session_results["Answered"])
    written_question_page.no_questions_correct.config(text = current_session_results["Correct"])
    # Use calculate_session_accuracy() to update overall session accuracy (including accuracy progress bar)
    accuracy_text, accuracy_value = calculate_session_accuracy()
    written_question_page.accuracy_label.config(text = accuracy_text)
    written_question_page.accuracy_bar.config(value = accuracy_value)
    # Update current_question_count and display updated count
    current_question_count[0] += 1
    written_question_page.question_number.config(text = current_question_count)

def make_multiline_text(text, type):
    # Decide maximum line length depending on the type of text (witdth of label widget)
    if type == "option":
        next_line_length = 40
    elif type == "question":
        next_line_length = 60
    elif type == "explanation":
        next_line_length = 100
    lines_used = 1
    # Split text into list of words split by spaces
    words_list = text.split(" ")
    text_to_display = ""
    for word in words_list:
        # Check if the length of the text plus the length of the world is less than the max line length
        if (len(text_to_display) + len(word)) < (lines_used * next_line_length):
            # If the new text would not overun (if statement is True) add word to text_to_display with space
            text_to_display = text_to_display + " " + word
        else:
            # Otherwise go onto new line and add \n to create new line before word added
            lines_used += 1
            text_to_display = text_to_display + "\n " + word
    return text_to_display


def calculate_session_accuracy():
    # If no questions have been answered, display 'n/a' for accuracy and give progress bar a default value (70%)
    if current_session_results["Answered"] == 0:
        accuracy_text = "Accuracy: n/a"
        accuracy_percent = 70
    # Otherwise calculate accuracy as a percent rounded to 1dp
    else:
        accuracy_percent = round((current_session_results["Correct"] / current_session_results["Answered"]) * 100, 1)
        accuracy_text = "Accuracy: " + str(accuracy_percent) + "%"
    # return both accuracy_text (to be displayed) and accuracy_percent (for use in accuracy bar)
    return accuracy_text, accuracy_percent


def check_option_selected():
    # If option_chosen StringVar is still '0', then display text to show no option chosen and do not check question
    if mc_question_page.option_chosen.get() == "0":
        mc_question_page.question_correct_label.config(text = "You must select an option")
    # Otherwise call check_mcq() subroutine
    else:
        check_mcq()

def check_mcq():
    # Increment questions answered in current_session_results
    current_session_results["Answered"] += 1
    mc_question_page.no_questions_answered.config(text = current_session_results["Answered"])
    questionID = current_questionID[0]
    question_options = DB_actions.get_options(questionID)
    for option in question_options:
        # If is_correct field for option equals 'C' then assign the option text to correct_option_text
        if option[2] == "C":
            correct_option_text = option[1].strip(" ")
    for i in range(1, 5):
        # If option chosen matches i value, get text for option chosen by user and remove any '\n's
        if mc_question_page.option_chosen.get() == str(i):
            user_option_text = mc_question_page.options[i - 1].cget("text")
            user_option_text = user_option_text.strip(" ")
            user_option_text = user_option_text.replace("\n", "")
            # Take away one from user_option_chosen as list indexing starts from 0
            user_option_chosen = i - 1
    mc_question_page.submit_answer_button.config(text = "Next question", command = choose_next_topic)
    # Call function depending on whether user_option_text and correct_option_text match
    # Additionaly add question result to queue
    if user_option_text == correct_option_text:
        recent_session_results.enqueue("C")
        # Only check for session milestones if question is answered correctly
        check_for_session_milestone()
        mcq_correct(user_option_chosen)
    else:
        recent_session_results.enqueue("I")
        mcq_incorrect(correct_option_text)

def check_written_text():
    # Get all user answer and check if any text is present
    user_answer = written_question_page.user_question_answer.get("1.0", "end-1c")
    if user_answer == "":
        written_question_page.question_status_label.config(text = "You must enter an answer")
    elif len(user_answer) > 200:
        written_question_page.question_status_label.config(text = "Answer is too long - over 200 characters")
    else:
        # Only call question checking algorithm if no text is entered
        check_written_question(user_answer.lower())

def check_written_question(user_answer):
    # Increment questions answered in current_session_results
    current_session_results["Answered"] += 1
    written_question_page.no_questions_answered.config(text = current_session_results["Answered"])
    # Get all answers to question using DB_actions function
    question_answers = unpack_list(DB_actions.get_answers(current_questionID[0]))
    question_correct = False
    answer_count = 0
    # Use loop to check if each possible answer is found in the user answer
    while (not question_correct) and answer_count < len(question_answers):
        # Get lowercase answer at index
        answer_to_check = question_answers[answer_count].lower()
        # Split up answer into list and make lowercase
        answers_to_check = answer_to_check.split(" ")
        question_correct = True
        # Check if each word in answer_to_check is found in the user answer
        for answer in answers_to_check:
            if user_answer.find(answer) == -1:
                question_correct = False
        answer_count += 1
    # Change button to go to next question
    written_question_page.submit_answer_button.config(text = "Next question", command = choose_next_topic)
    # Depending on whether question is correct, call function and add result to queue
    if question_correct:
        recent_session_results.enqueue("C")
        # Only check for session milestones if question is answered correctly
        check_for_session_milestone()
        written_question_correct()
    else:
        recent_session_results.enqueue("I")
        written_question_incorrect(current_questionID[0])

def mcq_correct(user_option_chosen):
    # Change colour of correct option to green and display correct
    mc_question_page.options[user_option_chosen].config(background = "green", selectcolor = "green")
    mc_question_page.question_correct_label.config(text = "Correct ")
    # Increment questions answered correctly in current_session_results and display new value
    current_session_results["Correct"] += 1
    mc_question_page.no_questions_correct.config(text = current_session_results["Correct"])
    # Calculate and display new session accuracy
    accuracy_text, accuracy_value = calculate_session_accuracy()
    mc_question_page.accuracy_label.config(text = accuracy_text)
    mc_question_page.accuracy_bar.config(value = accuracy_value)
    # Call change_topic_results to update topic_results in database
    change_topic_results("Correct")

def mcq_incorrect(correct_answer):
    mc_question_page.question_correct_label.config(text = "Incorrect ")
    for option in mc_question_page.options:
        option_text = option.cget("text").strip()
        option_text = option_text.replace("\n", "")
        # If option text for radiobutton (without '\n's) matches correct answer change option colour to light green
        if option_text == correct_answer:
            option.config(background = "light green", selectcolor = "light green")
    # Calculate and display new session accuracy
    accuracy_text, accuracy_value = calculate_session_accuracy()
    mc_question_page.accuracy_label.config(text = accuracy_text)
    mc_question_page.accuracy_bar.config(value = accuracy_value)
    # Call change_topic_results to update topic_results in database
    change_topic_results("Incorrect")

def written_question_correct():
    # Display message showing answer is correct in green
    written_question_page.question_status_label.config(text = "Correct ", fg = "green")
    # Increment questions answered correctly in current_session_results and display new value
    current_session_results["Correct"] += 1
    written_question_page.no_questions_correct.config(text = current_session_results["Correct"])
    # Calculate and display new session accuracy
    accuracy_text, accuracy_value = calculate_session_accuracy()
    written_question_page.accuracy_label.config(text = accuracy_text)
    written_question_page.accuracy_bar.config(value = accuracy_value)
    # Call change_topic_results to update topic_results in database
    change_topic_results("Correct")

def written_question_incorrect(questionID):
    # Get 'ideal' answers from database
    ideal_answers = unpack_list(DB_actions.get_ideal_answers(questionID))
    # Add ideal answers into one string, split over more than 1 line if necessery
    text_to_display = "Incorrect, answer is: "
    for answer in ideal_answers:
        text_to_display += (answer + ", ")
    text_to_display = text_to_display.strip(", ")
    text_to_display = make_multiline_text(text_to_display, "question")
    written_question_page.question_status_label.config(text = text_to_display)
    # Calculate and display new session accuracy
    accuracy_text, accuracy_value = calculate_session_accuracy()
    written_question_page.accuracy_label.config(text = accuracy_text)
    written_question_page.accuracy_bar.config(value = accuracy_value)
    # Call change_topic_results to update topic_results in database
    change_topic_results("Incorrect")

def change_topic_results(last_question_result):
    userID = DB_actions.retrieve_userID(current_username[0])
    topicID = DB_actions.get_question_topic(current_questionID[0])
    # Get questions answered and accuracy for topic using DB_actions get_topic_details function
    topic_details = DB_actions.get_topic_details(userID, topicID)
    # Find number of questions_correct by multiplying questions answered and accuracy
    questions_correct = topic_details[0] * topic_details[1]
    # Calculate accuracy depending on last question result (add one to question correct if last question was correct)
    if last_question_result == "Correct":
        new_accuracy = (questions_correct + 1) / (topic_details[0] + 1)
    elif last_question_result == "Incorrect":
        new_accuracy = questions_correct / (topic_details[0] + 1)
    # Update accuracy and questions_answered field in topic_results using update_topic_results
    DB_actions.update_topic_results(new_accuracy, topic_details[0] + 1, userID, topicID)


def check_for_session_milestone():
    # Call method to get queue as a list
    session_results = recent_session_results.get_queue()
    # Get value in user milestones dictionary and store it in best_streak
    best_streak = current_user_milestones["Questions answered in row"]
    current_streak = 0
    # Iterate through results in queue
    for result in session_results:
        # If item is 'C', then add one to streak
        if result == "C":
            current_streak += 1
        else:
            current_streak = 0
        # Update best_streak if current_streak is higher
        if current_streak > best_streak:
            best_streak = current_streak
    # Set value in dictionary depending on best streak (20 if 20, 10 if between 10-19, and 5 if between 5-9)
    if best_streak == 20:
        current_user_milestones["Questions answered in row"] = 20
    elif best_streak >= 10:
        current_user_milestones["Questions answered in row"] = 10
    elif best_streak >= 5:
        current_user_milestones["Questions answered in row"] = 5


def end_session():
    # Withdraw both question pages and open end_session_page
    mc_question_page.withdraw()
    written_question_page.withdraw()
    end_session_page.deiconify()
    end_session_page.username_label.config(text = current_username[0])
    # Add results to end_session page, including accuracy
    end_session_page.no_questions_answered.config(text = current_session_results["Answered"])
    end_session_page.no_questions_correct.config(text = current_session_results["Correct"])
    calculate_end_session_accuracy()
    # Gets epoch time for end of session
    session_times[1] = time.time()
    # Calculate session length and convert it to minutes
    time_for_session = (session_times[1] - session_times[0]) // 60
    end_session_page.session_time_label.config(text = "Session time: " + str(int(time_for_session)) + " mins")
    # Call function to check for a new time milestone
    check_time_milestone(time_for_session)
    # Use set_dashboard function to update dashboard and reset values associated with a session
    current_session_results["Answered"] = 0
    current_session_results["Correct"] = 0
    current_question_count[0] = 0
    current_questionID[0] = 0

def calculate_end_session_accuracy():
    # Set 'default' value if no questions have been answered
    if current_session_results["Answered"] == 0:
        accuracy_value = 70
        end_session_page.no_accuracy_label.config(text = "n/a")
    else:
        # Otherwise calculate accuracy and display it
        accuracy_value = round((current_session_results["Correct"] / current_session_results["Answered"]) * 100, 1)
        end_session_page.no_accuracy_label.config(text = str(accuracy_value) + "%")
    end_session_page.accuracy_bar.configure(value = accuracy_value)


def check_time_milestone(time_for_session):
    # Get longest time stored and compare it to current time
    best_session_time = DB_actions.get_longest_session(current_username[0])
    if time_for_session > best_session_time:
        # If current time is higher, then update longest session time
        DB_actions.update_longest_session(time_for_session, current_username[0])


def explain_mcq():
    mc_question_page.explain_button.config(state = "disabled")
    # Get question text and display at top of window
    question_text = DB_actions.get_question_text(current_questionID[0])
    text_to_display = make_multiline_text(question_text, "question")
    question_explanation_window.question_label.config(text = text_to_display)
    # Get correct question option from 4 options
    question_options = DB_actions.get_options(current_questionID[0])
    for option in question_options:
        if option[2] == "C":
            correct_answer = option[1]
    # Create prompt for response with specifc question and specific correct answer
    response_contents = "Explain the following question in around 800 characters based on A level Computer Science specifications (without mentioning them explicitly): "
    response_contents += question_text
    response_contents += ("The correct answer was " + correct_answer)
    response_contents += " Please do not use any markdown formatting in the response."
    # Generate and display reponse (over multiple lines if necessary)
    response = client.models.generate_content(model = "gemini-2.5-flash", contents = response_contents)
    text_to_display = make_multiline_text(response.text, "explanation")
    question_explanation_window.question_explanation.config(text = text_to_display)
    # Unhide window
    try:
        question_explanation_window.deiconify()
    except:
        pass

def explain_written_question():
    written_question_page.explain_button.config(state = "disabled")
    # Get question text and display at top of window
    question_text = DB_actions.get_question_text(current_questionID[0])
    text_to_display = make_multiline_text(question_text, "question")
    question_explanation_window.question_label.config(text = text_to_display)
    # Get question ideal answer(s)
    question_answers = unpack_list(DB_actions.get_ideal_answers(current_questionID[0]))
    # Create prompt for response with specifc question and ideal answers
    response_contents = "Explain the following question in around 800 characters based on A level Computer Science specifications (without mentioning them explicitly): "
    response_contents += question_text
    response_contents += "The correct answer(s) was "
    # Display answers together over multiple lines
    for answer in question_answers:
        response_contents += (answer + ", ")
    response_contents += " Please do not use any markdown formatting in the response."
    # Generate and display reponse (over multiple lines if necessary)
    response = client.models.generate_content(model = "gemini-2.5-flash", contents = response_contents)
    text_to_display = make_multiline_text(response.text, "explanation")
    question_explanation_window.question_explanation.config(text = text_to_display)
    try:
        question_explanation_window.deiconify()
    except:
        pass
# Page window objects defined here, with any function/data properties
home_page = GUI.Home_Page(home_to_login, home_to_create_account)
create_account_page = GUI.Create_Account_Page(create_account_to_home, create_account_attempt)
login_page = GUI.Login_Page(login_to_home, login_attempt)
dashboard = GUI.Dashboard(dashboard_to_home, dashboard_to_start_session)
start_session_page = GUI.Start_Session_Page(start_session_to_dashboard, get_topics, unpack_list(DB_actions.get_all_topics()))
mc_question_page = GUI.MC_Question_Page(end_session, check_option_selected, explain_mcq)
written_question_page = GUI.Written_Question_Page(end_session, check_written_text, explain_written_question)
end_session_page = GUI.End_Session_Page(end_session_to_dashboard)
question_explanation_window = GUI.Question_Explanation_Window()
home_page.mainloop()