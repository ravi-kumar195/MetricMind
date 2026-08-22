import os
import numpy as np
import pandas as pd
from email_dispatcher import send_email_alert
from narrative_agent import generate_business_summary

def create_mock_data(file_name="business_metrics.xlsx"):
    """Generates a sample 30-day dataset so you can test the script immediately."""
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30, freq="D")
    
    data = {
        "Date": dates,
        "Revenue": np.random.normal(loc=10000, scale=500, size=30),
        "Orders": np.random.normal(loc=200, scale=15, size=30),
        "Conversion_Rate": np.random.normal(loc=0.035, scale=0.002, size=30),
        "Traffic": np.random.normal(loc=5700, scale=300, size=30),
    }
    
    df = pd.DataFrame(data)
    
    # Inject an artificial anomaly on the final day for testing
    df.loc[df.index[-1], "Revenue"] = 4000  # A sharp drop
    df.loc[df.index[-1], "Traffic"] = 9000  # A sharp spike
    
    df.to_excel(file_name, index=False)
    print(f"[*] Created mock dataset: {file_name}")

def load_and_clean_data(file_name):
    """Reads the Excel file, standardizes columns, and sorts chronologically."""
    print(f"[*] Loading data from {file_name}...")
    df = pd.read_excel(file_name)
    
    # Standardize column names (remove spaces, make consistent)
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    
    # Ensure date column is properly typed and sorted
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    
    # Forward-fill any missing numeric data, then replace remaining NaNs with 0
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].ffill().fillna(0)
    
    return df

def calculate_metrics_and_anomalies(df, window=7, threshold=2.0):
    """Calculates rolling averages, standard deviations, and flags anomalies using Z-scores."""
    print(f"[*] Calculating {window}-day baselines and detecting anomalies...")
    processed_df = df.copy()
    
    # Identify all numeric columns except the Date
    metrics = processed_df.select_dtypes(include=[np.number]).columns
    
    for metric in metrics:
        # Calculate the moving average and standard deviation (shifted by 1 to exclude the current day from its own baseline)
        processed_df[f"{metric}_Baseline_Avg"] = processed_df[metric].shift(1).rolling(window=window, min_periods=3).mean()
        processed_df[f"{metric}_Baseline_Std"] = processed_df[metric].shift(1).rolling(window=window, min_periods=3).std()
        
        # Calculate the percentage change against the baseline
        processed_df[f"{metric}_Pct_Change"] = ((processed_df[metric] - processed_df[f"{metric}_Baseline_Avg"]) / processed_df[f"{metric}_Baseline_Avg"]) * 100
        
        # Calculate Z-Score: (Current Value - Baseline Average) / Baseline Standard Deviation
        std = processed_df[f"{metric}_Baseline_Std"].replace(0, np.nan) # Prevent division by zero
        processed_df[f"{metric}_Z_Score"] = (processed_df[metric] - processed_df[f"{metric}_Baseline_Avg"]) / std
        
        # Flag as anomaly if the absolute Z-Score exceeds our threshold
        processed_df[f"{metric}_Anomaly"] = processed_df[f"{metric}_Z_Score"].abs() > threshold

    return processed_df

def print_daily_report(df):
    """Outputs a clean, console-friendly report for the most recent day."""
    latest_data = df.iloc[-1]
    report_date = latest_data["Date"].strftime("%Y-%m-%d")
    
    print("\n" + "="*50)
    print(f"DAILY METRICS REPORT: {report_date}")
    print("="*50)
    
    # Extract the original metric names by filtering out our calculated columns
    metrics = [col for col in df.columns if not any(suffix in col for suffix in ["_Baseline", "_Pct_Change", "_Z_Score", "_Anomaly", "Date"])]
    
    anomalies_found = False
    
    for metric in metrics:
        current_val = latest_data[metric]
        baseline = latest_data[f"{metric}_Baseline_Avg"]
        pct_change = latest_data[f"{metric}_Pct_Change"]
        is_anomaly = latest_data[f"{metric}_Anomaly"]
        
        status_tag = "[ALERT]" if is_anomaly else "[ OK  ]"
        if is_anomaly:
            anomalies_found = True
            
        print(f"{status_tag} {metric.ljust(15)} | Value: {current_val:<10.2f} | 7-Day Avg: {baseline:<10.2f} | Shift: {pct_change:>+7.2f}%")
        
    print("-" * 50)
    if anomalies_found:
        print("⚠️  WARNING: Anomalies detected. Immediate review recommended.")
    else:
        print("✅  All metrics are operating within normal expected ranges.")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    EXCEL_FILE = "business_metrics.xlsx"

    # Day 1: Load Data & Run Math Baseline Engine
    if not os.path.exists(EXCEL_FILE):
        create_mock_data(EXCEL_FILE)

    clean_df = load_and_clean_data(EXCEL_FILE)
    processed_df = calculate_metrics_and_anomalies(clean_df)
    print_daily_report(processed_df)

    # Day 2: Generate AI Narrative Summary
    print("\nAI BUSINESS SUMMARY:")
    summary = generate_business_summary(processed_df)
    print(summary)

    # Day 3: Dispatch Automated Email Alert
    print("\nDISPATCHING ALERT:")
    send_email_alert(processed_df, summary)