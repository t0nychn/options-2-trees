# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 11:54:56 2021

@author: ztche
"""
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

# custom packages (see repo)
import tree_constructor as tc
import tree_plotter as tp

# headings
month = datetime.now().month
title = "options-2-trees"
if 1 <= month <= 5:
    st.title(title + " 🌳🌳")
elif 5 < month <= 8:
    st.title(title + " 🌴🌴")
elif 8 < month <= 11:
    st.title(title + " 🌲🌲")
else:
    st.title(title + " 🎄🎄")
st.write("by [Tony](https://www.linkedin.com/in/tony-c-8b592b162/)")
st.sidebar.title("Parameters")

# user inputs on sidebar
S = st.sidebar.slider('Stock Price (S)', value=500, 
                      min_value=250, max_value=750)

X = st.sidebar.slider('Exercise Price (X)', value=500, 
                      min_value=250, max_value=750)

T = st.sidebar.slider('Time Periods (T)', value=5, 
                      min_value=1, max_value=15)

r = st.sidebar.slider('Inter-period Interest Rate (r)', value=0.0, 
                      min_value=0.0, max_value=0.05, step=0.01)

u = st.sidebar.slider('Stock Growth Factor (u)', value=1.10, 
                      min_value=1.01, max_value=1.25, step=0.01)
d = 1/u
st.sidebar.write("Stock Decay Factor (d) ", round(d, 4))

# decimal point of values (non-adjustable)
dp = 6

# initialize calculations
trees = tc.Calculate(S, X, T, r, u, dp)

# display p value
p = trees.p_value()
st.sidebar.write("Stock Growth Probability (p) ", round(p, 4))

# back to main body
st.header("*See how the Cox-Ross-Rubinstein (CRR) options pricing model react to changing parameters*")
st.markdown("This visualisation aims to explore the dynamics of abstract financial theory. "
            "Can you adjust the display to see how how the value of a call option today is positively correlated to the interest rate, "
            "or how the diffusion of the CRR tree is inherently lognormal?"
            )

st.subheader('Key:')
st.markdown("✅ Stock tree: black")
call = st.checkbox('Call tree: blue')
put = st.checkbox('Put tree: red')

# plot stock tree
tp.plot_stock_lattice(trees.stock_prices())

# plot exercise price reference
plt.plot(range(T+1), [X for t in range(T+1)], 
         linestyle="dashed", label="Exercise Price (X)")
plt.annotate(X, (0, X), textcoords="offset points",
             xytext=(0,-15), ha='center')
plt.legend()

# plot options trees
if call:
    tp.plot_option_lattice(trees.call_values())
if put:
    tp.plot_option_lattice(trees.put_values(), 'ro-')
st.pyplot(plt)

# display calculated values
st.write("Call value (C): ", round(trees.call_values()[-1][0], 4), "Put value (P): ", round(trees.put_values()[-1][0], 4))

# text section
st.header("1. What's Going On?")
st.markdown("Options are financial instruments that derive value from an underlying asset. "
            "Most often, the underlying asset is a stock, which is what we're modelling here. "
            "Options must be exercised before they expire, but can only be exercised past a certain the exercise price. "
            "There are different kinds of options. Here, we're modelling vanilla European options, which can only be exercised at expiry. "
            )

st.markdown("You can buy options to gain from either a move up or a move down in the stock price. "
            "Call options give the holder the right to either buy the stock at the exercise price, or let the option contract expire worthless. "
            "Hence, the value of call options increase with the price of the underlying stock. Call options have payoff: "
            )

st.latex("max(S-X, 0)")

st.markdown("Put options give the holder the right to either sell the stock at the exercise price, or let the option contract expire worthless. "
            "Hence, the value of put options decrease when the price of the underlying stock increases. Put options have payoff: ")

st.latex("max(X-S, 0)")

st.markdown("To price options, the CRR model constructs a binomial tree of stock prices for n time periods up to time T, "
            "then works backwards across each time period from t = T to find the option price at t = 0. "
            "For simplicity, we've assumed that n = T (see the formulae used for this visualisation below). "
            "The stock tree (see below) is constructed by multipling each price node by growth factor u, and corresponding decay factor d to get the binomial states at t+1. "
            "The 'reverse' options pricing process involves calculating the option payoffs for each node at t = T, then applying a risk neutral probability measure p for each time period. "
            "Hence, the CRR process effectively constructs binomial trees for both the underlying stock and the option."
            )

st.image("https://github.com/t0nychn/options-2-trees/blob/main/binomial-tree-2-period.jpg?raw=true")

st.subheader("1.1 Main takeaways: ")
st.markdown("1) The nodes on the black tree tell us the future prices of a stock, and the nodes on the blue and red trees tell us the values of the corresponding options")
st.markdown("2) The CRR model gauges what the value of an option should be at t = 0 (today) by working backwards through the underlying stock tree using probability measure p")

st.header("2. Assumptions & Formulae")
st.subheader("2.1 Assumptions")
st.markdown("The [original CRR model](https://github.com/t0nychn/options-2-trees/blob/main/option_pricing_a_simplified_approach.pdf) was simplified for this presentation by: ")
st.markdown("a) Assuming T = n, which eliminates ΔT (T/n) from the original formulae")
st.markdown("b) Assuming r as the exponential inter-period rate, which eliminates r̂ (r/n) from the original formulae")
st.markdown("c) Assuming the underlying stock as non-cashflow generating, which eliminates 𝛿 (dividends) from the original formulae")
st.markdown("d) Assuming zero drift apart from the inherent lognormal diffusion process, which eliminates μ from the original formulae")
st.markdown("e) Allowing the user to directly adjust u, rather than calculating it from underlying volatility")

st.subheader("2.2 Formulae Used")
st.latex(r"d = \frac{1}{u}")
st.latex(r"S_{t+1} = S_t \cdot u")
st.latex(r"S_{t+1} = S_t \cdot d")
st.latex("C_T = max(S_T-X, 0)")
st.latex("P_T = max(X-S_T, 0)")
st.latex(r"p = \frac{e^r - d}{u - d}")
st.latex(r"C_t = e^{-r} (p \cdot Cu_{t+1} + (1 - p) \cdot Cd_{t+1})")
st.latex(r"P_t = e^{-r} (p \cdot Pu_{t+1} + (1 - p) \cdot Pd_{t+1})")
st.write("\n")

st.header("3. Misc")
st.markdown("Thanks for stopping by! For any comments or contributions please get in touch via [GitHub](https://github.com/t0nychn/options-2-trees)")
st.subheader("3.1 Resources")
st.markdown("[options-2-trees source code](https://github.com/t0nychn/options-2-trees/blob/main/final.py)")
st.markdown("[Investopedia: Options Definition](https://www.investopedia.com/terms/o/option.asp)")
st.markdown("[Nerdwallet: Options 101](https://www.nerdwallet.com/article/investing/options-trading-101)")
st.markdown("[Investopedia: Binomial Option Pricing Model](https://www.investopedia.com/terms/b/binomialoptionpricing.asp)")
st.markdown("[Cox, Ross & Rubinstein (1979). 'Option Pricing: a simplified approach'. Journal of Financial Economics 7 (1979) 229-263.](https://github.com/t0nychn/options-2-trees/blob/main/option_pricing_a_simplified_approach.pdf)")

st.subheader("3.2 Disclaimer")
st.write("All information on options-2-trees is provided for educational purposes only and does not constitute "
         "financial advice."
        )
