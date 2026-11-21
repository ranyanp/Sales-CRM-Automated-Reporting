# Sales CRM – Automated Customer Order Reporting System

## 1. Project Overview

The Sales CRM Automated Reporting System is a Python-based application that automates customer order reporting and email delivery.

It retrieves sales data from a MySQL database, processes and analyses the data using Pandas, generates individual Excel reports for customers, and provides an HTML dashboard to manage report delivery through email.

## 2. Business Problem

Manually preparing customer-wise sales reports and sending them through email can be time-consuming and error-prone.

This project automates the reporting process, reduces manual work, and makes customer reporting more efficient.

## 3. Technologies Used

- Python
- MySQL
- MySQL Connector
- Pandas
- OpenPyXL
- HTML
- CSS
- JavaScript
- SMTP Email Automation

## 4. System Workflow

1. Retrieve customer and order data from MySQL.
2. Connect Python to the MySQL database.
3. Load data into Pandas DataFrames.
4. Perform data cleaning and analysis.
5. Generate individual Excel reports for customers.
6. Display customer reports through an HTML dashboard.
7. Allow the user to send reports through email.
8. Record email sending status in MySQL.

## 5. Project Features

- MySQL database integration
- Automated data extraction
- Data cleaning and analysis using Pandas
- Customer-wise Excel report generation
- Interactive HTML dashboard
- Automated email delivery with Excel attachments
- Email status and error logging
- Retry tracking for failed email attempts

## 6. Project Structure

```text
Sales_crm_Automation/
│
├── database/
│   └── schema.sql
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── screenshots/
│
├── main.py
├── database.py
├── data_analysis.py
├── reports.py
├── email_sender.py
├── server.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 7. Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/ranyanp/Sales-CRM-Automated-Reporting.git
cd Sales-CRM-Automated-Reporting

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Add your own MySQL and SMTP configuration values.

### Step 5: Create the database

Execute `database/schema.sql` in MySQL to create the database and tables.

### Step 6: Generate customer reports

```bash
python3 main.py
```

### Step 7: Start the dashboard

```bash
python3 server.py
```

Open the following URL in your browser:

http://127.0.0.1:8000/

## 8. Security Considerations

- Database and SMTP credentials are stored in environment variables.
- The `.env` file is excluded from Git.
- Generated customer reports are excluded from the repository.
- SQL queries use parameterised inputs where applicable.



https://github.com/ranyanp/Sales-CRM-Automated-Reporting