from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/raw/synthetic")


def test_dataset_files_exist():
    required_files = [
        "customers.csv",
        "accounts.csv",
        "devices.csv",
        "beneficiaries.csv",
        "merchants.csv",
        "transactions.csv",
        "metadata.json",
    ]

    for filename in required_files:
        assert (DATA_DIR / filename).exists(), f"Missing file: {filename}"


def test_transaction_dataset():
    df = pd.read_csv(DATA_DIR / "transactions.csv")

    # ---------------------------------------------------------
    # Row count
    # ---------------------------------------------------------

    assert len(df) == 100_000

    # ---------------------------------------------------------
    # Required columns
    # ---------------------------------------------------------

    required_columns = [
        "transaction_id",
        "customer_id",
        "account_id",
        "timestamp",
        "amount",
        "currency",
        "transaction_type",
        "merchant_id",
        "beneficiary_id",
        "device_id",
        "location_city",
        "channel",
        "payment_method",
        "status",
        "is_fraud",
        "fraud_type",
    ]

    for column in required_columns:
        assert column in df.columns, f"Missing column: {column}"

    # ---------------------------------------------------------
    # Transaction IDs
    # ---------------------------------------------------------

    assert df["transaction_id"].is_unique

    # ---------------------------------------------------------
    # Duplicate rows
    # ---------------------------------------------------------

    assert df.duplicated().sum() == 0

    # ---------------------------------------------------------
    # Required non-null fields
    # ---------------------------------------------------------

    required_non_null = [
        "transaction_id",
        "customer_id",
        "account_id",
        "timestamp",
        "amount",
        "currency",
        "transaction_type",
        "device_id",
        "channel",
        "payment_method",
        "status",
        "is_fraud",
        "fraud_type",
    ]

    for column in required_non_null:
        assert df[column].notna().all(), (
            f"Null values found in required column: {column}"
        )

    # ---------------------------------------------------------
    # Amount validation
    # ---------------------------------------------------------

    assert (df["amount"] > 0).all()

    # ---------------------------------------------------------
    # Fraud label validation
    # ---------------------------------------------------------

    assert set(df["is_fraud"].unique()).issubset({0, 1})

    # Normal transactions must have fraud_type NORMAL
    assert (
        df.loc[
            df["is_fraud"] == 0,
            "fraud_type",
        ]
        == "NORMAL"
    ).all()

    # Fraud transactions must not have fraud_type NORMAL
    assert (
        df.loc[
            df["is_fraud"] == 1,
            "fraud_type",
        ]
        != "NORMAL"
    ).all()

    # ---------------------------------------------------------
    # Timestamp validation
    # ---------------------------------------------------------

    timestamps = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
    )

    assert timestamps.notna().all()

    # ---------------------------------------------------------
    # Currency validation
    # ---------------------------------------------------------

    assert set(df["currency"].unique()) == {"INR"}

    # ---------------------------------------------------------
    # Status validation
    # ---------------------------------------------------------

    assert set(
        df["status"].unique()
    ).issubset(
        {
            "SUCCESS",
            "FAILED",
            "PENDING",
        }
    )


def test_customer_integrity():
    customers = pd.read_csv(
        DATA_DIR / "customers.csv"
    )

    assert customers["customer_id"].is_unique

    assert customers["customer_id"].notna().all()


def test_account_integrity():
    customers = pd.read_csv(
        DATA_DIR / "customers.csv"
    )

    accounts = pd.read_csv(
        DATA_DIR / "accounts.csv"
    )

    customer_ids = set(
        customers["customer_id"]
    )

    assert accounts["account_id"].is_unique

    assert accounts["account_id"].notna().all()

    assert accounts["customer_id"].isin(
        customer_ids
    ).all()


def test_device_integrity():
    customers = pd.read_csv(
        DATA_DIR / "customers.csv"
    )

    devices = pd.read_csv(
        DATA_DIR / "devices.csv"
    )

    customer_ids = set(
        customers["customer_id"]
    )

    assert devices["device_id"].is_unique

    assert devices["device_id"].notna().all()

    assert devices["customer_id"].isin(
        customer_ids
    ).all()


def test_beneficiary_integrity():
    customers = pd.read_csv(
        DATA_DIR / "customers.csv"
    )

    beneficiaries = pd.read_csv(
        DATA_DIR / "beneficiaries.csv"
    )

    customer_ids = set(
        customers["customer_id"]
    )

    assert beneficiaries[
        "beneficiary_id"
    ].is_unique

    assert beneficiaries[
        "beneficiary_id"
    ].notna().all()

    assert beneficiaries[
        "customer_id"
    ].isin(
        customer_ids
    ).all()


def test_merchant_integrity():
    merchants = pd.read_csv(
        DATA_DIR / "merchants.csv"
    )

    assert merchants[
        "merchant_id"
    ].is_unique

    assert merchants[
        "merchant_id"
    ].notna().all()


def test_transaction_foreign_keys():
    transactions = pd.read_csv(
        DATA_DIR / "transactions.csv"
    )

    customers = pd.read_csv(
        DATA_DIR / "customers.csv"
    )

    accounts = pd.read_csv(
        DATA_DIR / "accounts.csv"
    )

    devices = pd.read_csv(
        DATA_DIR / "devices.csv"
    )

    beneficiaries = pd.read_csv(
        DATA_DIR / "beneficiaries.csv"
    )

    merchants = pd.read_csv(
        DATA_DIR / "merchants.csv"
    )

    # ---------------------------------------------------------
    # Customer foreign key
    # ---------------------------------------------------------

    assert transactions[
        "customer_id"
    ].isin(
        customers["customer_id"]
    ).all()

    # ---------------------------------------------------------
    # Account foreign key
    # ---------------------------------------------------------

    assert transactions[
        "account_id"
    ].isin(
        accounts["account_id"]
    ).all()

    # ---------------------------------------------------------
    # Device foreign key
    # ---------------------------------------------------------

    assert transactions[
        "device_id"
    ].isin(
        devices["device_id"]
    ).all()

    # ---------------------------------------------------------
    # Beneficiary foreign key
    #
    # beneficiary_id is nullable because some transactions
    # may legitimately have no beneficiary.
    # Only validate non-null IDs.
    # ---------------------------------------------------------

    beneficiary_mask = (
        transactions["beneficiary_id"].notna()
    )

    assert transactions.loc[
        beneficiary_mask,
        "beneficiary_id",
    ].isin(
        beneficiaries["beneficiary_id"]
    ).all()

    # ---------------------------------------------------------
    # Merchant foreign key
    #
    # merchant_id is also nullable for transactions that
    # don't involve a merchant.
    # ---------------------------------------------------------

    merchant_mask = (
        transactions["merchant_id"].notna()
    )

    assert transactions.loc[
        merchant_mask,
        "merchant_id",
    ].isin(
        merchants["merchant_id"]
    ).all()


if __name__ == "__main__":
    print(
        "Running dataset validation..."
    )

    test_dataset_files_exist()

    test_transaction_dataset()

    test_customer_integrity()

    test_account_integrity()

    test_device_integrity()

    test_beneficiary_integrity()

    test_merchant_integrity()

    test_transaction_foreign_keys()

    print(
        "DATASET VALIDATION PASSED"
    )