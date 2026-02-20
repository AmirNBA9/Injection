# NoSQL Injection Detection Using Machine Learning

> پایان‌نامه کارشناسی ارشد: **بهبود تشخیص حملات تزریق پایگاه‌داده غیررابطه‌ای مبتنی بر یادگیری ماشین**  
> دانشگاه صنعتی مالک‌اشتر · مجتمع دانشگاهی برق و کامپیوتر · رشته مهندسی کامپیوتر گرایش رایانش امن

---

## Table of Contents

- [Thesis Overview](#thesis-overview)
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

## Thesis Overview

| Item | Details |
|------|---------|
| **Title (EN)** | Improving NoSQL Injection Detection Using Machine Learning |
| **Title (FA)** | بهبود تشخیص حملات تزریق پایگاه‌داده غیررابطه‌ای مبتنی بر یادگیری ماشین |
| **University** | دانشگاه صنعتی مالک‌اشتر (Malek-Ashtar University of Technology) |
| **Degree** | کارشناسی ارشد مهندسی کامپیوتر – گرایش رایانش امن |
| **Document** | `Thesis_V3.4.docx` (latest); `Thesis_V3.3.docx`, `Thesis_V3.2.docx` (previous versions) |

**Thesis structure (۶ فصل):**

1. **فصل اول – مقدمه**: بیان مسئله، تشریح موضوع، ضرورت تحقیق، اهداف، نوآوری.
2. **فصل دوم – مبانی نظری و پیشینه پژوهش**: پایگاه‌داده‌های غیررابطه‌ای، چالش‌های امنیتی، یادگیری ماشین، مدل‌های زبان بزرگ، پیشینه پژوهش.
3. **فصل سوم – روش پیشنهادی**: خط‌لوله پژوهش، سناریوهای داده (Real-400 و Syn-2000)، تولید داده مصنوعی با GPT-5.2، مدل‌های یادگیری ماشین و تجمیعی، پیاده‌سازی.
4. **فصل چهارم – تجزیه‌وتحلیل داده‌ها (یافته‌ها)**: معیارهای ارزیابی، بررسی دیتاست‌ها، عملکرد در سه سناریو، مقایسه نهایی.
5. **فصل پنجم – بحث، نتیجه‌گیری و پیشنهادات**: مرور نتایج، تحلیل در چارچوب پیشینه، نقاط قوت و محدودیت‌ها، کاربردهای عملی، پیشنهادها برای تحقیقات آینده.
6. **فهرست مراجع**

---

## Overview

NoSQL databases (especially **MongoDB**) are increasingly targeted by injection attacks that exploit query operators and JavaScript execution. This project implements a full ML pipeline to detect such attacks by:

1. **Collecting** and labeling NoSQL query patterns (benign & malicious)
2. **Extracting** 18 numeric features from each query
3. **Augmenting** data using a Large Language Model (GPT-5.2) to generate synthetic samples (Syn-2000) when real labeled data is limited (Real-400)
4. **Training** multiple ML classifiers with stratified cross-validation
5. **Evaluating** models using accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix (with emphasis on FP/FN for security)

**Key finding from the thesis:** The “best” model depends on the data scenario: **Random Forest** on Real-400, **KNN** on Syn-2000 (Seed=50% Real), and **LightGBM** on Syn-2000 (Seed=All Real-400). Ensemble methods (Soft Voting, Stacking) can minimize FN but may increase FP; the choice should align with the operational security policy (FN-centric vs FP-centric).

---

## NoSQL Injection Attack Patterns

Examples of MongoDB injection payloads that this project aims to detect:

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

| Property | Value |
|----------|--------|
| **Base dataset (Real-400)** | 400 labeled NoSQL queries (MongoDB-oriented) |
| **Synthetic data (Syn-2000)** | 2,000 records generated with GPT-5.2 (two seeds: 50% Real, 100% Real) |
| **Train/Test** | 80% / 20% stratified split |
| **Label 0** | Benign (~22%) |
| **Label 1** | Malicious (~78%) |
| **Missing values** | None after preprocessing |

**Three experimental scenarios (as in thesis):**

- **Scenario 1 – Real-400:** Train/test on the original 400 real samples only.
- **Scenario 2 – Syn-2000 (Seed=50% Real):** Synthetic data generated using half of the real data as seed; train/test on synthetic (or defined mix).
- **Scenario 3 – Syn-2000 (Seed=All Real-400):** Synthetic data generated using all 400 real samples as seed; then split Syn-2000 into train/test.

---

## Features

18 numeric features are extracted from each NoSQL query (as in the thesis):

| # | Feature | Description |
|---|---------|-------------|
| 1 | `num_keys` | Number of keys in the query |
| 2 | `num_operators` | Count of MongoDB operators (`$ne`, `$gt`, …) |
| 3 | `length_user_value` | Length of the user-supplied value |
| 4 | `length_password_value` | Length of the password value |
| 5 | `length_username_value` | Length of the username value |
| 6 | `contains_email_pattern` | Whether an email pattern is present |
| 7 | `contains_ip_pattern` | Whether an IP address pattern is present |
| 8 | `nested_keys_exist` | Presence of nested keys |
| 9 | `num_nested_keys` | Count of nested keys |
| 10 | `contains_numeric_values` | Whether numeric values are present |
| 11 | `contains_boolean_values` | Whether boolean values are present |
| 12 | `contains_empty_strings` | Whether empty strings are present |
| 13 | `contains_fixed_values` | Whether fixed/hardcoded values are present |
| 14 | `unique_key_count` | Number of unique keys |
| 15 | `data_type_diversity` | Diversity of data types in the query |
| 16 | `total_record_length` | Total character length of the record |
| 17 | `special_characters_exist` | Whether special characters are present |
| 18 | `nested_depth` | Maximum nesting depth of the query |

---

## Project Structure

```
Injection/
├── README.md                          # Project documentation (this file)
├── NoSQLDetectionv2.ipynb             # Main ML training & evaluation notebook
├── splitData.ipynb                    # Train/test split utility
├── AnalyticsOfDataset.py              # Dataset generation & analysis
├── Set_DataToMongo.py                 # Import data into MongoDB
├── Del_RedundantRecord.py             # Remove duplicate records from MongoDB
├── finaldataset.json                 # Raw labeled dataset (JSON)
├── Thesis_V3.2.docx                  # Thesis document (v3.2)
├── Thesis_V3.3.docx                  # Thesis document (v3.3)
├── Thesis_V3.4.docx                  # Thesis document (v3.4 – current)
├── chapter1_refinement/              # Scripts used for Ch.1 transfer & refinement
│   ├── README.md                     # Description of scripts
│   ├── move_chapter1_working.py      # Content transfer (Ch.1 → Ch.2/3)
│   ├── refine_* / fix_* / verify_*   # Refinement and verification scripts
│   └── chapter1_text.txt             # Extracted Ch.1 text for analysis
└── Final/                             # Processed CSV datasets
    ├── data400.csv                    # Original 400-record dataset
    ├── train.csv                     # Full training set
    ├── train80.csv                   # 80% training split
    ├── test.csv                      # Full test set
    ├── test20.csv                    # 20% test split
    ├── synthetic_data_2000_*.csv      # Synthetic datasets (from 400 base)
    └── synthetic_from_train_*.csv    # Synthetic datasets (from train split)
```

---

## Installation

### Prerequisites

- Python 3.8+
- MongoDB (optional; for `Set_DataToMongo.py`, typically `localhost:27017`)

### Install Dependencies

```bash
pip install pandas numpy scikit-learn xgboost lightgbm imbalanced-learn matplotlib seaborn plotly pymongo
```

---

## Usage

### 1. Generate & Analyze Dataset

```bash
python AnalyticsOfDataset.py
```

Collects NoSQL query patterns, labels them as benign/malicious, removes near-duplicates (e.g. Jaccard similarity), and exports `finaldataset.json`.

### 2. Import Data into MongoDB (Optional)

```bash
python Set_DataToMongo.py
```

Reads `finaldataset.json` and inserts into MongoDB (`dataset.imp`). Ensure MongoDB is running.

### 3. Remove Duplicate Records (Optional)

```bash
python Del_RedundantRecord.py
```

Removes duplicate documents from MongoDB, keeping the most recent by `createdAt`.

### 4. Split Dataset

Use `splitData.ipynb` to perform an 80/20 stratified split while preserving label distribution.

### 5. Train & Evaluate Models

Use `NoSQLDetectionv2.ipynb` for:

- Loading and preprocessing data
- Feature extraction and (optional) correlation-based feature selection
- Class balancing (e.g. SMOTE) and scaling (e.g. StandardScaler)
- Training the classifiers listed below
- Stratified K-Fold cross-validation (e.g. 10-fold)
- Evaluation and visualizations (confusion matrices, ROC curves)
- Optional: synthetic data generation and scenario-based evaluation (Real-400, Syn-2000)

---

## Machine Learning Models & Results

**Models implemented (as in thesis):**

| Model | Description |
|-------|-------------|
| Logistic Regression | Base linear classifier |
| Decision Tree | Single tree, interpretable |
| K-Nearest Neighbors (KNN) | Instance-based, distance metric (e.g. Manhattan) |
| Support Vector Machine (SVM) | RBF kernel, probability estimates |
| Random Forest | Bagging of decision trees |
| Extra Trees | More randomized splits than Random Forest |
| Gradient Boosting | Sequential tree boosting |
| AdaBoost | Adaptive boosting |
| XGBoost | Gradient boosting (optimized) |
| LightGBM | Gradient boosting (efficient for larger/feature-rich data) |
| **Soft Voting Ensemble** | Weighted average of probabilities (e.g. KNN, RF, XGBoost, LightGBM, SVM) |
| **Stacking Ensemble** | Base learners + meta-learner (e.g. RF as final estimator) |

**Best model by scenario (from thesis results):**

| Scenario | Best overall (Accuracy / F1 macro) | Note |
|----------|-------------------------------------|------|
| Real-400 | **Random Forest** | Stable on small real data |
| Syn-2000 (Seed=50% Real) | **KNN** | Good local decision boundaries with denser synthetic data |
| Syn-2000 (Seed=All Real-400) | **LightGBM** | Best balance of accuracy and FP/FN on full-seed synthetic data |

- **FN vs FP:** Stacking can minimize FN (missed attacks) but may increase FP (false alarms); choice depends on security policy (FN-centric vs FP-centric).
- **Techniques:** SMOTE (optional), StandardScaler, StratifiedKFold, correlation-based feature selection (optional).

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
│  Evaluation &    │<───│  Model Training  │<───│  Preprocessing   │
│  Comparison      │    │  (12 classifiers │    │  (+ optional     │
│  (3 scenarios)   │    │   + 2 ensembles) │    │   SMOTE/Scaling) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                       │
                        ┌──────────────────┐    ┌────────▼────────┐
                        │  Synthetic Data  │<───│  GPT-5.2 (LLM)   │
                        │  Syn-2000        │    │  (optional)      │
                        └──────────────────┘    └─────────────────┘
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
