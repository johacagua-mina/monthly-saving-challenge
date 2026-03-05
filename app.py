from __future__ import annotations

import matplotlib.pyplot as plt

from savings import load_data, upsert_month, build_monthly_analysis, total_savings
from nudges import generate_nudge, log_reminder


def prompt_float(msg: str) -> float:
    value = float(input(msg).strip().replace(",", ""))
    if value < 0:
        raise ValueError("Value cannot be negative.")
    return value


def menu() -> None:
    print("\n=== Monthly Saving Challenge ===")
    print("1) Add/Update month saving")
    print("2) Show report")
    print("3) Plot progress")
    print("5) Generate WhatsApp reminder (copy-ready)")
    print("4) Exit")


def show_report() -> None:
    df = load_data()
    if df.empty:
        print("No data yet. Add a month first.")
        return

    report = build_monthly_analysis(df)
    cols = ["month", "target", "actual", "gap", "achieved_pct", "cumulative_actual"]

    print("\n--- Per-month analysis ---")
    print(report[cols].to_string(index=False))

    print("\n--- Totals ---")
    print(f"Total savings: £{total_savings(df):.2f}")


def plot_progress() -> None:
    df = load_data()
    if df.empty:
        print("No data yet. Add a month first.")
        return

    report = build_monthly_analysis(df)

    plt.figure()
    plt.plot(report["month"], report["target"], marker="o", label="Target")
    plt.plot(report["month"], report["actual"], marker="o", label="Actual")
    plt.xticks(rotation=45, ha="right")
    plt.title("Monthly Savings: Target vs Actual")
    plt.xlabel("Month")
    plt.ylabel("Amount (£)")
    plt.legend()
    plt.tight_layout()
    plt.show()


def whatsapp_reminder() -> None:
    df = load_data()
    if df.empty:
        print("No data yet. Add a month first.")
        return

    month = input("Month (YYYY-MM): ").strip()
    row = df[df["month"] == month]
    if row.empty:
        print("Month not found. Add it first.")
        return

    target = float(row.iloc[0]["target"])
    actual = float(row.iloc[0]["actual"])

    nudge = generate_nudge(month, target, actual, mood="sarcastic_coach")
    log_reminder(nudge, channel="whatsapp", status="draft")

    print("\n--- WhatsApp message (copy/paste) ---")
    print(nudge.message)
    print("-----------------------------------")


def main() -> None:
    while True:
        menu()
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                month = input("Month (YYYY-MM): ").strip()
                target = prompt_float("Monthly target (£): ")
                actual = prompt_float("Actual saved (£): ")
                upsert_month(month, target, actual)
                print("Saved ✅")

            elif choice == "2":
                show_report()

            elif choice == "3":
                plot_progress()

            elif choice == "5":
                whatsapp_reminder()

            elif choice == "4":
                print("Bye.")
                return

            else:
                print("Invalid option.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()