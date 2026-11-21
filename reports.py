
import os
import re
import pandas as pd
from pathlib import Path

from pkg_resources import safe_name


def generate_customer_reports(df):

    # Create reports folder
    os.makedirs("reports", exist_ok=True)

    # Identify unique customers
    customers = df["customer_id"].unique()

    for customer_id in customers:

        # Filter one customer's records
        customer_df = df[
            df["customer_id"] == customer_id
        ].copy()

        # Customer details
        customer_name = customer_df[
            "customer_name"
        ].iloc[0]

        email = customer_df["email"].iloc[0]

        # Calculate summary
        total_orders = customer_df[
            "order_id"
        ].nunique()

        total_quantity = customer_df[
            "quantity"
        ].sum()

        total_sales = customer_df[
            "total_amount"
        ].sum()

        # Create summary DataFrame
        customer_summary = pd.DataFrame({
            "Metric": [
                "Customer Name",
                "Email",
                "Total Orders",
                "Total Quantity",
                "Total Sales"
            ],
            "Value": [
                customer_name,
                email,
                total_orders,
                total_quantity,
                total_sales
            ]
        })
        # Create safe customer name
        safe_name = re.sub(
            r"[^A-Za-z0-9_-]+",
             "_",
    str(customer_name)
).strip("_")

# Create filename
        filename = f"reports/{customer_id}_{safe_name}_Report.xlsx"
        # Create filename
        # filename = f"reports/{customer_id}_{customer_name}_Report.xlsx"

        # Export both sheets
        with pd.ExcelWriter(
            filename,
            engine="openpyxl"
        ) as writer:

            customer_summary.to_excel(
                writer,
                sheet_name="Summary",
                index=False
            )

            customer_df.to_excel(
                writer,
                sheet_name="Order Details",
                index=False
            )

        print(
            f"Report generated for {customer_name}"
        )

    print("All customer reports generated!")
