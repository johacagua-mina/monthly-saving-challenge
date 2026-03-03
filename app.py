import matplotlib.pyplot as plt
from savings import load_data, upsert_month, build_monthly_analysis, total_savings


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
    print("4) Exit")


def show_report() -> None:
    df = load_data()
    if df.empty:
        print("No data yet. Add a month first.")
        return

    report = build_monthly_analysis(df)
    cols = ["month", "target", "actual", "gap", "achieved_pct", "cumulative_actual", "cumulative_gap"]
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
    plt.plot(report["month"], report["target"], marker="o")
    plt.plot(report["month"], report["actual"], marker="o")
    plt.xticks(rotation=45, ha="right")
    plt.title("Monthly Savings: Target vs Actual")
    plt.xlabel("Month")
    plt.ylabel("Amount (£)")
    plt.tight_layout()
    plt.show()


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

            elif choice == "4":
                print("Bye.")
                return

            else:
                print("Invalid option.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
   
