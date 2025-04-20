import streamlit as st

st.set_page_config(page_title="Intrinsic Value Calculator", layout="centered")

st.title("Intrinsic Value Calculator")
st.markdown("Estimate the intrinsic value of a company's shares using discounted cash flow (DCF) methodology.")

company_name = st.text_input("Enter Company Name")

with st.form("input_form"):
    st.subheader("Cash Flow Inputs")
    opc = st.number_input("Operating cash for present year", format="%.2f")
    opc1 = st.number_input("Operating cash for last year", format="%.2f")
    opc2 = st.number_input("Operating cash for year before last", format="%.2f")
    ope = st.number_input("Capital expenditure for present year", format="%.2f")
    ope1 = st.number_input("Capital expenditure for last year", format="%.2f")
    ope2 = st.number_input("Capital expenditure for year before last", format="%.2f")

    st.subheader("Growth & Discount Rates")
    gr = st.number_input("Growth rate (next 5 years) %", format="%.2f")
    gr1 = st.number_input("Growth rate (6–10 years) %", format="%.2f")
    tr = st.number_input("Terminal growth rate %", format="%.2f")
    dr = st.number_input("Discount rate %", format="%.2f")

    st.subheader("Financial Position")
    dv = st.number_input("Current debt", format="%.2f")
    cb = st.number_input("Cash & cash balance", format="%.2f")
    os = st.number_input("Outstanding shares", format="%.2f")

    submitted = st.form_submit_button("Calculate")

if submitted and company_name:
    # Step 1 Average Free Cash Flow
    aopc1 = opc - ope
    aopc2 = opc1 - ope1
    aopc3 = opc2 - ope2
    cashflow = (aopc1 + aopc2 + aopc3) / 3

    # Step 2 Future values
    oppcost = 1 + gr / 100
    toppcost = oppcost ** 5
    FV5years = cashflow * toppcost

    oppcost
