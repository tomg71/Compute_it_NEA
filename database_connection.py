# Import sqlite3 library
import sqlite3

# Connect to database
db = sqlite3.connect("project_database.db")
# Create cursor to interact with database
cur = db.cursor()

# Functions for user_details table
def count_users():
    '''Returns total number of records in user_details table (number of users)'''
    # Use aggregate count function to get total number of records
    cur.execute("SELECT COUNT(*) FROM user_details")
    # Store value in tuple in separate variable
    user_count = cur.fetchone()[0]
    return user_count

def insert_new_user(username, password_hash):
    '''Inserts new record into user_details table for new user'''
    # This acts as an 'autoincrement' line, so the userID will be unique & ascending for each new record
    userID = count_users() + 1
    cur.execute("INSERT INTO user_details VALUES (?, ?, ?, 0, 0, 0)", (userID, username, password_hash))
    # Commits changes to database
    db.commit()

def retrieve_password_hash(username):
    '''Returns password hash for record with username provided'''
    cur.execute("SELECT password_hash FROM user_details WHERE username = ?", (username,))
    password_hash = cur.fetchall()
    # Return message to main program is no entries are found
    if len(password_hash) == 0:
        return "no entries found"
    else:
        # Returns only the actual password hash value, without being in a data structure
        return password_hash[0][0]

def retrieve_userID(username):
    '''Returns userID for record with username provided'''
    cur.execute("SELECT userID FROM user_details WHERE username = ?", (username,))
    userID = cur.fetchall()
    # Returns only the actual userID, without being in a data structure
    return userID[0][0]

def change_failed_attempts(new_failed_attempts, username):
    '''Modifies failed_attempts value for a user'''
    cur.execute("UPDATE user_details SET failed_attempts = ? WHERE username = ?", (new_failed_attempts, username))
    db.commit()

def change_lock_until(new_lock_until, username):
    '''Modifies lock_until value for a user'''
    cur.execute("UPDATE user_details SET lock_until = ? WHERE username = ?", (new_lock_until, username))
    db.commit()

def reset_failed_attempts(username):
    '''Sets both failed_attempts and lock_until to 0 for a user (used after a successful login)'''
    cur.execute("UPDATE user_details SET failed_attempts = 0, lock_until = 0 WHERE username = ?", (username,))
    db.commit()

def get_failed_attempts(username):
    '''Returns failed_attempts value for a user based on the username provided'''
    cur.execute("SELECT failed_attempts FROM user_details WHERE username = ?", (username,))
    failed_attempts = cur.fetchall()
    return failed_attempts[0][0]

def get_lock_until(username):
    '''Returns lock_until value for a user based on the username provided'''
    cur.execute("SELECT lock_until FROM user_details WHERE username = ?", (username,))
    lock_until = cur.fetchall()
    return lock_until[0][0]

def get_longest_session(username):
    '''Returns longest_session value for a user '''
    cur.execute("SELECT longest_session FROM user_details WHERE username = ?", (username,))
    longest_session = cur.fetchall()
    return longest_session[0][0]

def update_longest_session(new_longest_session, username):
    '''Updates longest_session value for a user'''
    cur.execute("UPDATE user_details SET longest_session = ? WHERE username = ?", (new_longest_session, username))
    db.commit()

# Functions for topic_results table
def new_user_records(userID, topicIDs):
    '''Inserts new records for each topic for a new user (with default accuracy and questions_answered values)'''
    for topicID in topicIDs:
        cur.execute("INSERT INTO topic_results VALUES (?, ?, 0, 0)", (userID, topicID))
        db.commit()

def get_accuracy(userID, topicID):
    '''Returns accuracy value for user for specific topic'''
    cur.execute("SELECT accuracy FROM topic_results WHERE userID = ? AND topicID = ?", (userID, topicID))
    accuracy = cur.fetchall()
    # Returns only accuracy value (only 1 will be returned as 1 field selected and one 1 record will be retrieved)
    return accuracy[0][0]

def get_topic_details(userID, topicID):
    '''Returns questions_answered and accuracy values for user for a specific topic'''
    cur.execute("SELECT questions_answered, accuracy FROM topic_results WHERE userID = ? AND topicID = ?", (userID, topicID))
    topic_details = cur.fetchall()
    # Returns a tuple with items questions_answered and accuracy (without list around it)
    return topic_details[0]

