import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# Load the hidden .env file so Python can access the API key safely
load_dotenv()

def generate_business_summary(df):
    """Extracts the latest metrics and asks Gemini to summarize the situation."""
    
    # 1. Setup the Gemini API Connection
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API Key missing. Please add GEMINI_API_KEY to your .env file.")
    
    genai.configure(api_key=api_key)
    
    # We use gemini-1.5-flash because it is extremely fast and cost-effective for text tasks
    model = genai.GenerativeModel('gemini-3.6-flash') 
    
    # 2. Extract only the most recent day's data
    latest_data = df.iloc[-1]
    report_date = latest_data["Date"].strftime("%Y-%m-%d")
    
    # Filter for the base metric names
    metrics = [col for col in df.columns if not any(suffix in col for suffix in ["_Baseline", "_Pct_Change", "_Z_Score", "_Anomaly", "Date"])]
    
    anomalies = []
    normal_metrics = []
    
    # 3. Sort the metrics into "Broken" and "Normal" to feed the AI
    for metric in metrics:
        current_val = latest_data[metric]
        baseline = latest_data[f"{metric}_Baseline_Avg"]
        pct_change = latest_data[f"{metric}_Pct_Change"]
        is_anomaly = latest_data[f"{metric}_Anomaly"]
        
        detail = f"- {metric}: {current_val:.2f} (Expected: {baseline:.2f} | Shift: {pct_change:+.1f}%)"
        
        if is_anomaly:
            anomalies.append(detail)
        else:
            normal_metrics.append(detail)
            
    # 4. If nothing is broken, don't waste money calling the API
    if not anomalies:
        return f"{report_date} Summary: All metrics are operating within normal baseline ranges. No anomalies detected."
        
    # 5. Build the Prompt
    system_instructions = (
        "You are a senior data analyst reporting to a VP of Operations. "
        "Review the following daily metrics and write a concise, 3-sentence summary of the situation. "
        "Focus heavily on the anomalous metrics and try to logically connect them. "
        "Do not use statistical jargon like 'Z-scores'. Speak in clear, direct business terms."
    )
    
    data_context = (
        f"Date: {report_date}\n\n"
        f"ANOMALOUS METRICS (ACTION REQUIRED):\n" + "\n".join(anomalies) + "\n\n"
        f"NORMAL METRICS (FOR CONTEXT):\n" + "\n".join(normal_metrics)
    )
    
    prompt = f"{system_instructions}\n\n{data_context}"
    
    # 6. Make the API Call
    print("[*] Contacting Gemini API for narrative generation...")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"

