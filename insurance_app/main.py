# main.py

import streamlit as st
from utils import *
from datetime import datetime
import uuid

st.set_page_config(layout="wide")
st.title("🏥 Insurance Claims Management & Risk Analysis")

# Load data
policyholders = load_data("data/policyholders.json")
claims = load_data("data/claims.json")


menu = st.sidebar.radio("Menu", ["Register Policyholder", "Add Claim", "Risk Analysis", "Reports"])

# 1. Register Policyholder
if menu == "Register Policyholder":
    st.subheader("Register New Policyholder")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18)
    policy_type = st.selectbox("Policy Type", ["Health", "Vehicle", "Life"])
    sum_insured = st.number_input("Sum Insured")
    if st.button("Register"):
        if name:
            new_ph = {
                "id": str(uuid.uuid4()),
                "name": name,
                "age": age,
                "policy_type": policy_type,
                "sum_insured": sum_insured
            }
            policyholders.append(new_ph)
            save_data("data/policyholders.json", policyholders)
            st.success("Policyholder registered successfully.")
        else:
            st.error("Name cannot be empty.")

# 2. Add Claim
elif menu == "Add Claim":
    st.subheader("Add New Claim")
    name_to_id = {p["name"]: p["id"] for p in policyholders}
    selected_name = st.selectbox("Select Policyholder", list(name_to_id.keys()))
    amount = st.number_input("Claim Amount")
    reason = st.text_input("Reason")
    status = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
    date = st.date_input("Date of Claim", datetime.today())

    if st.button("Submit Claim"):
        new_claim = {
            "claim_id": str(uuid.uuid4()),
            "policyholder_id": name_to_id[selected_name],
            "amount": amount,
            "reason": reason,
            "status": status,
            "date": str(date)
        }
        claims.append(new_claim)
        save_data("data/claims.json", claims)
        st.success("Claim added successfully.")

# 3. Risk Analysis
elif menu == "Risk Analysis":
    st.subheader("High-Risk Policyholders")
    high_risk = []
    for p in policyholders:
        p_claims = [c for c in claims if c["policyholder_id"] == p["id"]]
        if is_high_risk(p_claims, p["sum_insured"]):
            high_risk.append(p["name"])
    st.write(high_risk)

    st.subheader("Claims by Policy Type")
    st.write(aggregate_by_policy_type(policyholders))

# 4. Reports
elif menu == "Reports":
    st.subheader("📅 Total Claims per Month")
    st.bar_chart(total_claims_per_month(claims))

    st.subheader("📈 Average Claim Amount by Policy Type")
    st.write(average_claim_by_type(policyholders, claims))

    st.subheader("💰 Highest Claim Filed")
    st.write(highest_claim(claims))

    st.subheader("⏳ Policyholders with Pending Claims")
    st.write(get_pending_claims(claims))
