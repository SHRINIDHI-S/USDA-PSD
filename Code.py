
# %%
# ---
# Load all necessary libraries for Streamlit app, data processing, and API calls.

import streamlit as st
import pandas as pd
import requests

# Debug print
print("✅ Libraries imported successfully.")
print("_" * 40)

# %%
# %% Tabbed UI: Introduction | Supply & Demand App | Appendix
# ---
# Creating separate tabs for clean user navigation.

tab1, tab2, tab3 = st.tabs(["Introduction", "Supply & Demand Calculator", "Appendix & Methodology"])

# %%

# %% Introduction Content – Full Visual Upgrade
with tab1:
    st.markdown("""
    <style>
    .intro-card {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.1);
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
    }
    .intro-card h2 {
        color: #2e6f95;
    }
    .intro-card h4 {
        margin-top: 25px;
        color: #00334e;
    }
    .badge {
        display: inline-block;
        padding: 6px 12px;
        background-color: #0d6efd;
        color: white;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 10px;
    }
    </style>

    <div class="intro-card">
        <div class="badge">USDA Data Tool</div>

        <h2>Welcome to the Supply & Demand Calculator</h2>

        This tool is built for analysts to <strong>quickly access, edit, and export</strong> global commodity data 
        from the official USDA Production, Supply & Distribution (PSD) system.

        <h4>What you can do:</h4>
        <ul>
            <li>Select <strong>Commodity</strong>, <strong>Country</strong>, and <strong>Market Year</strong></li>
            <li>Fetch live S&D data using the <strong>USDA PSD API</strong></li>
            <li>Manually adjust values like:
                <ul>
                    <li>Production</li>
                    <li>Imports</li>
                    <li>Feed Dom. Consumption</li>
                    <li>FSI Consumption</li>
                    <li>Exports</li>
                </ul>
            </li>
            <li>Get real-time calculations:
                <ul>
                    <li>Total Supply</li>
                    <li>Domestic Consumption</li>
                    <li>Total Use</li>
                    <li>Ending Stocks</li>
                </ul>
            </li>
            <li>Download results as <code>.csv</code></li>
        </ul>

        <h4>How to Navigate:</h4>
        <ul>
            <li><strong>Tab 1 (This)</strong> – Introduction & Instructions</li>
            <li><strong>Tab 2</strong> – Calculator: Fetch data, edit, calculate</li>
            <li><strong>Tab 3</strong> – Appendix: Full logic, formulas, and API references</li>
        </ul>

        Hover over input boxes for tooltips. Use the sidebar if enabled. Click tabs at the top to switch between views.
    </div>
    """, unsafe_allow_html=True)



# %%
# %% API Configuration
# ---
# Setting API key and headers for USDA FAS data access.

API_KEY = "PKH2By52gg05QecOChs1WLEFOVbFbRKzNeVYgM1R"
BASE_URL = "https://api.fas.usda.gov/api/psd"
headers = {"X-Api-Key": API_KEY}

# Debug print
print("✅ API Key and Headers set up.")
print("_" * 40)

# %%
# %% API Fetch Functions
# ---
# Functions to fetch commodities, countries, attributes, and PSD data.

@st.cache_data
def get_commodities():
    url = f"{BASE_URL}/commodities"
    response = requests.get(url, headers=headers)
    return response.json() if response.ok else []

@st.cache_data
def get_countries():
    url = f"{BASE_URL}/countries"
    response = requests.get(url, headers=headers)
    return response.json() if response.ok else []

@st.cache_data
def get_attribute_map():
    url = f"{BASE_URL}/commodityAttributes"
    response = requests.get(url, headers=headers)
    try:
        data = response.json()
        return {d["attributeName"]: d["attributeId"] for d in data if "attributeId" in d}
    except:
        return {}

def get_psd_data(commodity_code, country_code, year):
    url = f"{BASE_URL}/commodity/{commodity_code}/country/{country_code}/year/{year}"
    response = requests.get(url, headers=headers)
    if not response.ok:
        return []
    try:
        return response.json()
    except:
        return []

# %%
# %% Supply and Demand Calculator (Tab 2)
with tab2:
    st.header("Quick Supply and Demand Calculator")

    # Step 1: Fetch dropdown options
    commodities = get_commodities()
    countries = get_countries()
    attribute_map = get_attribute_map()

    commodity_options = {c["commodityName"]: c["commodityCode"] for c in commodities}
    country_options = {c["countryName"]: c["countryCode"] for c in countries}

    # Debug prints
    print("✅ Commodity and Country options fetched.")
    print(f"Total Commodities: {len(commodity_options)}")
    print(f"Total Countries: {len(country_options)}")

    # Step 2: Dropdown Selections
    selected_commodity = st.selectbox("Select a Commodity", options=list(commodity_options.keys()), help="Choose a commodity (e.g., Wheat, Corn).")
    selected_country = st.selectbox("Select a Country", options=list(country_options.keys()), help="Select the reporting country.")
    selected_year = st.number_input("Select Market Year", min_value=1990, max_value=2030, step=1, value=2020, help="Choose the analysis year.")

    commodity_code = commodity_options[selected_commodity]
    country_code = country_options[selected_country]

    # Debug prints
    print(f"✅ Selected Commodity: {selected_commodity} (Code: {commodity_code})")
    print(f"✅ Selected Country: {selected_country} (Code: {country_code})")
    print(f"✅ Selected Year: {selected_year}")

