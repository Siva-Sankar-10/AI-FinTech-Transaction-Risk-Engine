from __future__ import annotations

from random import Random

import pandas as pd


def generate_beneficiaries(
    customers: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic beneficiaries linked to customers.
    """

    rng = Random(seed)

    rows = []

    for _, customer in customers.iterrows():

        customer_id = customer["customer_id"]

        beneficiary_count = rng.choices(
            [0, 1, 2, 3, 4],
            weights=[10, 25, 30, 20, 15],
            k=1,
        )[0]

        for _ in range(beneficiary_count):

            rows.append(
                {
                    "beneficiary_id": (
                        f"BEN{len(rows) + 1:07d}"
                    ),
                    "customer_id": customer_id,
                    "beneficiary_type": rng.choice(
                        [
                            "PERSONAL",
                            "MERCHANT",
                            "BUSINESS",
                        ]
                    ),
                    "trusted": rng.random() < 0.85,
                    "beneficiary_age_days": rng.randint(
                        1,
                        2500,
                    ),
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    from customer_generator import generate_customers

    customers = generate_customers()

    beneficiaries = generate_beneficiaries(customers)

    print("=" * 70)
    print("BENEFICIARY GENERATOR TEST")
    print("=" * 70)
    print(f"Customers      : {len(customers):,}")
    print(f"Beneficiaries  : {len(beneficiaries):,}")
    print()

    if not beneficiaries.empty:
        print(beneficiaries.head())
        print()
        print(
            beneficiaries["beneficiary_type"].value_counts()
        )