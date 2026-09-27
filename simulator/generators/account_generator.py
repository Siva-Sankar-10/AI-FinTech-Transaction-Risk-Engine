from __future__ import annotations

from random import Random

import pandas as pd


def generate_accounts(
    customers: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic accounts associated with customers.
    """

    rng = Random(seed)

    rows = []

    for _, customer in customers.iterrows():
        customer_id = customer["customer_id"]

        # Most customers have one account.
        # Some have two.
        account_count = rng.choices(
            [1, 2],
            weights=[85, 15],
            k=1,
        )[0]

        for account_number in range(1, account_count + 1):

            if account_number == 1:
                account_type = customer["account_type"]
            else:
                account_type = (
                    "CURRENT"
                    if customer["account_type"] == "SAVINGS"
                    else "SAVINGS"
                )

            rows.append(
                {
                    "account_id": (
                        f"ACC{len(rows) + 1:07d}"
                    ),
                    "customer_id": customer_id,
                    "account_type": account_type,
                    "account_age_days": max(
                        30,
                        int(customer["account_age_days"])
                        - rng.randint(0, 180),
                    ),
                    "status": rng.choices(
                        ["ACTIVE", "DORMANT"],
                        weights=[98, 2],
                        k=1,
                    )[0],
                    "currency": "INR",
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    from customer_generator import generate_customers

    customers = generate_customers()

    accounts = generate_accounts(customers)

    print("=" * 70)
    print("ACCOUNT GENERATOR TEST")
    print("=" * 70)
    print(f"Customers : {len(customers):,}")
    print(f"Accounts  : {len(accounts):,}")
    print()
    print(accounts.head())
    print()
    print(accounts["status"].value_counts())