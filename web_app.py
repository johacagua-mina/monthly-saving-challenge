from exchange_api import convert_gbp
import streamlit as st
from savings import load_data, upsert_month
from nudges import generate_nudge, log_reminder

st.set_page_config(page_title="OuchSavings", page_icon="💸")
st.title("OuchSavings 💸")
st.caption("Behavioural finance savings tracker with motivational WhatsApp nudges.")

tab1, tab2 = st.tabs(["Add / Update month", "Generate WhatsApp nudge"])

with tab1:
    st.subheader("Add / Update month")
    month = st.text_input("Month (YYYY-MM)", value="2026-03")
    target = st.number_input("Monthly target (£)", min_value=0.0, value=200.0, step=10.0)
    actual = st.number_input("Actual saved (£)", min_value=0.0, value=120.0, step=10.0)

    if st.button("Save ✅"):
        upsert_month(month.strip(), float(target), float(actual))
        st.success("Saved!")

with tab2:
    st.subheader("Generate WhatsApp nudge")
    df = load_data()
    if df.empty:
        st.info("No data yet. Add a month first.")
    else:
        month_list = df["month"].tolist()
        pick = st.selectbox("Pick month", month_list)

        row = df[df["month"] == pick].iloc[0]
        target = float(row["target"])
        actual = float(row["actual"])
        progress = actual / target if target > 0 else 0

        st.write(f"Target: £{target}")
        st.write(f"Saved: £{actual}")

        st.progress(min(progress, 1.0))
        st.write(f"Progress: {progress:.0%}")
        

        mood = st.selectbox("Mood", ["sarcastic_coach", "supportive", "neutral"], index=0)

        if st.button("Generate nudge 💬"):
            n = generate_nudge(pick, target, actual, mood=mood)
            log_reminder(n, channel="whatsapp", status="draft")

            st.text_area("Copy/paste to WhatsApp", value=n.message, height=140)
            st.write("✅ Logged to `data/reminders.csv`")
    st.write(
    "Track your monthly savings and receive slightly sarcastic behavioural nudges to stay financially disciplined."
)   
    usd_value = convert_gbp(actual, "USD")
    st.write(f"Approx value in USD: ${usd_value:.2f}")         