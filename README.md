
# USDA Supply and Demand Calculator (Streamlit App)

---

## 📚 About This Project

This application enables analysts to quickly fetch, edit, recalculate, and export **Supply & Demand (S&D)** metrics for agricultural commodities such as Wheat, Corn, etc., using **live data from the USDA Foreign Agricultural Service (FAS) Production, Supply, and Distribution (PSD)** database.

The application is built with **Streamlit** to provide a clean, interactive web-based interface.

---

## 🎯 What This App Does

- Fetch real-time agricultural S&D data for selected Commodity, Country, and Market Year.
- Allow manual editing of key S&D fields:
  - Production
  - Imports
  - Feed Domestic Consumption
  - FSI Consumption
  - Exports
- Instantly recalculate:
  - Total Supply
  - Domestic Consumption
  - Total Use
  - Ending Stocks
- Download the final adjusted S&D balance as a `.csv` file.
- View internal logic, API information, and calculation formulas inside the app under the **Appendix** tab.

---

## 🛠 Setup Instructions (Step-by-Step)

### 1. Install Python

Ensure Python is installed on your system.  
Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

To verify if Python is installed, run:

```bash
python --version
```

---

### 2. Clone or Download This Project

Save the project folder locally.

### 3. Install Required Libraries

Navigate to the project folder:



Install all necessary libraries:

```bash
pip install -r requirements.txt
```

This installs:

| Library | Purpose |
|---------|---------|
| Streamlit | Building the web app |
| Pandas | Data manipulation |
| Requests | API calls to USDA |

---

### 4. Run the App

In the terminal:

```bash
streamlit run Code.py
```

This will launch the app in your default browser (usually at `http://localhost:8501/`).

---

## 🧮 Supply & Demand Formulas Used

| Calculation | Formula |
|-------------|---------|
| Total Supply | Beginning Stocks + Production + Imports |
| Domestic Consumption | Feed Domestic Consumption + FSI Consumption |
| Total Use | Domestic Consumption + Exports |
| Ending Stocks | Total Supply - Total Use |

---

## 🛡️ Error Handling and Validation

- API call status checked (`HTTP 200 OK`).
- Missing key metrics are flagged and stop calculations.
- Editable input fields enforce **numeric** values only.
- Downloadable `.csv` generated only after successful recalculation.

---

## 🔗 USDA API Endpoints Used

- `/commodities` → Fetch commodity list
- `/countries` → Fetch country list
- `/commodityAttributes` → Map attribute names to numeric IDs
- `/commodity/{commodity_code}/country/{country_code}/year/{market_year}` → Fetch main S&D balance data

All data is **publicly accessible** through the USDA Foreign Agricultural Service Open Data Portal:  
[https://apps.fas.usda.gov/opendatawebV2/](https://apps.fas.usda.gov/opendatawebV2/)

---

## 🧭 How to Use This Application

1. Select **Commodity**, **Country**, and **Year** from dropdowns.
2. The app fetches real data from the USDA database.
3. Analysts can **edit**:
   - Production
   - Imports
   - Feed Domestic Consumption
   - FSI Consumption
   - Exports
4. The app **automatically recalculates**:
   - Total Supply
   - Total Use
   - Ending Stocks
5. Click **Download CSV** to export your adjusted results.

---

## 📁 Project Structure

```
Kpler Assignment/
├── Code.py             # Main Streamlit app
├── requirements.txt    # Python libraries needed
├── README.md           # Full project documentation
```

---

## ✍️ Author

Developed by **Shrinidhi Sudhir**  
as part of the **Kpler Assignment** project.

---

## 🚀 Future Improvements (Optional Ideas)

- Add dynamic graphs to visualize supply vs demand over time.
- Allow comparing multiple countries side-by-side.
- Add a forecasting model based on historical data trends.

---

# Thank you for using the USDA S&D Calculator!

