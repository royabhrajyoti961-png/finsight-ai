import pandas as pd

def generate_ai_advice(df, question=""):
    if df is None or df.empty:
        return "Add some expenses first so I can analyze your spending."

    total = df["Amount"].sum()
    avg = df["Amount"].mean()

    category_spend = df.groupby("Category")["Amount"].sum()
    top_category = category_spend.idxmax()

    advice = []

    # General insights
    advice.append(f"💰 Your total spending is ₹ {round(total,2)}")
    advice.append(f"📊 Your average expense is ₹ {round(avg,2)}")

    # Category insight
    advice.append(f"📂 You spend most on {top_category}")

    # Smart suggestions
    if avg > 500:
        advice.append("🚨 Your daily average is high. Try setting a daily budget.")

    if "Food" in category_spend and category_spend["Food"] > 0.4 * total:
        advice.append("🍔 You spend a lot on food. Try cooking at home more often.")

    if "Shopping" in category_spend and category_spend["Shopping"] > 0.3 * total:
        advice.append("🛍️ Reduce impulse shopping. Wait 24 hours before buying.")

    advice.append("📉 Track expenses weekly to identify patterns and reduce waste.")

    # Answer custom question
    if question:
        if "reduce" in question.lower():
            advice.append("💡 Focus on cutting non-essential expenses like subscriptions, eating out, and impulse buying.")
        elif "save" in question.lower():
            advice.append("💡 Try the 50/30/20 rule: Needs/Wants/Savings.")
        else:
            advice.append("💡 Ask me about saving, budgeting, or reducing expenses!")

    return "\n\n".join(advice)
