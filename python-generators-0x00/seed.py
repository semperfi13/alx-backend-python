#!/usr/bin/python3
import csv
import uuid
import mysql.connector
from mysql.connector import errorcode


def connect_db():
    """Connect to the MySQL database server"""
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


def create_database(connection):
    """Create the database ALX_prodev if it does not exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()


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


def create_table(connection):
    """Create a table user_data if it does not exist with the required fields"""
    cursor = connection.cursor()
    table_description = (
        "CREATE TABLE IF NOT EXISTS `user_data` ("
        "  `user_id` VARCHAR(36) NOT NULL,"
        "  `name` VARCHAR(255) NOT NULL,"
        "  `email` VARCHAR(255) NOT NULL,"
        "  `age` DECIMAL(10,0) NOT NULL,"
        "  PRIMARY KEY (`user_id`),"
        "  INDEX `user_id_index` (`user_id`)"
        ") ENGINE=InnoDB"
    )
    try:
        cursor.execute(table_description)
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists.")
        else:
            print(f"Failed creating table: {err}")
    finally:
        cursor.close()


def insert_data(connection, csv_file_path):
    """Insert data from CSV file into the database if it does not exist"""
    cursor = connection.cursor()

    # First check if table is empty
    cursor.execute("SELECT COUNT(*) FROM user_data")
    count = cursor.fetchone()[0]
    if count > 0:
        print("Data already exists in the table")
        cursor.close()
        return

    try:
        with open(csv_file_path, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Check if user_id already exists (though table should be empty)
                cursor.execute(
                    "SELECT 1 FROM user_data WHERE user_id = %s", (row["user_id"],)
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) "
                        "VALUES (%s, %s, %s, %s)",
                        (row["user_id"], row["name"], row["email"], int(row["age"])),
                    )
        connection.commit()
        print("Data inserted successfully")
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found")
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()
