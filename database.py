
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return connection


def get_sales_data():

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT
            c.customer_id,
            c.customer_name,
            c.email,
            o.order_id,
            oi.item_id,
            o.order_date,
            o.order_status,
            p.product_name,
            p.category,
            
            oi.quantity,
            oi.unit_price,
            (oi.quantity * oi.unit_price) AS total_amount

        FROM customers c

        INNER JOIN orders o
            ON c.customer_id = o.customer_id

        INNER JOIN order_items oi
            ON o.order_id = oi.order_id

        INNER JOIN products p
            ON oi.product_id = p.product_id

        WHERE o.order_status = 'Completed'

        ORDER BY o.order_date DESC
    """

    cursor.execute(query)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return records
