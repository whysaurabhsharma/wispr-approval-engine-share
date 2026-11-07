"""Business case maths. All inputs visible; placeholders are reported, never hidden.
CLI: python scripts/build_case.py --users 142 --hours 1,2,4 --rate 60 --price 12,15
     --users per-seat gives per-user figures when no user count is known (public-signal accounts).
Prints a markdown table: one row per (hours, price) pair, plus the inputs and which are placeholders."""
import argparse, itertools
def build(active_users, hours_saved_per_user_month, loaded_cost_per_hour, price_per_user_month, placeholders=()):
    value = active_users * hours_saved_per_user_month * loaded_cost_per_hour
    cost = active_users * price_per_user_month
    return {"monthly_value": value, "monthly_cost": cost, "ratio": round(value / cost, 1) if cost else None,
            "annual_value": value * 12, "annual_cost": cost * 12,
            "value_at_half_hours": value / 2, "placeholders": list(placeholders)}
def nums(s): return [float(x) for x in s.split(",") if x.strip()]
def money(x): return f"${x:,.0f}" if x >= 100 else f"${x:,.2f}"
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", default="per-seat"); ap.add_argument("--hours", default="1,2,4")
    ap.add_argument("--rate", default="60"); ap.add_argument("--price", required=True)
    ap.add_argument("--placeholders", default="hours,rate")
    a = ap.parse_args()
    users = 1 if a.users == "per-seat" else int(a.users)
    unit = "per user" if a.users == "per-seat" else f"for {users} users"
    print(f"Inputs: users={a.users}; hours saved per user per month={a.hours}; loaded cost per hour=${a.rate}; price per user per month=${a.price}")
    print(f"Placeholders (not Wispr figures): {a.placeholders}\n")
    for p in nums(a.price):
        for rate in nums(a.rate):
            print(f"Break-even at ${p:g} per user per month and ${rate:g} per hour: {p / rate * 60:.0f} minutes saved per user per month.")
    print(f"\n| hours saved / user / month | price / user / month | monthly value ({unit}) | monthly cost ({unit}) | value / cost |")
    print("|---|---|---|---|---|")
    for h, p in itertools.product(nums(a.hours), nums(a.price)):
        for rate in nums(a.rate):
            r = build(users, h, rate, p)
            print(f"| {h:g} | ${p:g} | {money(r['monthly_value'])} | {money(r['monthly_cost'])} | {r['ratio']}x |")