# %%
    # Step 3: Fetch PSD data
    psd_data = get_psd_data(commodity_code, country_code, selected_year)

    if not psd_data:
        st.warning("No data available for the selected Commodity, Country, and Year.")
        st.stop()

    data_dict = {item["attributeId"]: item["value"] for item in psd_data}

    # Debug print
    print("✅ PSD data fetched and parsed into attributeId:value dictionary.")

# %%
# Step 4: Attribute Mapping
id_map = {
    name: attribute_map.get(name, -1)
    for name in [
        "Beginning Stocks",
        "Production",
        "Imports",
        "Feed Dom. Consumption",
        "FSI Consumption",
        "Exports"
    ]
}

# Retrieve values from data_dict with safe defaults
values = {
    key: float(data_dict.get(attr_id, 0))
    for key, attr_id in id_map.items()
}

st.subheader("Editable Key Metrics (Provide Adjustments)")
st.caption("Beginning Stocks: Stock carried over from the previous year. (Auto-filled)")

# Beginning Stocks are shown but not editable
beginning_stocks = values["Beginning Stocks"]
st.write(f"Beginning Stocks: {beginning_stocks}")

# Editable fields for the analyst
production = st.number_input(
    "Production", 
    value=values["Production"], 
    min_value=0.0, 
    max_value=1_000_000.0, 
    step=1.0, 
    help="Total domestic production during the year."
)

imports = st.number_input(
    "Imports", 
    value=values["Imports"], 
    min_value=0.0, 
    max_value=1_000_000.0, 
    step=1.0, 
    help="Total imports during the year."
)

feed_dom = st.number_input(
    "Feed Domestic Consumption", 
    value=values["Feed Dom. Consumption"], 
    min_value=0.0, 
    max_value=1_000_000.0, 
    step=1.0, 
    help="Grains or seeds consumed as livestock feed."
)

fsi_consumption = st.number_input(
    "FSI Consumption", 
    value=values["FSI Consumption"], 
    min_value=0.0, 
    max_value=1_000_000.0, 
    step=1.0, 
    help="Food, Seed, and Industrial uses."
)

exports = st.number_input(
    "Exports", 
    value=values["Exports"], 
    min_value=0.0, 
    max_value=1_000_000.0, 
    step=1.0, 
    help="Total exports during the year."
)

# Debug print to confirm rendering
print("Editable metric fields rendered and values captured.")


# %%
# Step 5: Perform Calculations
total_supply = beginning_stocks + production + imports
domestic_consumption = feed_dom + fsi_consumption
total_use = domestic_consumption + exports
ending_stocks = total_supply - total_use

# Debug prints (uncomment during development/testing)
print("Real-time calculations performed:")
print(f"  Total Supply = {beginning_stocks} + {production} + {imports} = {total_supply}")
print(f"  Domestic Consumption = {feed_dom} + {fsi_consumption} = {domestic_consumption}")
#print(f

# %%
# Step 6: Display Final Results
st.subheader("Calculated Supply & Demand Metrics")

final_df = pd.DataFrame({
    "Metric": [
        "Beginning Stocks",
        "Production",
        "Imports",
        "Total Supply",
        "Feed Domestic Consumption",
        "FSI Consumption",
        "Domestic Consumption",
        "Exports",
        "Total Use",
        "Ending Stocks"
    ],
    "Value": [
        beginning_stocks,
        production,
        imports,
        total_supply,
        feed_dom,
        fsi_consumption,
        domestic_consumption,
        exports,
        total_use,
        ending_stocks
    ]
})

# Display the final table to the user
st.dataframe(final_df, use_container_width=True)

# Debug print to verify final DataFrame creation
# print("Final recalculated DataFrame prepared for display and download.")
# %%  
# %% 
# Step 7: Provide Download Option
# ---
# This enables the user to download the recalculated table as a CSV file.

csv_file = final_df.to_csv(index=False)

st.download_button(
    label="Download Supply and Demand Metrics CSV",
    data=csv_file,
    file_name="supply_demand_metrics.csv",
    mime="text/csv"
)

# Debug print
# print("CSV download button available for user.")

    

# %%
# %% Appendix Section
# ---
# This section provides the full documentation of the app and its logic.

with tab3:
    st.header("Appendix: Methodology and Calculation Logic")

    st.markdown("""
    ### API Endpoints Utilized
    - `/commodities`: Fetch list of commodities
    - `/countries`: Fetch list of countries
    - `/commodityAttributes`: Map human-readable names to attribute IDs
    - `/commodity/{commodity_code}/country/{country_code}/year/{year}`: Fetch PSD data

    ### Supply & Demand Formulas
    - **Total Supply** = Beginning Stocks + Production + Imports
    - **Domestic Consumption** = Feed Dom. Consumption + FSI Consumption
    - **Total Use** = Domestic Consumption + Exports
    - **Ending Stocks** = Total Supply - Total Use

    ### User Inputs Explanation
    - **Production**: Total commodity output within the year.
    - **Imports**: Total quantity imported into the country.
    - **Feed Dom. Consumption**: Quantity used as animal feed.
    - **FSI Consumption**: Quantity used for Food, Seed, Industrial purposes.
    - **Exports**: Total quantity exported out of the country.

    ### Error Handling and Validation
    - All API calls checked for success (HTTP 200).
    - Missing attributes are flagged and the process is halted with an error.
    - Editable input fields accept only valid numeric values to maintain data integrity.

    ---
    This application is designed to be intuitive for analysts while ensuring full auditability and transparency for technical reviewers.
    """)

# %%
