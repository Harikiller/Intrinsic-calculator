import streamlit as st

st.set_page_config(page_title="Intrinsic Value Calculator", layout="centered")

st.title("💹 Intrinsic Value of Share Price Calculator")
company_name = st.text_input("Enter Company Name")

# Section 1: Cash Flow
with st.expander("💵 Cash Flow"):
    st.subheader("💵 Operating Cash Flow & Capital Expenditure")
    opc = st.number_input('Operating Cash - Present Year', value=0.0)
    opc1 = st.number_input('Operating Cash - Last Year', value=0.0)
    opc2 = st.number_input('Operating Cash - Year Before Last', value=0.0)

    ope = st.number_input('Capital Expenditure - Present Year', value=0.0)
    ope1 = st.number_input('Capital Expenditure - Last Year', value=0.0)
    ope2 = st.number_input('Capital Expenditure - Year Before Last', value=0.0)

# Section 2: Growth Assumptions
with st.expander("📈 Growth Assumptions"):
    st.subheader("📈 Growth & Discount Rates")
    gr = st.number_input('Growth Rate for Next 5 Years (%)', value=0.0)
    gr1 = st.number_input('Growth Rate for Years 6-10 (%)', value=0.0)
    tr = st.number_input('Terminal Growth Rate (%)', value=0.0)
    dr = st.number_input('Discount Rate (%)', value=0.0)

# Section 3: Financial Position
with st.expander("🏦 Financial Position"):
    st.subheader("💰 Cash, Debt & Shares Info")
    dv = st.number_input('Total Debt (Current Year)', value=0.0)
    cb = st.number_input('Cash & Cash Equivalents', value=0.0)
    os = st.number_input('Outstanding Shares', value=1.0, help="Must be greater than 0")

# Calculate Button
if st.button("📈 Calculate Intrinsic Value"):
    # Input validations
    if os <= 0:
        st.error("Outstanding Shares must be greater than 0.")
        st.stop()
    if dr <= tr:
        st.error("Discount Rate must be greater than Terminal Growth Rate.")
        st.stop()

    # Free cash flows
    free_cash_flows = [(opc - ope), (opc1 - ope1), (opc2 - ope2)]
    cashflow = sum(free_cash_flows) / len(free_cash_flows)

    # Growth rates
    grp = gr / 100
    grp1 = gr1 / 100
    trp = tr / 100
    drp = dr / 100

    # Future values
    FV5years = cashflow * ((1 + grp) ** 5)
    FV6to10years = FV5years * ((1 + grp1) ** 5)

    # Terminal value
    terminalvalue = FV6to10years * ((1 + trp) / (drp - trp))

    # Projected cash flows
    FV = [cashflow * ((1 + grp) ** i) if i < 5 else FV5years * ((1 + grp1) ** (i - 5)) for i in range(10)]

    # Discounted to present value
    PV = [FV[i] / ((1 + drp) ** (i + 1)) for i in range(10)]
    netpv = sum(PV)
    pvtv = terminalvalue / ((1 + drp) ** 10)
    sumofpresentvalues = netpv + pvtv

    # Net debt
    netdebt = dv - cb
    totalpresentvalue = sumofpresentvalues - netdebt

    # Share price
    shareprice = totalpresentvalue / os
    uppershareprice = shareprice * 1.1
    lowershareprice = shareprice * 0.9
    marginofsafetyprice = lowershareprice * 0.7

    st.subheader(f"🧾 Results for {company_name or 'the company'}")
    st.success(f"Intrinsic Value of Share Price: ₹{shareprice:.2f}")
    st.info(f"Upper Bound: ₹{uppershareprice:.2f}")
    st.info(f"Lower Bound: ₹{lowershareprice:.2f}")
    st.warning(f"Margin of Safety Price: ₹{marginofsafetyprice:.2f}")
