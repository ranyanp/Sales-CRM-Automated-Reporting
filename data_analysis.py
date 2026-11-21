
import pandas as pd


def clean_sales_data(df):

    # Keep original data safe
    df_clean = df.copy()

    # Convert data types
    df_clean["quantity"] = pd.to_numeric(
        df_clean["quantity"],
        errors="coerce"
    )

    df_clean["unit_price"] = pd.to_numeric(
        df_clean["unit_price"],
        errors="coerce"
    )

    df_clean["order_date"] = pd.to_datetime(
        df_clean["order_date"],
        errors="coerce"
    )

    # Remove exact duplicate rows
    df_clean = df_clean.drop_duplicates()

    # Standardise text values
    df_clean["order_status"] = (
        df_clean["order_status"].str.strip().str.title()
    )

    df_clean["category"] = (
        df_clean["category"].str.strip().str.title()
    )

    # Identify valid transactions
    valid_transactions = df_clean[
        (df_clean["quantity"] > 0) &
        (df_clean["unit_price"] >= 0) &
        (df_clean["order_date"].notnull())
    ].copy()

    # Recalculate total amount
    valid_transactions["total_amount"] = (
        valid_transactions["quantity"] *
        valid_transactions["unit_price"]
    )

    return valid_transactions
