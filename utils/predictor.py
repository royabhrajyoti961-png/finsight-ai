import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_spending(df):
    """
    Predict future spending based on past transaction data.
    Uses simple Linear Regression on time series.
    """

    # ❌ Not enough data
    if df is None or len(df) < 5:
        return None

    try:
        df = df.copy()

        # Convert Date column
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        # Create time index
        df["day_index"] = np.arange(len(df))

        # Features and target
        X = df[["day_index"]]
        y = df["Amount"]

        # Train model
        model = LinearRegression()
        model.fit(X, y)

        # Predict next 5 days average
        future_days = np.array([[len(df) + i] for i in range(1, 6)])
        predictions = model.predict(future_days)

        # Return average prediction
        return round(predictions.mean(), 2)

    except Exception as e:
        print("Prediction Error:", e)
        return None
