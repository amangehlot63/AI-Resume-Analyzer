import sqlite3


# Register user
def register_user(username, password):

    conn = sqlite3.connect('database/app.db')

    cursor = conn.cursor()

    try:

        cursor.execute(

            '''

            INSERT INTO users (

                username,
                password

            )

            VALUES (?, ?)

            ''',

            (username, password)

        )

        conn.commit()

        return True

    except:
        return False

    finally:
        conn.close()


# Login user
def login_user(username, password):

    conn = sqlite3.connect('database/app.db')

    cursor = conn.cursor()

    cursor.execute(

        '''

        SELECT *

        FROM users

        WHERE username = ?
        AND password = ?

        ''',

        (username, password)

    )

    user = cursor.fetchone()

    conn.close()

    return user