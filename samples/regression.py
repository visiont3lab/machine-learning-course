from sklearn.linear_model import LinearRegression,Lasso
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.preprocessing import PolynomialFeatures
from plotly import graph_objects as go
import pandas as pd
import numpy as np 
from datetime import datetime
import os

#--  pip install scikit-learn

url ="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"  
df = pd.read_csv(url) # lettura
df.head()
df["variazione_totale_positivi"].values
df["data"].values
fig = go.Figure()
fig.add_traces(go.Scatter(
    x=np.linspace(-5,5, num=len(df["variazione_totale_positivi"].values)), #df["data"].values,
    y=df["variazione_totale_positivi"].values
))
#fig.show()

# ---- Prepara i dati
X = np.linspace(-5,5, num=len(df["variazione_totale_positivi"].values)).reshape(-1,1) # 2D matrice (344,1) row (dati raccolti),col (gli input)
y = df["variazione_totale_positivi"].values # --(344,)
# Creazioen train test set
# ---------

# --- Preprocessing
# Polynomial Feature --> Crea nuovi input partendo da quelli che gia abbiamo
poly = PolynomialFeatures(degree=2) # 2,3,4 -->5 --700
X_new = poly.fit_transform(X)
print(X_new.shape)
#Xnew = np.array([X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8)]).T  # 4,344 --> 344,4
# PCA riduce il numero di input
# ------------------

# Regression 
#v = RandomForestRegressor()
v = LinearRegression()
#v = ExtraTreesRegressor()
v.fit(X_new,y)  # mettere dei valori allinterno delle variabli coef_,  intercept  -> w0,w1 ---- wn
Y_pred = v.predict(X_new) #np.array([8,8*8,8*8*8]).reshape(-1,3)) # coef_, intercept_
#print(Y_pred)
# Y_pred = w0 + w1*X  ---_>
#Y_n = v.intercept_ + v.coef_[0]*8 + v.coef_[1]*8*8 + v.coef_[2]*8*8*8
#print(Y_n)
# Y_pred = w0 + w1*X + w2*np.power(X,2) + w3*np.power(X,3) + w4*np.power(X,4) + w5*np.power(X,5) + w6*np.power(X,6) + w7*np.power(X,7) + w8*np.power(X,8)
# --------

fig = go.Figure()
fig.add_traces(go.Scatter(
     x=X.reshape(-1), #df["data"].values,
     y=y
))
fig.add_traces(go.Scatter(
     x = X.reshape(-1), #df["data"].values,
     y=Y_pred
))
#fig.show()
fig.write_html("results.html")
