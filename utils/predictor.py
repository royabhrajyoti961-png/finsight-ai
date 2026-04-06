import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def prepare_data(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    # Daily aggregation
    daily = df.groupby("Date")["Amount"].sum().reset_index()
    daily["day_index"] = np.arange(len(daily))

    return daily

def predict_future(df, days=7):
    if df is None or len(df) < 5:
        return None, None

    daily = prepare_data(df)

    X = daily[["day_index"]]
    y = daily["Amount"]

    model = LinearRegression()
    model.fit(X, y)

    # Future prediction
    future_index = np.arange(len(daily), len(daily)+days)
    future_index = future_index.reshape(-1,1)

    predictions = model.predict(future_index)

    future_dates = pd.date_range(
        start=daily["Date"].max(),
        periods=days+1
    )[1:]

    future_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted": predictions
    })

    return daily, future_df


def generate_insights(df):
    insights = []

    total = df["Amount"].sum()
    avg = df["Amount"].mean()

    # Category analysis
    cat = df.groupby("Category")["Amount"].sum()
    top_cat = cat.idxmax()

    insights.append(f"💸 You spend most on {top_cat}")

    # Overspending alert
    if avg > 500:
        insights.append("🚨 Your average spending is high. Try reducing daily expenses.")

    # Saving suggestion
    if "Food" in cat and cat["Food"] > 0.4 * total:
        insights.append("🍔 High food spending. Consider cooking more at home.")

    insights.append("📊 Track your daily trends to improve savings.")

    return insights
