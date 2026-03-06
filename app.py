
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Load dataset
data = pd.read_csv("Concrete_Data.csv")

X = data.drop("Strength", axis=1)
y = data["Strength"]

model = RandomForestRegressor()
model.fit(X,y)

st.title("AI Concrete Mix Analyzer")

st.subheader("Enter Concrete Mix")

cement = st.number_input("Cement (kg/m3)",0.0,1000.0,320.0)
water = st.number_input("Water (kg/m3)",0.0,500.0,150.0)
flyash = st.number_input("Flyash (kg/m3)",0.0,200.0,30.0)
ggbs = st.number_input("GGBS (kg/m3)",0.0,200.0,0.0)
gravel = st.number_input("Gravel (kg/m3)",0.0,1500.0,1000.0)
sand = st.number_input("Sand (kg/m3)",0.0,1000.0,700.0)
sp = st.number_input("Superplasticizer",0.0,20.0,5.0)
wc = st.number_input("Water/Cement Ratio",0.0,1.0,0.5)
age = st.number_input("Age (days)",1,365,28)

wbinder = water/(cement+flyash+ggbs+0.0001)

if st.button("Analyze Mix"):

    input_data = pd.DataFrame([[cement,water,flyash,ggbs,gravel,sand,sp,wbinder,wc,age]],
                              columns=X.columns)

    prediction = model.predict(input_data)[0]

    st.success(f"Predicted Compressive Strength = {prediction:.2f} MPa")

    st.subheader("Optimized Mix Suggestions")

    mixes = []

    # material costs (₹ per kg)
    cement_cost = 7
    flyash_cost = 2
    ggbs_cost = 3
    sand_cost = 1
    gravel_cost = 1
    sp_cost = 50

    for i in range(400):

        c = cement + np.random.uniform(-40,40)
        w = water + np.random.uniform(-20,20)
        fa = flyash + np.random.uniform(-20,20)
        g = ggbs + np.random.uniform(-20,20)
        gr = gravel + np.random.uniform(-60,60)
        s = sand + np.random.uniform(-60,60)
        spx = sp + np.random.uniform(-2,2)

        wcx = w/c
        wb = w/(c+fa+g+0.0001)

        row = [c,w,fa,g,gr,s,spx,wb,wcx,age]

        pred = model.predict(pd.DataFrame([row],columns=X.columns))[0]

        cost = (c*cement_cost +
                fa*flyash_cost +
                g*ggbs_cost +
                s*sand_cost +
                gr*gravel_cost +
                spx*sp_cost)

        mixes.append([c,w,fa,g,gr,s,spx,pred,cost])

    df = pd.DataFrame(mixes,
        columns=["Cement","Water","Flyash","GGBS","Gravel","Sand","SP","Predicted Strength","Cost"])

    df["Strength Difference"] = abs(df["Predicted Strength"]-prediction)

    best = df.sort_values(["Strength Difference","Cost"]).head(5)

    st.subheader("Best Mix Designs (Strength + Cost Optimized)")

    st.dataframe(best)
