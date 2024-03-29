import sqlite3
from users import User


conn = sqlite3.connect('users.db')

c = conn.cursor()

c.execute("""CREATE TABLE users (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	first_name VARCHAR(30),
	last_name VARCHAR(30),
	age INTEGER(3),
	email VARCHAR(30))""")

c.execute("""CREATE TABLE inlog (
	username VARCHAR(100),
	password VARCHAR(100),
	userid INTEGER NOT NULL PRIMARY KEY, FOREIGN KEY(userid) REFERENCES users(id))""")

conn.commit()

def insert_user(user):
	with conn:
		c.execute(f"INSERT INTO users  (first_name, last_name, age, email) VALUES ('{user.first}','{user.last}',{user.age},'{user.email}')")

def get_users(users):
	c.execute("SELECT * FROM users")
	return c.fetchall()

def get_users_by_name(first_name):
	c.execute("SELECT * FROM users WHERE first_name=:first", {'first': first_name})
	return c.fetchall()

def get_users_by_name(last_name):
	c.execute("SELECT * FROM users WHERE last_name=:last", {'last': last_name})
	return c.fetchall()

def update_age(user, age):
	with conn:
		c.execute("""UPDATE users SET age = :age
					WHERE first_name = :first AND last_name = :last""",
					{'first': user.first, 'last': user.last, 'age': age})

def remove_user(user):
	with conn:
		c.execute("DELETE from users WHERE first_name = :first AND last_name = :last",
		{'first': user.first, 'last': user.last,})

user_1 = User("user.id", "Kevin", "Jonker", "69", "user.email")

insert_user(user_1)

update_age(user_1, 89)

#users = get_users_by_name('Kevin')
#print(users)

#users = get_users_by_name('Jonker')
#print(users)

users = get_users('all')
print(users)

conn.close()


# Voor database.db
#CREATE TABLE patienten (
#	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#	first_name VARCHAR(30),
#	last_name VARCHAR(30),
#	age INTEGER(3),
#	email VARCHAR(30),
#	tag VARCHAR(16))

#INSERT INTO patienten (first_name, last_name, age, email, tag)
#VALUES ('Peter', 'Jansen', '78', 'peterj78@mail.com', '1BBD2EE2');

#INSERT INTO patienten (first_name, last_name, age, email, tag)
#VALUES ('Youri', 'Bakker', '88', 'yourib88@mail.com', '1B009727');

#INSERT INTO patienten (first_name, last_name, age, email, tag)
#VALUES ('Kevin', 'Jonker', '76', 'kevinj76@mail.com', '8901F3B6');

#INSERT INTO patienten (first_name, last_name, age, email, tag)
#VALUES ('Iris', 'Mob', '75', 'irism75@mail.com', 'AB399C65');

#create role rZorgverlening;
#grant all on verzorgers to rZorgverlening;
#grant rZorgverlening to ......;
