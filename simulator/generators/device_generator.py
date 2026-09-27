from __future__ import annotations

from random import Random

import pandas as pd


def generate_devices(
    customers: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic customer devices.
    """

    rng = Random(seed)

    device_types = [
        "MOBILE",
        "WEB",
        "TABLET",
    ]

    operating_systems = [
        "ANDROID",
        "IOS",
        "WINDOWS",
        "MACOS",
        "LINUX",
    ]

    rows = []

    for _, customer in customers.iterrows():

        customer_id = customer["customer_id"]

        device_count = rng.choices(
            [1, 2, 3],
            weights=[55, 35, 10],
            k=1,
        )[0]

        for device_number in range(1, device_count + 1):

            device_type = rng.choice(device_types)

            if device_type == "MOBILE":
                os = rng.choice(["ANDROID", "IOS"])
            elif device_type == "TABLET":
                os = rng.choice(["ANDROID", "IOS"])
            else:
                os = rng.choice(
                    ["WINDOWS", "MACOS", "LINUX"]
                )

            rows.append(
                {
                    "device_id": (
                        f"DEV{len(rows) + 1:07d}"
                    ),
                    "customer_id": customer_id,
                    "device_type": device_type,
                    "os": os,
                    "trusted": (
                        True
                        if device_number == 1
                        else rng.random() < 0.70
                    ),
                    "device_age_days": rng.randint(
                        1,
                        1500,
                    ),
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    from customer_generator import generate_customers

    customers = generate_customers()

    devices = generate_devices(customers)

    print("=" * 70)
    print("DEVICE GENERATOR TEST")
    print("=" * 70)
    print(f"Customers : {len(customers):,}")
    print(f"Devices   : {len(devices):,}")
    print()
    print(devices.head())
    print()
    print(devices["device_type"].value_counts())