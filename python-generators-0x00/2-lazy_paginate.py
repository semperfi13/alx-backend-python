#!/usr/bin/python3
import seed


def paginate_users(page_size, offset):
    """Fetches a page of users from the database"""
    connection = seed.connect_to_prodev()
    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def lazy_paginate(page_size):
    """Generator that lazily loads pages of users"""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # No more data
            break
        yield page
        offset += page_size
