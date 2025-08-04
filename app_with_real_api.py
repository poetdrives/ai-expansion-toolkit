
import streamlit as st
import random
import requests

# ----- Page Config ----- #
st.set_page_config(page_title="AI Expansion Toolkit", layout="centered")

# ----- Helper Functions ----- #
def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[0]
        return {
            "official_name": data["name"]["official"],
            "capital": data["capital"][0],
            "region": data["region"],
            "languages": list(data["languages"].values()),
            "population": data["population"]
        }
    else:
        return {"error": f"Could not retrieve data for {country_name}"}

def get_gdp_per_capita(country_code):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.PCAP.CD?format=json&per_page=1&date=2022"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1 and data[1] and data[1][0]["value"]:
            return round(data[1][0]["value"], 2)
    return None

country_code_map = {
    "Germany": "DE",
    "India": "IN",
    "Japan": "JP",
    "Brazil": "BR",
    "Canada": "CA"
}

# ----- Header ----- #
st.title("AI Expansion Toolkit for Global Automotive Markets")
st.markdown("Helping automotive companies explore international expansion with AI-powered insights.")

# ----- Input Panel ----- #
st.subheader("Enter Expansion Parameters")
vehicle_type = st.text_input("Vehicle Type (e.g., electric SUV, compact sedan)")
target_country = st.selectbox("Target Country", list(country_code_map.keys()))
business_goal = st.selectbox("Expansion Goal", ["Launch Sales", "Establish Service Network", "Build Supply Chain", "Open Manufacturing Plant"])

# ----- Generate Report Button ----- #
if st.button("Generate Expansion Report"):
    with st.spinner("Analyzing international market data..."):
        st.subheader("🌐 Expansion Summary")

        # ----- Country Info ----- #
        country_info = get_country_info(target_country)
        if "error" not in country_info:
            st.write("**📊 Country Overview:**")
            st.write(f"- Official Name: {country_info['official_name']}")
            st.write(f"- Capital: {country_info['capital']}")
            st.write(f"- Region: {country_info['region']}")
            st.write(f"- Languages: {', '.join(country_info['languages'])}")
            st.write(f"- Population: {country_info['population']:,}")
        else:
            st.warning(country_info["error"])

        # ----- GDP Info ----- #
        wb_code = country_code_map.get(target_country)
        if wb_code:
            gdp = get_gdp_per_capita(wb_code)
            if gdp:
                st.write(f"**💰 GDP per Capita (2022):** ${gdp:,}")
            else:
                st.warning("Could not retrieve GDP data.")

        # ----- Mocked Market Fit Score ----- #
        fit_score = random.randint(60, 95)
        st.metric(label="Market Fit Score", value=f"{fit_score}/100")

        # ----- Mocked Regulations Summary ----- #
        st.write("**Regulatory Overview:**")
        st.success(f"{target_country} requires localized emission testing and homologation for all {vehicle_type} imports. Consider WLTP or BS6 standards depending on the region.")

        # ----- Mocked Cultural Insights ----- #
        st.write("**Cultural & Localization Tips:**")
        if target_country == "Japan":
            st.info("Consumers value compact design, advanced tech, and efficiency. Localization should include metric units, clean UI, and Japanese language support.")
        elif target_country == "Germany":
            st.info("Engineering quality and performance are critical. Emphasize range, build quality, and after-sales service.")
        elif target_country == "India":
            st.info("Focus on affordability, road durability, and low-maintenance EVs. Hindi-language materials and pricing in INR recommended.")
        else:
            st.info(f"Customize product and marketing for local preferences in {target_country} using region-specific language, pricing, and feature sets.")

        # ----- Mocked Strategy Tip ----- #
        st.write("**Strategic Recommendation:**")
        st.warning("Partner with local distributors or EV infrastructure companies for smoother entry and faster growth.")

# ----- Footer ----- #
st.markdown("---")
st.caption("Demo version – now with real-world API data.")
