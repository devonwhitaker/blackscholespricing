import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def b_scholes(S0, strike, t, r, sigma, type='call'):
    """
    S0: Current Price
    strike: strike price
    t: time to maturity in days
    r: risk-free rate
    sigma: volatility
    type: call or put
    """

    t = t / 365

    d1 = (np.log(S0 / strike) + (r + sigma**2 / 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - (sigma * np.sqrt(t))

    if type == 'call':
        price = S0 * norm.cdf(d1) - strike * np.exp(-r * t) * norm.cdf(d2)
    elif type == 'put':
        price = strike * np.exp(-r * t) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    else:
        raise ValueError("type must be either call or put")
    
    return price

st.set_page_config(layout="wide")

st.sidebar.header("Pricing Parameters:")

S0_slider = st.sidebar.number_input('Select Current Price:', min_value=0.00, value=100.00, step=0.01)
strike_slider = st.sidebar.number_input('Select Strike Price:', min_value=0.00, value=100.00, step=0.01)
t_slider = st.sidebar.number_input('Time to Maturity (Days):', min_value=0, max_value=730, value=30, step=1)
r_slider = st.sidebar.number_input('Risk-Free Rate:', min_value=0.00, max_value=0.20, value=0.06, step=0.01)
sigma_slider = st.sidebar.number_input('Volatility:', min_value=0.00, max_value=0.99, value=0.20, step=0.01)


call_price = b_scholes(S0_slider, strike_slider, t_slider, r_slider, sigma_slider)
put_price = b_scholes(S0_slider, strike_slider, t_slider, r_slider, sigma_slider, type='put')


st.title("Black-Scholes Pricing Model")

df = pd.DataFrame({"Current Asset Price": [S0_slider],
                  "Strike Price": [strike_slider],
                  "Volatility": [sigma_slider],
                  "Time to Maturity (Days)": [t_slider],
                  "Risk-Free Rate": [r_slider]})

st.markdown(
    """
    <style>
        .dataframe-container {
            width: 100%;
            overflow-x: auto;
        }
        .dataframe {
            width: 100%;
            min-width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)



st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <div style="border: 2px solid green; border-radius: 10px; padding: 10px; background-color: #28a745; color: white; margin-right: 10px;">
            <h3 style="text-align: center;">Call Option Price: ${call_price:.2f}</h3>
        </div>
        <div style="border: 2px solid red; border-radius: 10px; padding: 10px; background-color: #8f1317; color: white;">
            <h3 style="text-align: center;">Put Option Price: ${put_price:.2f}</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.subheader("Heatmap Parameters:")

min_spot = st.sidebar.number_input('Min Spot Price:', min_value=0.00, max_value=S0_slider, value=S0_slider-10.00, step=0.01)
max_spot = st.sidebar.number_input('Max Spot Price:', min_value=S0_slider, value=S0_slider+10.00, step=0.01)

min_vol = st.sidebar.number_input('Min Volatility:', min_value=0.00, max_value=sigma_slider, value=sigma_slider-0.02, step=0.01)
max_vol = st.sidebar.number_input('Max Volatility:', min_value=sigma_slider, value=sigma_slider+0.02, step=0.01)

spot_range = np.linspace(min_spot,max_spot, 10)
vol_range = np.linspace(min_vol, max_vol, 10)

call_data = []

for spot in spot_range:
    row = []
    for vol in vol_range:
        price = b_scholes(spot, strike_slider, t_slider, r_slider, vol, type='call')
        row.append(round(price,2))
    call_data.append(row)

call_df = pd.DataFrame(call_data, index=spot_range, columns=vol_range)


call_fig = px.imshow(
    call_df,
    text_auto=True,
    labels=dict(x="Spot Price", y="Volatility", color="Call Price"),
    x=call_df.index,
    y=call_df.columns,
    color_continuous_scale='rdylgn',
    aspect='auto'
)


put_data = []

for spot in spot_range:
    row = []
    for vol in vol_range:
        price = b_scholes(spot, strike_slider, t_slider, r_slider, vol, type='put')
        row.append(round(price,2))
    put_data.append(row)

put_df = pd.DataFrame(put_data, index=spot_range, columns=vol_range)


put_fig = px.imshow(
    put_df,
    text_auto=True,
    labels=dict(x="Spot Price", y="Volatility", color="Put Price"),
    x=put_df.index,
    y=put_df.columns,
    color_continuous_scale='rdylgn',
    aspect='auto'
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(call_fig, use_container_width=True)

with col2:
    st.plotly_chart(put_fig, use_container_width=True)

print(put_df.head())