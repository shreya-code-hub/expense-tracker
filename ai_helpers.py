import os
import io
import json
import numpy as np
from datetime import datetime, date
from calendar import monthrange
from models import db, Transaction, Budget

# Local Category Predictor using Naive Bayes
def predict_category(user_id, description):
    if not description:
        return None
        
    # Fetch historical transactions of type expense
    txs = Transaction.query.filter_by(user_id=user_id, type='expense').all()
    if len(txs) < 3:
        return None
        
    descriptions = [t.description for t in txs if t.description and t.category]
    categories = [t.category for t in txs if t.description and t.category]
    
    if len(descriptions) < 3:
        return None
        
    # Check if all transactions are classified under a single category
    unique_cats = list(set(categories))
    if len(unique_cats) == 1:
        return unique_cats[0]
        
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.pipeline import make_pipeline
        
        # Create pipeline: vectorize and classify
        model = make_pipeline(
            TfidfVectorizer(lowercase=True, stop_words='english'),
            MultinomialNB()
        )
        model.fit(descriptions, categories)
        
        pred = model.predict([description])[0]
        return pred
    except Exception as e:
        print(f"Classifier error: {e}")
        return None

# Local Spend Forecaster using Linear Regression
def forecast_spends(user_id, year, month):
    now = date.today()
    _, num_days = monthrange(year, month)
    
    # Query current month expenses
    txs = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.type == 'expense',
        db.extract('year', Transaction.date) == year,
        db.extract('month', Transaction.date) == month
    ).order_by(Transaction.date.asc()).all()
    
    # Aggregate spending per day
    daily_spends = {d: 0.0 for d in range(1, num_days + 1)}
    for t in txs:
        day = t.date.day
        daily_spends[day] += t.amount
        
    # Calculate cumulative spend arrays
    cumulative = []
    current_sum = 0.0
    
    max_actual_day = num_days
    if year == now.year and month == now.month:
        max_actual_day = now.day
        
    for d in range(1, max_actual_day + 1):
        current_sum += daily_spends[d]
        cumulative.append(current_sum)
        
    forecast_days = []
    forecast_values = []
    
    if len(cumulative) >= 2:
        try:
            from sklearn.linear_model import LinearRegression
            # X = days, Y = cumulative spending
            X = np.array(range(1, max_actual_day + 1)).reshape(-1, 1)
            Y = np.array(cumulative)
            
            reg = LinearRegression()
            reg.fit(X, Y)
            
            # Predict for all days in the month
            for d in range(1, num_days + 1):
                pred_val = reg.predict([[d]])[0]
                pred_val = max(0.0, float(pred_val))
                forecast_days.append(d)
                forecast_values.append(pred_val)
        except Exception as e:
            print(f"Regression forecasting error: {e}")
            
    # Fallback to daily average if model training fails or data is sparse
    if not forecast_values and len(cumulative) >= 1:
        avg_velocity = cumulative[-1] / len(cumulative)
        for d in range(1, num_days + 1):
            forecast_days.append(d)
            forecast_values.append(avg_velocity * d)
            
    return {
        "actual_days": list(range(1, len(cumulative) + 1)),
        "actual_values": cumulative,
        "forecast_days": forecast_days,
        "forecast_values": forecast_values
    }

# Gemini AI Chat Client
def gemini_chat_response(api_key, context_data, user_message):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        system_prompt = (
            "You are Expenso, a premium AI personal finance advisor chatbot inside an Expense Tracker application. "
            "Your tone is helpful, encouraging, and professional. Use formatting (bold text, lists, and emojis) where appropriate. "
            "Below is the real-time financial context of the logged-in user:\n\n"
            f"{context_data}\n\n"
            "Analyze this context and answer the user's message. If they ask about their balance, category expenses, "
            "or budget alerts, refer directly to the metrics provided in the context. "
            "If they ask general questions, provide smart financial recommendations. Reply in the user's language (matching the tone of their greeting)."
        )
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"{system_prompt}\n\nUser: {user_message}")
        
        resp_text = response.text.strip().replace("\n", "<br>")
        return resp_text
    except Exception as e:
        print(f"Gemini Chat error: {e}")
        return f"Expenso: I encountered an error connecting to the AI model. Details: {str(e)}"

# Gemini Receipt Scanner Vision
def gemini_scan_receipt(api_key, file_data, mimetype):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            "Analyze this receipt image. Extract the transaction details and return them strictly in JSON format. "
            "Do not include any markdown fences, backticks, or explanation. "
            "Use this exact schema:\n"
            "{\n"
            '  "amount": float,\n'
            '  "category": "Food" | "Travel" | "Shopping" | "Bills" | "Entertainment" | "Other",\n'
            '  "description": "Merchant Name / Short Description",\n'
            '  "date": \"YYYY-MM-DD\"\n'
            "}\n"
            "If you cannot determine a field, return a reasonable estimate or leave it blank."
        )
        
        image_part = {
            "mime_type": mimetype,
            "data": file_data
        }
        
        response = model.generate_content([prompt, image_part])
        text = response.text.strip()
        
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
            
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Gemini Vision error: {e}")
        raise e
