import ccxt
import pandas as pd
import time
import os

# ===== 파라미터 =====
SYMBOL       = "ETH/USDT"
TIMEFRAME    = "5m"
LIMIT_PER_CALL = 1500
TARGET_CANDLES = 100000        # ← 원하는 총 캔들 수 (예: 100000, 200000, 400000, 500000)
START_ISO      = "2024-06-01T00:00:00Z"  # ← 더 과거부터 받고 싶으면 앞당기기
CSV_NAME    = "eth_5m.csv"
APPEND_IF_EXISTS = False       # True면 파일 있으면 이어받기, False면 항상 새로 시작(덮어쓰기)

# ===== 거래소 =====
exchange = ccxt.binance()
print(f"[INFO] SYMBOL={SYMBOL}, TF={TIMEFRAME}, TARGET={TARGET_CANDLES}, START={START_ISO}, APPEND={APPEND_IF_EXISTS}")

# ===== 기존 파일 처리 (이어받기) =====
existing = None
if os.path.exists(CSV_NAME):
    if APPEND_IF_EXISTS:
        try:
            existing = pd.read_csv(CSV_NAME)
            if set(["timestamp","open","high","low","close","volume"]).issubset(existing.columns):
                print(f"[INFO] Found existing file: {CSV_NAME}  rows={len(existing)}")
            else:
                print("[WARN] Existing CSV columns are unexpected; ignoring it.")
                existing = None
        except Exception as e:
            print(f"[WARN] Failed to read existing CSV ({e}); ignoring.")
            existing = None
    else:
        print(f"[INFO] Overwrite mode. Existing file {CSV_NAME} will be replaced.")

# ===== 시작점 계산 =====
if existing is not None and len(existing) > 0:
    # 마지막 행 다음부터 이어받기
    last_ts = pd.to_datetime(existing["timestamp"].iloc[-1])
    since_ms = int(last_ts.value // 1_000_000) + 1  # ns -> ms
    collected = len(existing)
    rows = existing[["timestamp","open","high","low","close","volume"]].copy()
    print(f"[INFO] Resume from last timestamp: {last_ts}  (ms={since_ms})")
else:
    since_ms = exchange.parse8601(START_ISO)
    collected = 0
    rows = pd.DataFrame(columns=["timestamp","open","high","low","close","volume"])
    print(f"[INFO] Start fresh from {START_ISO} (ms={since_ms})")

# ===== 수집 루프 =====
while True:
    if collected >= TARGET_CANDLES:
        break

    bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, since=since_ms, limit=LIMIT_PER_CALL)
    if not bars:
        print("[INFO] No more bars returned. Stopping.")
        break

    df = pd.DataFrame(bars, columns=["timestamp","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # 기존 rows와 겹치는 구간 제거
    if len(rows) > 0:
        last_time = rows["timestamp"].iloc[-1]
        df = df[df["timestamp"] > last_time]

    if len(df) == 0:
        print("[INFO] No new bars (possibly reached latest). Stopping.")
        break

    rows = pd.concat([rows, df], ignore_index=True)
    collected = len(rows)

    print(f"[INFO] Collected: {collected} (last={rows['timestamp'].iloc[-1]})")

    # 다음 요청 시작점 갱신
    since_ms = int(df["timestamp"].iloc[-1].value // 1_000_000) + 1

    # API rate limit
    time.sleep(exchange.rateLimit / 1000)

    # 안전 저장 (주기적으로 저장)
    if collected % 10000 < LIMIT_PER_CALL:
        rows.to_csv(CSV_NAME, index=False)
        print(f"[INFO] Autosaved to {CSV_NAME} (rows={collected})")

# 최종 저장
rows.to_csv(CSV_NAME, index=False)
print(f"[DONE] Saved {len(rows)} rows to {CSV_NAME}")