def update_topic_results(accuracy, questions_answered, userID, topicID):
    '''Updates a record in topic_results based on a userID and topicID'''
    parameters = (accuracy, questions_answered, userID, topicID)
    cur.execute("UPDATE topic_results SET accuracy = ?, questions_answered = ? WHERE userID = ? AND topicID = ?", parameters)
    db.commit()

def get_accuracy_details(userID):
    '''Returns accuracy and questions_answered fields for all records of a user'''
    cur.execute("SELECT accuracy, questions_answered FROM topic_results WHERE userID = ?", (userID,))
    user_accuracy_details = cur.fetchall()
    return user_accuracy_details

def no_of_questions_answered(userID):
    '''Returns total number of questions answered by a user'''
    # Use aggregate sum function to get number of questions answered
    cur.execute("SELECT SUM(questions_answered) FROM topic_results WHERE userID = ?", (userID,))
    total_questions_answered = cur.fetchone()[0]
    return total_questions_answered

# Multi-table function (topics and topic_results)
def get_dashboard_details(accuracy_type, userID):
    '''Returns 3 records, with fields topic_name and accuracy, which have either the highest/lowest accuracy values'''
    # If "Higest" is inputted, use descending order (get highest accuracies)
    if accuracy_type == "Highest":
        # Join statement written out over two lines as it is too long for one line
        # Order by accuracy first, then order by questions_answered if two records have equal accuracy
        execute_statement = '''SELECT topic_name, accuracy, questions_answered FROM topics, topic_results WHERE 
        topics.topicID = topic_results.topicID AND userID = ? ORDER BY accuracy DESC, questions_answered DESC'''
        cur.execute(execute_statement, (userID,))
        # Retrieve only first 3 records
        user_results = cur.fetchmany(3)
    # If "Lowest" is inputted, use ascending order (get lowest accuracies)
    elif accuracy_type == "Lowest":
        execute_statement = '''SELECT topic_name, accuracy, questions_answered FROM topics, topic_results WHERE 
        topics.topicID = topic_results.topicID AND userID = ? ORDER BY accuracy ASC, questions_answered DESC'''
        cur.execute(execute_statement, (userID,))
        user_results = cur.fetchmany(3)
    return user_results

# Functions for topics table
def get_all_topics():
    '''Returns all topic names'''
    cur.execute("SELECT topic_name FROM topics")
    topic_list = cur.fetchall()
    return topic_list


# Functions for questions table
def num_of_questions(topicID):
    '''Returns number of records found in table with certain topicID'''
    cur.execute("SELECT COUNT(*) FROM questions WHERE topicID = ?", (topicID,))
    # Returns only exact number
    number_of_questions = cur.fetchone()[0]
    return number_of_questions

def get_possible_questions(topicID, type):
    '''Returns any questionIDs found of a certain topicID and type'''
    cur.execute("SELECT questionID FROM questions WHERE topicID = ? AND question_type = ?", (topicID, type))
    possible_questions = cur.fetchall()
    return possible_questions

def get_question_text(questionID):
    '''Returns text for a question given the questionID'''
    cur.execute("SELECT question FROM questions WHERE questionID = ?", (questionID,))
    question_text = cur.fetchone()[0]
    return question_text

def get_question_topic(questionID):
    '''Returns the topicID of a question given the questionID'''
    cur.execute("SELECT topicID FROM questions WHERE questionID = ?", (questionID,))
    question_topic = cur.fetchone()[0]
    return question_topic

# Functions for written_answers table
def get_answers(questionID):
    '''Returns answer field for any records with a certain questionID'''
    cur.execute("SELECT answer FROM written_answers WHERE questionID = ?", (questionID,))
    question_answers = cur.fetchall()
    return question_answers

def get_ideal_answers(questionID):
    '''Return answer field for any records with a certain questionID and marked as ideal answers'''
    cur.execute("SELECT answer FROM written_answers WHERE questionID = ? AND ideal_answer = 'Y'", (questionID,))
    ideal_answers = cur.fetchall()
    return ideal_answers

# Multi-table functions (questions and multi_choice_options)
def get_options(questionID):
    '''Returns question text, option text and whether an option is correct for all 4 options for a question'''
    # Join statement written out over two lines as it is too long for one line
    execute_statement = '''SELECT question, option_text, is_correct FROM questions, multi_choice_options
    WHERE questions.questionID = multi_choice_options.questionID AND questions.questionID = ?'''
    cur.execute(execute_statement, (questionID,))
    options = cur.fetchall()
    return options