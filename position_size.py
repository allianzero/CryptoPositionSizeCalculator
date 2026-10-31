"""Position-size, risk, and liquidation calculator for leveraged crypto.

Given an account balance, a risk percentage, an entry price, and a
stop-loss price, this module computes how much to risk, the position
size in coins and in notional value, the risk/reward ratio, and a
simplified liquidation price for long and short positions. It does
not trade and does not connect to any exchange.
"""
import argparse
import json
import sys


def risk_amount(account_balance, risk_pct):
    if account_balance < 0 or risk_pct < 0:
        raise ValueError("balance and risk_pct must be non-negative")
    return account_balance * risk_pct / 100


def position_size_coins(account_balance, risk_pct, entry, stop_loss):
    distance = abs(entry - stop_loss)
    if distance == 0:
        raise ValueError("entry and stop_loss must differ")
    if entry <= 0 or stop_loss <= 0:
        raise ValueError("prices must be positive")
    return risk_amount(account_balance, risk_pct) / distance


def position_notional(coins, entry):
    return coins * entry


def risk_reward(entry, stop_loss, take_profit):
    risk = abs(entry - stop_loss)
    reward = abs(take_profit - entry)
    if risk == 0:
        raise ValueError("entry and stop_loss must differ")
    return reward / risk


def liquidation_price(entry, leverage, side, maintenance_margin_pct=0.5):
    """Simplified liquidation price.

    Long:  entry * (1 - 1/leverage + maintenance_margin/100)
    Short: entry * (1 + 1/leverage - maintenance_margin/100)
    Maintenance margin is a small buffer; real exchanges use their own
    margin, funding, and fee rules, so treat this as an estimate.
    """
    if leverage <= 0:
        raise ValueError("leverage must be positive")
    if side not in ("long", "short"):
        raise ValueError("side must be 'long' or 'short'")
    mm = maintenance_margin_pct / 100
    if side == "long":
        return entry * (1 - 1 / leverage + mm)
    return entry * (1 + 1 / leverage - mm)


def summarize(account_balance, risk_pct, entry, stop_loss, take_profit, leverage, side):
    coins = position_size_coins(account_balance, risk_pct, entry, stop_loss)
    return {
        "risk_amount": risk_amount(account_balance, risk_pct),
        "position_coins": coins,
        "position_notional": position_notional(coins, entry),
        "risk_reward": risk_reward(entry, stop_loss, take_profit),
        "liquidation_price": liquidation_price(entry, leverage, side),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Crypto position size calculator")
    parser.add_argument("--balance", required=True, type=float)
    parser.add_argument("--risk-pct", required=True, type=float)
    parser.add_argument("--entry", required=True, type=float)
    parser.add_argument("--stop-loss", required=True, type=float)
    parser.add_argument("--take-profit", required=True, type=float)
    parser.add_argument("--leverage", required=True, type=float)
    parser.add_argument("--side", required=True, choices=["long", "short"])
    args = parser.parse_args(argv)
    try:
        result = summarize(args.balance, args.risk_pct, args.entry,
                           args.stop_loss, args.take_profit, args.leverage, args.side)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
