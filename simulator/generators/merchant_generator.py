from __future__ import annotations

from random import Random

import pandas as pd


def generate_merchants(
    n_merchants: int = 2_000,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic merchants.
    """

    rng = Random(seed)

    merchant_categories = [
        "GROCERY",
        "RESTAURANT",
        "E_COMMERCE",
        "TRAVEL",
        "FUEL",
        "ENTERTAINMENT",
        "HEALTHCARE",
        "EDUCATION",
        "UTILITIES",
        "ELECTRONICS",
        "FASHION",
        "OTHER",
    ]

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

    risk_categories = [
        "LOW",
        "MEDIUM",
        "HIGH",
    ]

    rows = []

    for i in range(1, n_merchants + 1):

        category = rng.choice(merchant_categories)

        risk = rng.choices(
            risk_categories,
            weights=[70, 25, 5],
            k=1,
        )[0]

        rows.append(
            {
                "merchant_id": f"MER{i:06d}",
                "merchant_category": category,
                "city": rng.choice(cities),
                "country": "IN",
                "risk_category": risk,
            }
        )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    merchants = generate_merchants()

    print("=" * 70)
    print("MERCHANT GENERATOR TEST")
    print("=" * 70)
    print(f"Merchants : {len(merchants):,}")
    print()
    print(merchants.head())
    print()
    print(merchants["merchant_category"].value_counts())
    print()
    print(merchants["risk_category"].value_counts())