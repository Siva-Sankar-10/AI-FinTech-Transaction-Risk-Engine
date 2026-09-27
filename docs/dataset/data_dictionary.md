*# AI FinTech Transaction Risk Engine*

*# Canonical Data Dictionary*



*## Customer*



*| Field | Type | Description |*

*|---|---|---|*

*| customer\_id | string | Unique synthetic customer identifier |*

*| customer\_segment | string | Customer category |*

*| account\_age\_days | integer | Age of customer account |*

*| home\_city | string | Customer's normal city |*

*| account\_type | string | Savings/current/business |*



*## Account*



*| Field | Type | Description |*

*|---|---|---|*

*| account\_id | string | Unique account identifier |*

*| customer\_id | string | Associated customer |*

*| account\_type | string | Type of account |*

*| account\_age\_days | integer | Account age |*

*| status | string | Account status |*



*## Device*



*| Field | Type | Description |*

*|---|---|---|*

*| device\_id | string | Unique device identifier |*

*| customer\_id | string | Associated customer |*

*| device\_type | string | Mobile/web/desktop |*

*| os | string | Operating system |*

*| first\_seen | datetime | First observed date |*

*| trusted | integer | Whether device is trusted |*



*## Beneficiary*



*| Field | Type | Description |*

*|---|---|---|*

*| beneficiary\_id | string | Unique beneficiary |*

*| customer\_id | string | Associated customer |*

*| first\_added | datetime | Date beneficiary was added |*

*| trusted | integer | Trusted status |*



*## Merchant*



*| Field | Type | Description |*

*|---|---|---|*

*| merchant\_id | string | Unique merchant |*

*| merchant\_category | string | Merchant category |*

*| city | string | Merchant city |*

*| country | string | Merchant country |*

*| risk\_category | string | Merchant risk category |*



*## Transaction*



*| Field | Type | Description |*

*|---|---|---|*

*| transaction\_id | string | Unique transaction |*

*| customer\_id | string | Customer performing transaction |*

*| account\_id | string | Account used |*

*| timestamp | datetime | Transaction timestamp |*

*| amount | float | Transaction amount |*

*| currency | string | Transaction currency |*

*| transaction\_type | string | Purchase/transfer/etc |*

*| merchant\_id | string | Merchant if applicable |*

*| beneficiary\_id | string | Beneficiary if applicable |*

*| device\_id | string | Device used |*

*| location\_city | string | Transaction location |*

*| channel | string | Mobile/web/ATM/etc |*

*| payment\_method | string | UPI/card/bank transfer/etc |*

*| status | string | Transaction status |*

*| is\_fraud | integer | Ground-truth fraud label |*

*| fraud\_type | string | Fraud category |*

