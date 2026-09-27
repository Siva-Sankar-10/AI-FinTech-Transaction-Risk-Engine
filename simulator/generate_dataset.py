from __future__ import annotations

import json
from pathlib import Path

from simulator.generators.account_generator import (
    generate_accounts,
)
from simulator.generators.beneficiary_generator import (
    generate_beneficiaries,
)
from simulator.generators.customer_generator import (
    generate_customers,
)
from simulator.generators.device_generator import (
    generate_devices,
)
from simulator.generators.merchant_generator import (
    generate_merchants,
)
from simulator.generators.transaction_generator import (
    generate_transactions,
)


SEED = 42

N_CUSTOMERS = 10_000
N_MERCHANTS = 2_000
N_TRANSACTIONS = 100_000

FRAUD_RATE = 0.05

OUTPUT_DIR = Path(
    "data/raw/synthetic"
)


def main() -> None:

    print("=" * 70)
    print("AI FINTECH TRANSACTION RISK ENGINE")
    print("SYNTHETIC DATASET GENERATOR")
    print("=" * 70)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------
    # Customers
    # ---------------------------------------------------------

    print("\n[1/6] Generating customers...")

    customers = generate_customers(
        n_customers=N_CUSTOMERS,
        seed=SEED,
    )

    print(
        f"      Customers: {len(customers):,}"
    )

    # ---------------------------------------------------------
    # Accounts
    # ---------------------------------------------------------

    print("\n[2/6] Generating accounts...")

    accounts = generate_accounts(
        customers=customers,
        seed=SEED,
    )

    print(
        f"      Accounts: {len(accounts):,}"
    )

    # ---------------------------------------------------------
    # Devices
    # ---------------------------------------------------------

    print("\n[3/6] Generating devices...")

    devices = generate_devices(
        customers=customers,
        seed=SEED,
    )

    print(
        f"      Devices: {len(devices):,}"
    )

    # ---------------------------------------------------------
    # Beneficiaries
    # ---------------------------------------------------------

    print("\n[4/6] Generating beneficiaries...")

    beneficiaries = generate_beneficiaries(
        customers=customers,
        seed=SEED,
    )

    print(
        f"      Beneficiaries: {len(beneficiaries):,}"
    )

    # ---------------------------------------------------------
    # Merchants
    # ---------------------------------------------------------

    print("\n[5/6] Generating merchants...")

    merchants = generate_merchants(
        n_merchants=N_MERCHANTS,
        seed=SEED,
    )

    print(
        f"      Merchants: {len(merchants):,}"
    )

    # ---------------------------------------------------------
    # Transactions
    # ---------------------------------------------------------

    print("\n[6/6] Generating transactions...")

    transactions = generate_transactions(
        customers=customers,
        accounts=accounts,
        devices=devices,
        beneficiaries=beneficiaries,
        merchants=merchants,
        n_transactions=N_TRANSACTIONS,
        fraud_rate=FRAUD_RATE,
        seed=SEED,
    )

    print(
        f"      Transactions: {len(transactions):,}"
    )

    # ---------------------------------------------------------
    # Save entity tables
    # ---------------------------------------------------------

    customers.to_csv(
        OUTPUT_DIR / "customers.csv",
        index=False,
    )

    accounts.to_csv(
        OUTPUT_DIR / "accounts.csv",
        index=False,
    )

    devices.to_csv(
        OUTPUT_DIR / "devices.csv",
        index=False,
    )

    beneficiaries.to_csv(
        OUTPUT_DIR / "beneficiaries.csv",
        index=False,
    )

    merchants.to_csv(
        OUTPUT_DIR / "merchants.csv",
        index=False,
    )

    transactions.to_csv(
        OUTPUT_DIR / "transactions.csv",
        index=False,
    )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata = {
        "dataset_name": (
            "synthetic_fintech_transaction_dataset"
        ),
        "version": "0.1.0",
        "seed": SEED,
        "customers": len(customers),
        "accounts": len(accounts),
        "devices": len(devices),
        "beneficiaries": len(beneficiaries),
        "merchants": len(merchants),
        "transactions": len(transactions),
        "configured_fraud_rate": FRAUD_RATE,
        "actual_fraud_rate": round(
            float(
                transactions["is_fraud"].mean()
            ),
            6,
        ),
        "date_min": str(
            transactions["timestamp"].min()
        ),
        "date_max": str(
            transactions["timestamp"].max()
        ),
        "currency": "INR",
        "synthetic": True,
        "contains_real_pii": False,
    }

    with open(
        OUTPUT_DIR / "metadata.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
        )

    # ---------------------------------------------------------
    # Final summary
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATASET GENERATION COMPLETE")
    print("=" * 70)

    print(
        f"Customers       : {len(customers):,}"
    )

    print(
        f"Accounts        : {len(accounts):,}"
    )

    print(
        f"Devices         : {len(devices):,}"
    )

    print(
        f"Beneficiaries   : {len(beneficiaries):,}"
    )

    print(
        f"Merchants       : {len(merchants):,}"
    )

    print(
        f"Transactions    : {len(transactions):,}"
    )

    print(
        f"Fraud rate      : "
        f"{transactions['is_fraud'].mean() * 100:.2f}%"
    )

    print(
        f"Output directory: {OUTPUT_DIR}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()