import sqlite3
from users import User

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE users (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	first_name VARCHAR(30),
	last_name VARCHAR(30),
	age INTEGER(3),
	email VARCHAR(30))""")

def insert_user(user):
	with conn:
		c.execute("INSERT INTO users VALUES (:id, :first, :last, :age, :email)", {'id': user.id,'first': user.first, 'last': user.last, 'age': user.age, 'email': user.email})

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

#update_age(user_1, 89)

#users = get_users_by_name('Kevin')
#print(users)

#users = get_users_by_name('Jonker')
#print(users)

users = get_users('all')
print(users)

conn.close()