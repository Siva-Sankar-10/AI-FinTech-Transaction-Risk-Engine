from __future__ import annotations

from datetime import date, timedelta
from random import Random

import pandas as pd


CUSTOMER_SEGMENTS = [
    "RETAIL",
    "PREMIUM",
    "BUSINESS",
]

ACCOUNT_TYPES = [
    "SAVINGS",
    "CURRENT",
]


def generate_customers(
    n_customers: int = 10_000,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic customer profiles.

    The generated data contains no real PII.
    """

    rng = Random(seed)

    cities = [
        "Chennai",
        "Bengaluru",
        "Hyderabad",
        "Mumbai",
        "Delhi",
        "Pune",
        "Coimbatore",
        "Kochi",
        "Madurai",
        "Visakhapatnam",
    ]

    today = date(2026, 1, 1)

    rows = []

    for i in range(1, n_customers + 1):
        segment = rng.choices(
            CUSTOMER_SEGMENTS,
            weights=[75, 15, 10],
            k=1,
        )[0]

        if segment == "RETAIL":
            avg_amount = rng.uniform(500, 5000)
            daily_frequency = rng.uniform(2, 10)
        elif segment == "PREMIUM":
            avg_amount = rng.uniform(3000, 25000)
            daily_frequency = rng.uniform(3, 15)
        else:
            avg_amount = rng.uniform(10000, 200000)
            daily_frequency = rng.uniform(5, 30)

        account_age_days = rng.randint(90, 3650)

        rows.append(
            {
                "customer_id": f"CUST{i:06d}",
                "customer_segment": segment,
                "account_type": rng.choice(ACCOUNT_TYPES),
                "account_age_days": account_age_days,
                "home_city": rng.choice(cities),
                "expected_avg_transaction_amount": round(avg_amount, 2),
                "expected_daily_transaction_count": round(
                    daily_frequency,
                    2,
                ),
                "preferred_transaction_start_hour": rng.randint(7, 10),
                "preferred_transaction_end_hour": rng.randint(20, 23),
                "customer_since": (
                    today - timedelta(days=account_age_days)
                ).isoformat(),
            }
        )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_customers()

    print("=" * 70)
    print("CUSTOMER GENERATOR TEST")
    print("=" * 70)
    print(f"Customers generated : {len(df):,}")
    print()
    print(df.head())
    print()
    print(df["customer_segment"].value_counts())