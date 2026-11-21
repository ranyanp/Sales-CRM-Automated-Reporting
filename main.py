
import pandas as pd
from database import get_sales_data
import os
from data_analysis import clean_sales_data
from reports import generate_customer_reports
# Step 1: Retrieve records from MySQL
sales = get_sales_data()

# Step 2: Get column names
# For now, use the known SQL result columns
columns = [
    "customer_id",
    "customer_name",
    "email",
    "order_id",
    "item_id",
    "order_date",
    "order_status",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "total_amount"
]

# Step 3: Convert into DataFrame
df = pd.DataFrame(sales, columns=columns)

# Step 4: Convert date column
df["order_date"] = pd.to_datetime(df["order_date"])

# Step 5: Inspect data
print("\nFirst 5 Records:")
print(df.head())

print("\nDataFrame Information:")
df.info()

print("\nDataFrame Shape:")
print(df.shape)

print("\nStatistical Summary:")
print(df.describe())

# Step 6: Export to Excel
df.to_excel("sales_report.xlsx", index=False)

print("\nExcel Report Generated Successfully!")

# os.makedirs("reports", exist_ok=True)
# os.makedirs() creates a directory.reports is the directory name exist_ok=True prevents an error if the folder already exists.
# Clean data
clean_df = clean_sales_data(df)
generate_customer_reports(clean_df)