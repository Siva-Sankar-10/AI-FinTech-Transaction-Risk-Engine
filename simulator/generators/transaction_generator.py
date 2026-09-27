from __future__ import annotations

from datetime import datetime, timedelta
from random import Random

import pandas as pd

from simulator.scenarios.fraud import (
    FRAUD_TYPES,
    generate_fraud_transaction,
)
from simulator.scenarios.normal import (
    generate_normal_transaction,
)


def generate_transactions(
    customers: pd.DataFrame,
    accounts: pd.DataFrame,
    devices: pd.DataFrame,
    beneficiaries: pd.DataFrame,
    merchants: pd.DataFrame,
    n_transactions: int = 100_000,
    fraud_rate: float = 0.05,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a chronological synthetic transaction dataset.

    All transaction attributes are linked to the synthetic
    customer/account/device/beneficiary/merchant entities.
    """

    if not 0 < fraud_rate < 1:
        raise ValueError("fraud_rate must be between 0 and 1")

    rng = Random(seed)

    # ---------------------------------------------------------
    # Build lookup tables
    # ---------------------------------------------------------

    customer_records = customers.to_dict("records")
    account_records = accounts.to_dict("records")
    device_records = devices.to_dict("records")
    beneficiary_records = beneficiaries.to_dict("records")
    merchant_records = merchants.to_dict("records")

    accounts_by_customer: dict[str, list[dict]] = {}

    for account in account_records:
        accounts_by_customer.setdefault(
            account["customer_id"],
            [],
        ).append(account)

    devices_by_customer: dict[str, list[dict]] = {}

    for device in device_records:
        devices_by_customer.setdefault(
            device["customer_id"],
            [],
        ).append(device)

    beneficiaries_by_customer: dict[str, list[dict]] = {}

    for beneficiary in beneficiary_records:
        beneficiaries_by_customer.setdefault(
            beneficiary["customer_id"],
            [],
        ).append(beneficiary)

    # ---------------------------------------------------------
    # Date range
    # ---------------------------------------------------------

    start_datetime = datetime(2025, 1, 1, 0, 0, 0)

    end_datetime = datetime(2025, 8, 31, 23, 59, 59)

    total_seconds = int(
        (end_datetime - start_datetime).total_seconds()
    )

    rows = []

    for transaction_number in range(
        1,
        n_transactions + 1,
    ):

        # -----------------------------------------------------
        # Select customer
        # -----------------------------------------------------

        customer = rng.choice(customer_records)

        customer_id = customer["customer_id"]

        # -----------------------------------------------------
        # Select customer's account
        # -----------------------------------------------------

        customer_accounts = accounts_by_customer.get(
            customer_id,
            [],
        )

        if not customer_accounts:
            continue

        account = rng.choice(customer_accounts)

        # -----------------------------------------------------
        # Select customer's device
        # -----------------------------------------------------

        customer_devices = devices_by_customer.get(
            customer_id,
            [],
        )

        if not customer_devices:
            continue

        device = rng.choice(customer_devices)

        # -----------------------------------------------------
        # Select beneficiary
        # -----------------------------------------------------

        customer_beneficiaries = (
            beneficiaries_by_customer.get(
                customer_id,
                [],
            )
        )

        beneficiary = None

        if customer_beneficiaries:
            beneficiary = rng.choice(
                customer_beneficiaries
            )

        # -----------------------------------------------------
        # Select merchant
        # -----------------------------------------------------

        merchant = rng.choice(
            merchant_records
        )

        # -----------------------------------------------------
        # Generate timestamp
        # -----------------------------------------------------

        timestamp = (
            start_datetime
            + timedelta(
                seconds=rng.randint(
                    0,
                    total_seconds,
                )
            )
        )

        # -----------------------------------------------------
        # Decide normal vs fraud
        # -----------------------------------------------------

        is_fraud = rng.random() < fraud_rate

        if is_fraud:

            fraud_type = rng.choice(
                FRAUD_TYPES
            )

            transaction = generate_fraud_transaction(
                customer=customer,
                device=device,
                beneficiary=beneficiary,
                merchant=merchant,
                timestamp=timestamp,
                rng=rng,
                fraud_type=fraud_type,
            )

        else:

            transaction = generate_normal_transaction(
                customer=customer,
                device=device,
                beneficiary=beneficiary,
                merchant=merchant,
                timestamp=timestamp,
                rng=rng,
            )

        # -----------------------------------------------------
        # Add entity identifiers
        # -----------------------------------------------------

        transaction["transaction_id"] = (
            f"TXN{transaction_number:08d}"
        )

        transaction["customer_id"] = customer_id

        transaction["account_id"] = account[
            "account_id"
        ]

        rows.append(transaction)

    df = pd.DataFrame(rows)

    # ---------------------------------------------------------
    # Sort chronologically
    # ---------------------------------------------------------

    df = df.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    return df