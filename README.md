# CryptoPositionSizeCalculator

A Python calculator for leveraged crypto position sizing: how much to risk, how large a position that risk allows, risk/reward, and a simplified liquidation price.

## Installation

No third-party dependencies. Requires Python 3.9 or later.

## Usage

```bash
python position_size.py \
  --balance 10000 --risk-pct 1 \
  --entry 60000 --stop-loss 59000 --take-profit 63000 \
  --leverage 10 --side long
```

Example output:

```json
{
  "risk_amount": 100.0,
  "position_coins": 0.1,
  "position_notional": 6000.0,
  "risk_reward": 3.0,
  "liquidation_price": 54300.0
}
```

## How it works

- Risk amount = `balance * risk_pct / 100`.
- Position size in coins = `risk_amount / |entry - stop_loss|`.
- Risk/reward = `|take_profit - entry| / |entry - stop_loss|`.
- Simplified liquidation, long = `entry * (1 - 1/leverage + maintenance_margin)`, short = `entry * (1 + 1/leverage - maintenance_margin)`, with a default 0.5% maintenance margin in the function.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Limitations

- This is a calculator, not financial advice and not a trading bot.
- Real liquidation prices depend on the exchange's margin, funding, fees, and position mode. Treat the liquidation figure as an estimate, not a guarantee.
- It does not connect to any exchange or wallet and never needs a private key.

## License

MIT. See `LICENSE`.
