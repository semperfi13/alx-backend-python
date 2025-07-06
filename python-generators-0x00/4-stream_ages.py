#!/usr/bin/python3
import seed


def stream_user_ages():
    """Generator that streams user ages one by one from the database"""
    connection = seed.connect_to_prodev()
    if not connection:
        yield None
        return

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT age FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]
    finally:
        cursor.close()
        connection.close()


def calculate_average_age():
    """Calculates average age using the stream_user_ages generator"""
    total = 0
    count = 0

    for age in stream_user_ages():
        if age is not None:
            total += age
            count += 1

    if count == 0:
        return 0.0

    average = total / count
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
