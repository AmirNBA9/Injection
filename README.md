# NoSQL Injection Detection Using Machine Learning

> A research project for detecting NoSQL (MongoDB) injection attacks using supervised machine learning models. This work is part of a thesis project focused on binary classification of malicious vs. benign NoSQL queries.

---

## Table of Contents

- [Overview](#overview)
- [NoSQL Injection Attack Patterns](#nosql-injection-attack-patterns)
- [Dataset](#dataset)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Machine Learning Models & Results](#machine-learning-models--results)
- [Workflow](#workflow)
- [References](#references)

---

## Overview

NoSQL databases (especially MongoDB) are increasingly targeted by injection attacks that exploit query operators and JavaScript execution. This project builds a complete ML pipeline to detect such attacks by:

1. **Collecting** and labeling NoSQL query patterns (benign & malicious)
2. **Extracting** 18 numeric features from each query
3. **Training** multiple ML classifiers with cross-validation
4. **Evaluating** models using accuracy, precision, recall, F1-score, and ROC-AUC

---

## NoSQL Injection Attack Patterns

Below are examples of common MongoDB injection payloads that this project aims to detect:

```javascript
// Operator-based injection
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": {"$gt": ""}, "password": {"$gt": ""}}
{"username": {"$in": ["Admin", "admin", "root"]}, "password": {"$gt": ""}}

// JavaScript injection
$where: '1 == 1'
true, $where: '1 == 1'

// Time-based blind injection
';sleep(5000);
';it=new Date();do{pt=new Date();}while(pt-it<5000);

// Database manipulation
db.injection.insert({success:1});
db.dropDatabase();

// Regex-based injection
' && this.password.match(/.*/)//+%00

// URL-encoded payloads
'%20%26%26%20this.password.match(/.*/)//+%00
```

---

## Dataset

| Property          | Value                                   |
|-------------------|-----------------------------------------|
| **Base records**  | 400 labeled NoSQL queries               |
| **Synthetic data**| Expanded to 2,000 records               |
| **Train/Test**    | 80% / 20% stratified split              |
| **Label 0**       | Benign (~22%)                           |
| **Label 1**       | Malicious (~78%)                        |
| **Missing values**| None (after preprocessing)              |

---

## Features

18 numeric features are extracted from each NoSQL query:

| # | Feature                    | Description                              |
|---|----------------------------|------------------------------------------|
| 1 | `num_keys`                 | Number of keys in the query              |
| 2 | `num_operators`            | Count of MongoDB operators (`$ne`, `$gt`, ...) |
| 3 | `length_user_value`        | Length of the user-supplied value         |
| 4 | `length_password_value`    | Length of the password value              |
| 5 | `length_username_value`    | Length of the username value              |
| 6 | `contains_email_pattern`   | Whether an email pattern is present      |
| 7 | `contains_ip_pattern`      | Whether an IP address pattern is present |
| 8 | `nested_keys_exist`        | Presence of nested keys                  |
| 9 | `num_nested_keys`          | Count of nested keys                     |
| 10| `contains_numeric_values`  | Whether numeric values are present       |
| 11| `contains_boolean_values`  | Whether boolean values are present       |
| 12| `contains_empty_strings`   | Whether empty strings are present        |
| 13| `contains_fixed_values`    | Whether fixed/hardcoded values are present |
| 14| `unique_key_count`         | Number of unique keys                    |
| 15| `data_type_diversity`      | Diversity of data types in the query     |
| 16| `total_record_length`      | Total character length of the record     |
| 17| `special_characters_exist` | Whether special characters are present   |
| 18| `nested_depth`             | Maximum nesting depth of the query       |

---

## Project Structure

```
Injection/
├── README.md                          # Project documentation
├── NoSQLDetectionv2.ipynb             # Main ML training & evaluation notebook
├── splitData.ipynb                    # Train/test split utility
├── AnalyticsOfDataset.py              # Dataset generation & analysis
├── Set_DataToMongo.py                 # Import data into MongoDB
├── Del_RedundantRecord.py             # Remove duplicate records from MongoDB
├── finaldataset.json                  # Raw labeled dataset (JSON)
├── Thesis_V3.1.docx                   # Thesis document (v3.1)
├── Thesis_V3.2.docx                   # Thesis document (v3.2)
└── Final/                             # Processed CSV datasets
    ├── data400.csv                    # Original 400-record dataset
    ├── train.csv                      # Full training set
    ├── train80.csv                    # 80% training split
    ├── test.csv                       # Full test set
    ├── test20.csv                     # 20% test split
    ├── synthetic_data_2000_*.csv      # Synthetic datasets (from 400 base)
    └── synthetic_from_train_*.csv     # Synthetic datasets (from train split)
```

---

## Installation

### Prerequisites

- Python 3.8+
- MongoDB (running on `localhost:27017`)

### Install Dependencies

```bash
pip install pandas numpy scikit-learn xgboost imbalanced-learn matplotlib seaborn plotly pymongo
```

---

## Usage

### 1. Generate & Analyze Dataset

```bash
python AnalyticsOfDataset.py
```

This script collects NoSQL query patterns, labels them as benign/malicious, removes near-duplicates using Jaccard similarity, and exports `finaldataset.json`.

### 2. Import Data into MongoDB

```bash
python Set_DataToMongo.py
```

Connects to MongoDB at `localhost:27017`, reads `finaldataset.json`, and inserts the records into the `dataset.imp` collection. Make sure MongoDB is running before executing this script.

### 3. Remove Duplicate Records (Optional)

```bash
python Del_RedundantRecord.py
```

Identifies and removes duplicate documents from MongoDB, keeping the most recent entry based on `createdAt`.

### 4. Split Dataset

Open and run `splitData.ipynb` in Jupyter Notebook. This performs an 80/20 stratified split, preserving the label distribution.

### 5. Train & Evaluate Models

Open and run `NoSQLDetectionv2.ipynb` in Jupyter Notebook. This notebook handles:
- Data loading & preprocessing
- Feature selection (correlation-based)
- Class balancing with SMOTE
- Feature scaling with StandardScaler
- Training 7 classifiers
- 10-fold Stratified K-Fold cross-validation
- Performance visualization (confusion matrices, ROC curves)

---

## Machine Learning Models & Results

| Model                | Accuracy  | AUC    |
|----------------------|-----------|--------|
| Logistic Regression  | ~78%      | ~85%   |
| Decision Tree        | ~76%      | ~73%   |
| Random Forest        | ~81%      | ~89%   |
| Gradient Boosting    | ~81%      | ~89%   |
| **XGBoost**          | **~83%**  | **~90%** |
| KNN                  | ~79%      | ~86%   |
| Ensemble (Voting)    | ~82%      | ~90%   |

> **Best performer: XGBoost** with ~82.8% accuracy and ~90.3% AUC.

### Techniques Used

- **SMOTE** — Synthetic Minority Over-sampling to handle class imbalance
- **StandardScaler** — Feature normalization
- **StratifiedKFold** — 10-fold cross-validation preserving class ratios
- **Correlation-based feature selection** — Removing highly correlated features

---

## Workflow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Data Collection │───>│  Feature         │───>│  Train/Test     │
│  & Labeling      │    │  Extraction      │    │  Split (80/20)  │
│  (400 queries)   │    │  (18 features)   │    │  Stratified     │
└─────────────────┘    └──────────────────┘    └────────┬────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐    ┌────────▼────────┐
│  Evaluation &    │<───│  Model Training  │<───│  Preprocessing  │
│  Comparison      │    │  (7 classifiers) │    │  SMOTE + Scaling│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## References

1. [Wikipedia — NoSQL](https://en.wikipedia.org/wiki/NoSQL)
2. [NoSQL Database Directory](http://nosql-database.org/)
3. [NoSQLi — Go-based scanner](https://github.com/Charlie-belmer/nosqli)
4. [PayloadsAllTheThings — NoSQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection)
5. [OWASP — Testing for NoSQL Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.6-Testing_for_NoSQL_Injection)
6. [NoSQL Injection in MongoDB — Zanon.io](https://zanon.io/posts/nosql-injection-in-mongodb/)
7. [NoSQL Injections: Classic & Blind — DailySecurity](https://www.dailysecurity.fr/nosql-injections-classique-blind/)
8. [MongoDB Injection Username/Password Enumeration](https://github.com/an0nlk/Nosql-MongoDB-injection-username-password-enumeration/tree/master)
9. [NoSQL Injection Wordlists](https://github.com/cr0hn/nosqlinjection_wordlists/tree/master)
10. [NoSQLi Lab](https://github.com/digininja/nosqlilab)
11. [Fault Injection Dataset](https://github.com/dessertlab/Fault-Injection-Dataset)
12. [Synthetic Dataset for SQL Injection](https://github.com/lsiddiqsunny/Synthetic-dataset-for-SQL-Injection)
13. [Injection Attacks in NoSQL Backends](https://github.com/riyazwalikar/injection-attacks-nosql-talk)
14. [NoSQL Dataset Analytics (400 records)](https://github.com/capnmav77/No-SQL_Gen/blob/master/DatasetAnalytics.ipynb)

---

## License

This project is developed as part of a thesis research. Please contact the author for usage permissions.

