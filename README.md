# WebScrappinffinal — Web Scraper (Notebook + Script)
[![Kaggle Badge](https://img.shields.io/badge/Kaggle-Vishesh%20Patel-blue?style=flat&logo=kaggle)](https://www.kaggle.com/visheshptel)

This project contains a Python web scraper designed to collect real property data directly from the [Connecticut Online Database (VGSI)](https://www.vgsi.com/connecticut-online-database/).  
It extracts genuine property records — including **ownership details, sales history, sale prices, and transaction dates** — for multiple Connecticut cities.  
The most interesting feature is the availability of **historical sales data**, making this dataset highly valuable for **price prediction models, trend analysis, and real-estate analytics.**


This repository contains a Jupyter notebook (`Webscrappinffinal_clean.ipynb`) and an auto-generated Python script (`scraper_from_notebook.py`) that implement a web-scraping workflow.

## 📌 What this project includes
- **Cleaned notebook** (no outputs) for easy GitHub viewing.
- **Python script** auto-converted from the notebook code cells.
- **Inferred `requirements.txt`** based on imports detected.
- **Repo hygiene**: `.gitignore`, `LICENSE`, and `data/` folder.

## ▶️ Quickstart
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python scraper_from_notebook.py
```
## 📊 Data Sources

This repository includes two curated Excel datasets capturing the **historical property sales records for the state of Connecticut**, with a particular focus on **Bridgeport** and **Fairfield City**.  
These datasets are highly valuable for **price prediction, real-estate analytics, and machine-learning modeling**, as they provide detailed transaction history across owners, prices, and structural property features (e.g., number of bathrooms, fireplaces, etc.).

### 1) `data/Merged_Property_Details.xlsx`
- **Shape:** 98,654 rows × 8 columns  
- **Purpose:** Final **merged dataset** created using a unique primary key to combine multiple data sources for **property price prediction**.  
- **Coverage:** Historical transactions for properties across Connecticut, primarily Bridgeport and Fairfield.  
- **Example columns:** `Owner`, `Sale Price`, `Certificate`, `Book & Page`, `Instrument`, `Sale Date`, `Address`, `Pincode`

### 2) `data/Transformed_Sales_Data.xlsx`
- **Sheets:** `Sheet1`  
- **Shape:** 19,506 rows × 39 columns  
- **Purpose:** Intermediate **transformed sales dataset** containing cleaned, structured transaction records prior to merging. It includes multi-owner sales history, property descriptions, and physical attributes such as **bathrooms, fireplaces, and land details**.  
- **Example columns:** `Unique_ID`, `Owner_1`, `Sale_Price_1`, `Sale_Date_1`, `Owner_2`, `Sale_Price_2`, `Sale_Date_2`, …, `Address`, `Pincode`, `Description`, `Land`

### 🔗 Download Options
- **Direct (GitHub):** Download the Excel files directly from the `data/` folder:
  - [`Merged_Property_Details.xlsx`](./data/Merged_Property_Details.xlsx)
  - [`Transformed_Sales_Data.xlsx`](./data/Transformed_Sales_Data.xlsx)
- **Kaggle Profile:** Additional datasets and CSV exports are shared on my Kaggle profile:  
  👉 [https://www.kaggle.com/visheshptel](https://www.kaggle.com/visheshptel)


## 🧠 Notebook
Open in Jupyter to run step-by-step:
- `Webscrappinffinal_clean.ipynb`

## 🔎 Detected Imports
(No external imports detected automatically.)

## 🧰 Requirements (inferred)
See `requirements.txt` — adjust as needed.

## 📁 Structure
```
.
├── Webscrappinffinal_clean.ipynb
├── scraper_from_notebook.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── data/
    └── .gitkeep
```

## ✅ Prep for GitHub
- Review `scraper_from_notebook.py` and make functions/CLI flags if desired.
- Confirm `requirements.txt` (add versions if needed).
- Keep credentials in `.env` and **never** commit secrets.
- Pin this repo on your GitHub profile.
