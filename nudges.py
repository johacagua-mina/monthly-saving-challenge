from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")
REMINDERS_CSV = DATA_DIR / "reminders.csv"


@dataclass
class Nudge:
    month: str
    mood: str
    message: str


def _ensure_reminders_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not REMINDERS_CSV.exists():
        pd.DataFrame(columns=["date", "month", "channel", "mood", "message", "status"]).to_csv(
            REMINDERS_CSV, index=False
        )


def _money(x: float) -> str:
    return f"£{x:.2f}".replace(".00", "")


def generate_nudge(month: str, target: float, actual: float, mood: str = "sarcastic_coach") -> Nudge:
    """
    Monzo-inspired, emotionally-driven reminder.
    Default mood: sarcastic_coach (A + C).
    """
    target = float(target)
    actual = float(actual)

    if target <= 0:
        msg = "Set a target first. Even your future self needs a number, not a vibe."
        return Nudge(month=month, mood=mood, message=msg)

    gap = actual - target
    pct = (actual / target) * 100.0

    if pct >= 110:
        msg = (
            f"Okay, show-off. You saved {_money(actual)} vs target {_money(target)} "
            f"({pct:.0f}%). Keep going — but don’t get cocky."
        )
    elif pct >= 100:
        msg = (
            f"Target hit ✅ {_money(actual)} saved ({pct:.0f}%). "
            f"Now protect the streak. Future-you is watching."
        )
    elif pct >= 75:
        needed = target - actual
        msg = (
            f"You’re close. {_money(actual)} saved ({pct:.0f}%). "
            f"Only {_money(needed)} left. Don’t fumble it now."
        )
    elif pct >= 40:
        needed = target - actual
        msg = (
            f"Reality check: {_money(actual)} saved ({pct:.0f}%). "
            f"You still owe yourself {_money(needed)} this month. No excuses — adjust the plan."
        )
    else:
        needed = target - actual
        msg = (
            f"Ouch. {_money(actual)} saved ({pct:.0f}%). "
            f"Target is {_money(target)}. You’re short by {_money(needed)}. "
            f"Today you choose: comfort or control."
        )

    # Coach-style line: avoid negative money confusion
    diff = actual - target

    if diff > 0:
        delta_line = f"Surplus: {_money(diff)}"
    elif diff < 0:
        delta_line = f"Shortfall: {_money(-diff)}"
    else:
        delta_line = "On target ✅"

    progress_line = f"Progress: {pct:.0f}% of monthly target"
    coach_line = f"{delta_line} | Target: {_money(target)} | Actual: {_money(actual)}"
    return Nudge(
    month=month,
    mood=mood,
    message=f"{msg}\n{progress_line}\n{coach_line}"
)


def log_reminder(nudge: Nudge, channel: str = "whatsapp", status: str = "draft") -> None:
    _ensure_reminders_storage()

    row = {
        "date": date.today().isoformat(),
        "month": nudge.month,
        "channel": channel,
        "mood": nudge.mood,
        "message": nudge.message,
        "status": status,
    }

    try:
        df = pd.read_csv(REMINDERS_CSV)
    except Exception:
        df = pd.DataFrame(columns=["date", "month", "channel", "mood", "message", "status"])

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(REMINDERS_CSV, index=False, encoding="utf-8")