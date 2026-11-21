
import os
import re
import ssl
import smtplib
import certifi
from pathlib import Path
from datetime import date
from email.message import EmailMessage
from email.utils import formataddr

from dotenv import load_dotenv
from database import get_connection


# Load SMTP credentials from .env
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME", "Sales CRM")

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"


# 1. Retrieve customer information from MySQL
def get_customer(customer_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT customer_id, customer_name, email
            FROM customers
            WHERE customer_id = %s
        """
        
        cursor.execute(query, (customer_id,))
        customer = cursor.fetchone()
        print(f"Retrieved customer info: {customer}")

        return customer

    finally:
        cursor.close()
        connection.close()


# 2. Create or update the email attempt log
def start_email_attempt(customer_id, report_month):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        check_query = """
            SELECT report_status
            FROM report_email_logs
            WHERE customer_id = %s
              AND report_month = %s
        """

        cursor.execute(check_query, (customer_id, report_month))
        existing_log = cursor.fetchone()

        if existing_log and existing_log["report_status"] == "Sent":
            raise ValueError(
                "This customer's report has already been sent."
            )

        insert_query = """
            INSERT INTO report_email_logs
            (customer_id, report_month, report_status, attempt_count)
            VALUES (%s, %s, 'Pending', 1)

            ON DUPLICATE KEY UPDATE
                report_status = 'Pending',
                sent_at = NULL,
                error_message = NULL,
                attempt_count = attempt_count + 1
        """

        cursor.execute(insert_query, (customer_id, report_month))
        connection.commit()

    finally:
        cursor.close()
        connection.close()


# 3. Update email status in MySQL
def update_email_status(
    customer_id,
    report_month,
    status,
    error_message=None
):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        if status == "Sent":

            query = """
                UPDATE report_email_logs
                SET report_status = 'Sent',
                    sent_at = NOW(),
                    error_message = NULL
                WHERE customer_id = %s
                  AND report_month = %s
            """

            cursor.execute(query, (customer_id, report_month))

        else:

            query = """
                UPDATE report_email_logs
                SET report_status = 'Failed',
                    sent_at = NULL,
                    error_message = %s
                WHERE customer_id = %s
                  AND report_month = %s
            """

            cursor.execute(
                query,
                (error_message, customer_id, report_month)
            )

        connection.commit()

    finally:
        cursor.close()
        connection.close()


# 4. Send the customer's Excel report
def send_customer_report(customer_id):

    report_month = date.today().replace(day=1)
    log_started = False

    try:

        # Retrieve customer information
        customer = get_customer(customer_id)

        if not customer:
            raise ValueError("Customer not found.")

        # Create an email attempt record
        start_email_attempt(customer_id, report_month)
        log_started = True

        customer_name = customer["customer_name"]
        receiver_email = customer["email"]

        # Validate the email address format
        email_pattern = r"[^@\s]+@[^@\s]+\.[^@\s]+"

        if not receiver_email or not re.fullmatch(
            email_pattern, receiver_email
        ):
            raise ValueError("Customer email address is invalid.")

        # Locate the report using the trusted customer information
        safe_name = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            customer_name
        ).strip("_")

        report_file = (
            REPORTS_DIR /
            f"{customer_id}_{safe_name}_Report.xlsx"
        )
        print(f"#########Looking for report file at: {report_file}")

        if not report_file.is_file():
            raise FileNotFoundError(
                "Customer Excel report was not found."
            )

        # Prepare the email
        message = EmailMessage()

        message["From"] = formataddr(
            (SENDER_NAME, SMTP_EMAIL)
        )

        message["To"] = receiver_email

        message["Subject"] = (
            f"Monthly Sales Report - {customer_name}"
        )

        message.set_content(
            f"""
Dear {customer_name},

Please find your monthly sales report attached.

Thank you for your business.

Regards,
{SENDER_NAME}
"""
        )

        # Attach Excel file
        with open(report_file, "rb") as file:

            excel_data = file.read()

        message.add_attachment(
            excel_data,
            maintype="application",
            subtype=(
                "vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            filename=report_file.name
        )

        # Validate SMTP configuration
        if not all([SMTP_HOST, SMTP_EMAIL, SMTP_PASSWORD]):
            raise ValueError("SMTP configuration is incomplete.")

        # Connect to SMTP server and send email
        with smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT,
            timeout=30
        ) as server:

            server.ehlo()

            # server.starttls(
            #     context=ssl.create_default_context()
            # )
            ssl_context = ssl.create_default_context(
            cafile=certifi.where()
)

            server.starttls(context=ssl_context)

            server.ehlo()

            server.login(
                SMTP_EMAIL,
                SMTP_PASSWORD
            )

            refused = server.send_message(message)

            if refused:
                raise RuntimeError(
                    "The email server refused the recipient."
                )

        # Update status only after SMTP accepts the email
        update_email_status(
            customer_id,
            report_month,
            "Sent"
        )

        return {
            "success": True,
            "message": (
                f"Report submitted successfully for {customer_name}."
            )
        }

    except Exception as error:

        print("Email sending failed:", error)

        # Record the failure in MySQL
        if log_started:
            try:
                update_email_status(
                    customer_id,
                    report_month,
                    "Failed",
                    str(error)[:2000]
                )
            except Exception as log_error:
                print("Could not update email log:", log_error)

        return {
            "success": False,
            "message": str(error)
        }
