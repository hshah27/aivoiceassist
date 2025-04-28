import sqlite3
import csv
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()
# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT into sys_command VALUES (null,'telegram','C:\\Users\\HASTI\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe')"
# cursor.execute(query)
# conn.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

query = "INSERT INTO web_command VALUES (null,'chat gpt', 'https://chatgpt.com/')"
cursor.execute(query)
conn.commit()
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 2, 20]  # First Name, Last Name, Phone Number

# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     headers = next(csvreader, None)  # Skip headers
#     for row in csvreader:
#         if len(row) > max(desired_columns_indices):  # Ensure indices exist
#             selected_data = [row[i] for i in desired_columns_indices]
#             cursor.execute('''INSERT INTO contacts (id, name, mobile_no) VALUES (null, ?, ?);''', 
#                            (f"{selected_data[0]} {selected_data[1]}", selected_data[2]))  # Combine first and last name
#         else:
#             print(f"Skipping row (not enough columns): {row}")

# conn.commit()
# conn.close()

# query = "delete from contacts where id = 1"
# cursor.execute(query)
# conn.commit()


# query = 'hasti'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# if results:  
#     print(results[0][0])  # Print the first result
# else:
#     print("No matching contacts found.")