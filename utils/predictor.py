import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_spending(df):
    if len(df) < 5:
        return None

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    df['day'] = np.arange(len(df))

    X = df[['day']]
    y = df['amount']

    model = LinearRegression()
    model.fit(X, y)

    future_day = [[len(df) + 5]]
    prediction = model.predict(future_day)

    return round(prediction[0], 2)
