#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode


def connect_to_prodev():
    """Connect to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="", database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None


def stream_users_in_batches(batch_size):
    """Generator function that fetches users in batches from the database"""
    connection = connect_to_prodev()
    if not connection:
        yield None
        return

    cursor = connection.cursor(dictionary=True)
    offset = 0

    while True:
        try:
            query = f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}"
            cursor.execute(query)
            batch = cursor.fetchall()

            if not batch:
                break  # No more data

            yield batch
            offset += batch_size

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            break

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Processes batches of users and filters those over 25 years old"""
    for batch in stream_users_in_batches(batch_size):
        if batch is None:
            break

        for user in batch:
            if user["age"] > 25:
                print(user)
