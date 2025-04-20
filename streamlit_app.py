import streamlit as st

st.set_page_config(page_title="Intrinsic Value Calculator", layout="centered")

st.title("💹 Intrinsic Value of Share Price Calculator")
company_name = st.text_input("Enter Company Name")

st.header("📊 Input Financial Data")

opc = st.number_input('Enter Operating Cash for Present Year', value=0.0)
opc1 = st.number_input('Enter Operating Cash for Last Year', value=0.0)
opc2 = st.number_input('Enter Operating Cash for Last to Last Year', value=0.0)

ope = st.number_input('Enter Capital Expenditure for Present Year', value=0.0)
ope1 = st.number_input('Enter Capital Expenditure for Last Year', value=0.0)
ope2 = st.number_input('Enter Capital Expenditure for Last to Last Year', value=0.0)

gr = st.number_input('Enter Growth Rate for Next 5 Years (%)', value=0.0)
gr1 = st.number_input('Enter Growth Rate for 6-10 Years (%)', value=0.0)
tr = st.number_input('Enter Terminal Growth Rate (%)', value=0.0)
dr = st.number_input('Enter Discount Rate for Terminal Growth (%)', value=0.0)

dv = st.number_input('Enter Current Year Debt', value=0.0)
cb = st.number_input('Enter Current Cash & Cash Balance', value=0.0)
os = st.number_input('Enter Outstanding Shares', value=1.0)

if st.button("📈 Calculate Intrinsic Value"):
    # Free cash flows
    aopc1 = opc - ope
    aopc2 = opc1 - ope1
    aopc3 = opc2 - ope2
    aopc = aopc1 + aopc2 + aopc3
    cashflow = aopc / 3

    # Growth rates
    grp = gr / 100
    grp1 = gr1 / 100
    trp = tr / 100
    drp = dr / 100

    # Future values
    oppcost = 1 + grp
    toppcost = oppcost ** 5
    FV5years = cashflow * toppcost

    oppcost1 = 1 + grp1
    toppcost1 = oppcost1 ** 5
    FV6to10years = FV5years * toppcost1

    # Terminal value
    trdr = drp - trp
    trr = 1 + trp
    trrdr = trr / trdr
    terminalvalue = FV6to10years * trrdr

    # FV for 10 years
    FV = [cashflow * (oppcost ** i) if i <= 5 else FV5years * (oppcost1 ** (i - 5)) for i in range(1, 11)]

    # Present values
    drprcosts = [(1 + drp) ** i for i in range(1, 11)]
    PV = [FV[i] / drprcosts[i] for i in range(10)]

    netpv = sum(PV)

    # Terminal value PV
    drcost = (1 + drp) ** 10
    pvtv = terminalvalue / drcost

    sumofpresentvalues = netpv + pvtv

    # Net debt
    netdebt = dv - cb

    # Total present value
    totalpresentvalue = sumofpresentvalues - netdebt

    # Share prices
    shareprice = totalpresentvalue / os
    uppershareprice = shareprice * 1.1
    lowershareprice = shareprice * 0.9
    marginofsafetyprice = lowershareprice * 0.7

    st.subheader(f"🧾 Results for {company_name or 'the company'}")
    st.success(f"Intrinsic Value of Share Price: ₹{shareprice:.2f}")
    st.info(f"Upper Bound: ₹{uppershareprice:.2f}")
    st.info(f"Lower Bound: ₹{lowershareprice:.2f}")
    st.warning(f"Margin of Safety Price: ₹{marginofsafetyprice:.2f}")
