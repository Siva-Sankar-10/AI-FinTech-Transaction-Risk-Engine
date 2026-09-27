from __future__ import annotations

import math
from datetime import datetime
from random import Random


TRANSACTION_TYPES = [
    "PURCHASE",
    "TRANSFER",
    "BILL_PAYMENT",
    "ATM_WITHDRAWAL",
]

CHANNELS = [
    "MOBILE_APP",
    "WEB",
    "ATM",
    "POS",
]

PAYMENT_METHODS = [
    "UPI",
    "CARD",
    "BANK_TRANSFER",
    "NET_BANKING",
    "CASH",
]


def generate_normal_transaction(
    customer: dict,
    device: dict,
    beneficiary: dict | None,
    merchant: dict | None,
    timestamp: datetime,
    rng: Random,
) -> dict:
    """
    Generate a normal synthetic transaction based on
    the customer's expected behavior.
    """

    # ---------------------------------------------------------
    # Customer spending baseline
    # ---------------------------------------------------------

    avg_amount = float(
        customer["expected_avg_transaction_amount"]
    )

    # ---------------------------------------------------------
    # Generate realistic transaction amount
    # ---------------------------------------------------------

    amount = max(
        50.0,
        rng.lognormvariate(
            math.log(avg_amount),
            0.45,
        ),
    )

    # ---------------------------------------------------------
    # Transaction attributes
    # ---------------------------------------------------------

    transaction_type = rng.choice(
        TRANSACTION_TYPES
    )

    channel = rng.choice(
        CHANNELS
    )

    payment_method = rng.choice(
        PAYMENT_METHODS
    )

    # ---------------------------------------------------------
    # Merchant / location
    # ---------------------------------------------------------

    if merchant is not None:
        merchant_id = merchant["merchant_id"]
        location_city = merchant["city"]
    else:
        merchant_id = None
        location_city = customer["home_city"]

    # ---------------------------------------------------------
    # Beneficiary
    # ---------------------------------------------------------

    if beneficiary is not None:
        beneficiary_id = beneficiary["beneficiary_id"]
    else:
        beneficiary_id = None

    # ---------------------------------------------------------
    # Final transaction
    # ---------------------------------------------------------

    return {
        "timestamp": timestamp,
        "amount": round(amount, 2),
        "currency": "INR",
        "transaction_type": transaction_type,
        "merchant_id": merchant_id,
        "beneficiary_id": beneficiary_id,
        "device_id": device["device_id"],
        "location_city": location_city,
        "channel": channel,
        "payment_method": payment_method,
        "status": "SUCCESS",
        "is_fraud": 0,
        "fraud_type": "NORMAL",
    }