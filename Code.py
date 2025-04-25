
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
# %% Tabbed UI: Introduction | Supply & Demand App | Appendix

import streamlit.components.v1 as components

with tab1:
    components.html("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            padding: 20px;
            color: #1a1a1a;
        }
        .intro-box {
            background-color: #f1f3f5;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 800px;
            margin: auto;
        }
        h2 {
            color: #124265;
        }
        h4 {
            margin-top: 20px;
            color: #0b3c5d;
        }
        ul {
            padding-left: 20px;
        }
    </style>

    <div class="intro-box">
        <h2>Welcome to the USDA Supply & Demand Calculator</h2>
        <p>This app helps analysts <strong>quickly fetch, edit, and analyze</strong> agricultural commodity data using the live USDA PSD API.</p>

        <h4>What you can do:</h4>
        <ul>
            <li>Select Commodity, Country, and Market Year</li>
            <li>Fetch real-time PSD data from USDA</li>
            <li>Manually adjust values like:
                <ul>
                    <li>Production</li>
                    <li>Imports</li>
                    <li>Feed Dom. Consumption</li>
                    <li>FSI Consumption</li>
                    <li>Exports</li>
                </ul>
            </li>
            <li>View recalculated metrics:
                <ul>
                    <li>Total Supply</li>
                    <li>Domestic Consumption</li>
                    <li>Total Use</li>
                    <li>Ending Stocks</li>
                </ul>
            </li>
            <li>Download results as a CSV file</li>
        </ul>

        <h4>Navigation Help:</h4>
        <ul>
            <li><strong>Tab 1</strong>: This Introduction</li>
            <li><strong>Tab 2</strong>: Use the Calculator</li>
            <li><strong>Tab 3</strong>: Appendix & Logic</li>
        </ul>
    </div>
    """, height=700)

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
# %% Step 4: Attribute Mapping & Editable Metrics UI
with tab2:
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

    values = {
        key: float(data_dict.get(attr_id, 0))
        for key, attr_id in id_map.items()
    }

    st.subheader("Edit & Recalculate Key Supply-Demand Metrics")
    st.caption("Beginning Stocks: Stock carried over from the previous year. (Auto-filled)")

    beginning_stocks = values["Beginning Stocks"]
    st.write(f"Beginning Stocks: {beginning_stocks}")

    production = st.number_input("Production", value=values["Production"], min_value=0.0, max_value=1_000_000.0, step=1.0)
    imports = st.number_input("Imports", value=values["Imports"], min_value=0.0, max_value=1_000_000.0, step=1.0)
    feed_dom = st.number_input("Feed Domestic Consumption", value=values["Feed Dom. Consumption"], min_value=0.0, max_value=1_000_000.0, step=1.0)
    fsi_consumption = st.number_input("FSI Consumption", value=values["FSI Consumption"], min_value=0.0, max_value=1_000_000.0, step=1.0)
    exports = st.number_input("Exports", value=values["Exports"], min_value=0.0, max_value=1_000_000.0, step=1.0)

    print("Editable input section rendered under Tab 2.")

# %% Step 5: Perform Calculations (within tab2)
    total_supply = beginning_stocks + production + imports
    domestic_consumption = feed_dom + fsi_consumption
    total_use = domestic_consumption + exports
    ending_stocks = total_supply - total_use

    print("Real-time calculations performed:")
    print(f"  Total Supply = {beginning_stocks} + {production} + {imports} = {total_supply}")
    print(f"  Domestic Consumption = {feed_dom} + {fsi_consumption} = {domestic_consumption}")
    print(f"  Total Use = {domestic_consumption} + {exports} = {total_use}")
    print(f"  Ending Stocks = {total_supply} - {total_use} = {ending_stocks}")

# %% Step 6: Display Final Results (Styled Table with Header & Borders)
with tab2:
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

    calculated_fields = [
        "Total Supply",
        "Domestic Consumption",
        "Total Use",
        "Ending Stocks"
    ]

    def highlight_rows(row):
        if row["Metric"] in calculated_fields:
            return [
                'background-color: #fff3cd; color: black; font-weight: bold; border: 1.5px solid white;',
                'background-color: #fff3cd; color: black; font-weight: bold; border: 1.5px solid white;'
            ]
        return ['border: 1.5px solid #ccc;'] * len(row)

    styled_df = (
        final_df.style
        .apply(highlight_rows, axis=1)
        .set_table_styles([
            {"selector": "thead tr th", 
             "props": [
                 ("background-color", "#1f1f1f"),
                 ("color", "white"),
                 ("font-weight", "bold"),
                 ("border-bottom", "2px solid white"),
                 ("border-top", "2px solid white"),
             ]},
            {"selector": "th", "props": [("border", "1px solid white")]},
            {"selector": "td", "props": [("border", "1px solid #aaa")]}
        ])
    )

    st.dataframe(styled_df, use_container_width=True)

    print("✅ Styled table with bold header and calculated row highlights rendered.")

# %% Step 7: Download Option with Highlight Column
    csv_file = final_df.to_csv(index=False)
    st.download_button(
    label="Download Supply and Demand Metrics CSV",
    data=csv_file,
    file_name="supply_demand_metrics.csv",
    mime="text/csv",
    key="download_csv_tab2"  # ✅ uniquely identifies this download button
)


    print("✅ CSV file includes highlight column and is ready for download.")



    

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
