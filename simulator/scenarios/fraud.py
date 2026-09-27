from __future__ import annotations

from datetime import datetime
from random import Random


FRAUD_TYPES = [
    "ACCOUNT_TAKEOVER",
    "VELOCITY_FRAUD",
    "AMOUNT_ANOMALY",
    "NEW_BENEFICIARY",
    "DEVICE_COMPROMISE",
    "UNUSUAL_BEHAVIOR",
]


def generate_fraud_transaction(
    customer: dict,
    device: dict,
    beneficiary: dict | None,
    merchant: dict | None,
    timestamp: datetime,
    rng: Random,
    fraud_type: str | None = None,
) -> dict:

    if fraud_type is None:
        fraud_type = rng.choice(FRAUD_TYPES)

    avg_amount = float(
        customer["expected_avg_transaction_amount"]
    )

    amount = avg_amount
    location_city = customer["home_city"]

    merchant_id = None
    beneficiary_id = None

    if merchant is not None:
        merchant_id = merchant["merchant_id"]

    if beneficiary is not None:
        beneficiary_id = beneficiary["beneficiary_id"]

    channel = rng.choice(
        [
            "MOBILE_APP",
            "WEB",
            "ATM",
        ]
    )

    payment_method = rng.choice(
        [
            "UPI",
            "CARD",
            "BANK_TRANSFER",
            "NET_BANKING",
        ]
    )

    if fraud_type == "ACCOUNT_TAKEOVER":

        amount = avg_amount * rng.uniform(3.0, 8.0)

        channel = "MOBILE_APP"
        payment_method = "BANK_TRANSFER"

        location_city = rng.choice(
            [
                "Mumbai",
                "Delhi",
                "Bengaluru",
                "Hyderabad",
                "Pune",
            ]
        )

    elif fraud_type == "VELOCITY_FRAUD":

        amount = avg_amount * rng.uniform(1.2, 3.0)

        channel = "MOBILE_APP"

    elif fraud_type == "AMOUNT_ANOMALY":

        amount = avg_amount * rng.uniform(5.0, 15.0)

    elif fraud_type == "NEW_BENEFICIARY":

        amount = avg_amount * rng.uniform(2.0, 6.0)

        payment_method = "BANK_TRANSFER"

    elif fraud_type == "DEVICE_COMPROMISE":

        amount = avg_amount * rng.uniform(2.0, 7.0)

        location_city = rng.choice(
            [
                "Chennai",
                "Bengaluru",
                "Mumbai",
                "Delhi",
                "Hyderabad",
            ]
        )

    elif fraud_type == "UNUSUAL_BEHAVIOR":

        amount = avg_amount * rng.uniform(2.0, 5.0)

        location_city = rng.choice(
            [
                "Kochi",
                "Pune",
                "Delhi",
                "Mumbai",
            ]
        )

    return {
        "timestamp": timestamp,
        "amount": round(max(50.0, amount), 2),
        "currency": "INR",
        "transaction_type": rng.choice(
            [
                "PURCHASE",
                "TRANSFER",
                "BILL_PAYMENT",
                "ATM_WITHDRAWAL",
            ]
        ),
        "merchant_id": merchant_id,
        "beneficiary_id": beneficiary_id,
        "device_id": device["device_id"],
        "location_city": location_city,
        "channel": channel,
        "payment_method": payment_method,
        "status": "SUCCESS",
        "is_fraud": 1,
        "fraud_type": fraud_type,
    }