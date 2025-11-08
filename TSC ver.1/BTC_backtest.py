import pandas as pd
import numpy as np

# ===== 설정 =====
CSV_PATH      = "btc_5m.csv"
SYMBOL        = "BTC/USDT"
TIMEFRAME     = "5m"

INITIAL_CAP   = 10000.0
LEVERAGE      = 10
FEE_RATE      = 0.0005
SLIPPAGE_PCT  = 0.0000

TP_PCT        = 0.002
SL_PCT        = 0.0014

EMA_FAST      = 10
EMA_SLOW      = 20
RSI_PERIOD    = 14

# ===== 데이터 로드 =====
df = pd.read_csv(CSV_PATH)
df.columns = [c.lower() for c in df.columns]
need = {"open","high","low","close"}
if not need.issubset(df.columns):
    raise ValueError(f"CSV must include columns: {need}")

# ===== 지표 계산 =====
df["ema_fast"] = df["close"].ewm(span=EMA_FAST, adjust=False).mean()
df["ema_slow"] = df["close"].ewm(span=EMA_SLOW, adjust=False).mean()

delta = df["close"].diff()
gain = np.where(delta > 0, delta, 0)
loss = np.where(delta < 0, -delta, 0)
avg_gain = pd.Series(gain).rolling(RSI_PERIOD).mean()
avg_loss = pd.Series(loss).rolling(RSI_PERIOD).mean()
rs = avg_gain / avg_loss
df["rsi"] = 100 - (100 / (1 + rs))

df["bull"] = df["close"] > df["open"]
df["bear"] = df["close"] < df["open"]

# ===== 유틸 =====
def first_touch_long(high_, low_, tp, sl):
    if low_ <= sl: return "SL"
    if high_ >= tp: return "TP"
    return None

def first_touch_short(high_, low_, tp, sl):
    if high_ >= sl: return "SL"
    if low_  <= tp: return "TP"
    return None

# ===== 시뮬 =====
equity = INITIAL_CAP
equity_curve = np.zeros(len(df))
position_qty = 0.0
entry_px = None
entry_idx = None
trades = []

# === 상태 관리 ===
# state: 0=대기, 1=세트 첫캔들확정, 2=연속2확인, 3=연속3확정(진입대기)
state = 0
set_dir = 0  # +1 롱 세트, -1 숏 세트
anchor_idx = None
pending_entry = None

for i in range(len(df)):

    # === 포지션 보유중 TP/SL 체크 ===
    if position_qty != 0.0 and entry_px is not None:
        hi, lo = df.at[i, "high"], df.at[i, "low"]
        if position_qty > 0:
            tp, sl = entry_px*(1+TP_PCT), entry_px*(1-SL_PCT)
            out = first_touch_long(hi, lo, tp, sl)
        else:
            tp, sl = entry_px*(1-TP_PCT), entry_px*(1+SL_PCT)
            out = first_touch_short(hi, lo, tp, sl)

        if out:
            exit_px = tp if out=="TP" else sl
            fee = abs(position_qty)*exit_px*FEE_RATE
            pnl = (exit_px - entry_px)*position_qty - fee
            equity += pnl
            trades.append({"dir":"LONG" if position_qty>0 else "SHORT",
                           "entry_idx":entry_idx, "exit_idx":i,
                           "entry":entry_px, "exit":exit_px,
                           "pnl":pnl, "balance":equity})
            position_qty = 0.0
            entry_px = None
            entry_idx = None
            state = 0  # 세트 리셋

    # === 예약 진입 ===
    if pending_entry and pending_entry["index"] == i and position_qty == 0.0:
        open_px = df.at[i, "open"]
        fill_px = open_px * (1 + SLIPPAGE_PCT)
        notional = equity * LEVERAGE
        qty = notional / fill_px
        fee = qty * fill_px * FEE_RATE
        equity -= fee
        position_qty = qty * (1 if pending_entry["dir"]>0 else -1)
        entry_px = fill_px
        entry_idx = i
        pending_entry = None
        state = 0  # 리셋 후 대기상태로

    # === 세트 판정 로직 ===
    if position_qty == 0.0:  # 무포지션 상태에서만
        c, o = df.at[i, "close"], df.at[i, "open"]
        ema_fast = df.at[i, "ema_fast"]
        ema_slow = df.at[i, "ema_slow"]
        rsi_val  = df.at[i, "rsi"]
        bull = df.at[i, "bull"]
        bear = df.at[i, "bear"]

        # ----- 상태 0: 첫캔들 대기 -----
        if state == 0:
            if bull and (ema_fast < ema_slow) and (rsi_val > 50):
                state = 1
                set_dir = +1
                anchor_idx = i
            elif bear and (ema_fast > ema_slow) and (rsi_val < 50):
                state = 1
                set_dir = -1
                anchor_idx = i

        # ----- 상태 1~2: 연속 방향 체크 -----
        elif state in [1, 2]:
            if set_dir == +1 and bull:
                state += 1
            elif set_dir == -1 and bear:
                state += 1
            else:
                # 방향 깨짐 → 세트 리셋
                state = 0
                set_dir = 0
                anchor_idx = None

        # ----- 상태 3: 3연속 확정 → 다음 봉 시가 진입 예약 -----
        elif state == 3:
            if i + 1 < len(df):
                pending_entry = {"dir": set_dir, "index": i + 1}
            state = 0
            set_dir = 0
            anchor_idx = None

    # === equity 업데이트 ===
    mark = df.at[i, "close"]
    if position_qty != 0.0 and entry_px:
        unreal = (mark - entry_px) * position_qty
        equity_curve[i] = max(equity + unreal, 1e-6)
    else:
        equity_curve[i] = equity

# ===== 리포트 =====
trades_df = pd.DataFrame(trades)
trades_df.to_csv("trades.csv", index=False)
pd.DataFrame({"equity":equity_curve}).to_csv("equity_curve.csv", index=False)

if len(trades_df) == 0:
    print("No trades.")
else:
    wins = trades_df[trades_df["pnl"] > 0]
    losses = trades_df[trades_df["pnl"] <= 0]
    total_pnl = trades_df["pnl"].sum()
    win_rate = len(wins)/len(trades_df)*100 if len(trades_df)>0 else 0
    peak = np.maximum.accumulate(equity_curve)
    dd = (equity_curve - peak) / peak
    mdd = dd.min() * 100

    print(f"Symbol/TF: {SYMBOL}/{TIMEFRAME}")
    print(f"Trades   : {len(trades_df)}")
    print(f"Win rate : {win_rate:.2f}%")
    print(f"Total PnL: {total_pnl:.2f}")
    print(f"MDD      : {mdd:.2f}%")
    print(f"Final Eq : {equity_curve[-1]:.2f}")