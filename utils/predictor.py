import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_spending(df):
    if len(df) < 5:
        return None

    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    df['day'] = np.arange(len(df))

    X = df[['day']]
    y = df['Amount']

    model = LinearRegression()
    model.fit(X, y)

    future = [[len(df) + 5]]
    prediction = model.predict(future)

    return round(prediction[0], 2)
