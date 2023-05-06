# Flask Messanger

Flask Messenger is a simple messaging application for the browser. Developed on Flask.

***

### I. Installation steps
<br>

#### 1. Clone the repository

    git clone https://github.com/D1scoB0y/Chat.git

#### 2. Create virtualenv and install requirements
```
    python -m venv venv
```
then
```
    .\venv\Scripts\activate
```
then
```
    cd "project_directory"
```
then
```
    pip install -r requirements.txt
```

#### 3. Add .env file to the root directory

```
# secret key
SECRET_KEY = your secret key

# database config (PostgreSQL by default)
DB_USER = your db user
DB_PASSWORD = your db password
DB_HOST = your db host
DB_PORT = your db port
DB_NAME = your db name
```

> Configure the all parameters for yourself. The default database is PostgreSQL. If you want to use another database you can config SQLALCHEMY_DATABASE_URI in config.py file.

> [PostgreSQL installation guide](https://www.youtube.com/watch?v=0n41UTkOBb0)

#### 4. Make migrations
```
flask db init
```
then
```
flask db migrate
```
then
```
flask db upgrade
```

#### 5. Start the app!
    python app.py

Then open 127.0.0.1:5000 in your browser

***

### II. Messaging
<br>

To exchange messages, you need to register at least 2 users. This is very easy to do, since you only need to come up with a username and password to register.

#### 1. Register 2 users

Open two different bowsers and go to 127.0.0.1:5000. You will see the main page for non-authorized users. Click on the "New Account" button and register in different browsers under different names.


#### 2. Find one of your users using the search bar

Just start typing the name of the user you want to find and you'll get some hints.

#### 3. You can start messaging!

Type your message into input field and press "Send" button(or Enter on your keyboard).

#### 4. Chat commands

There is some very useful chat commands:

1. "/ban" - banned your pen friend
2. "/unban" - unban your friend
3. "/help" - show all chat commands
4. "/clear" - delete all system messages

***

### III. User data

You can change username or logout on user profile page, click on the panel with your name in the upper right corner to go there

