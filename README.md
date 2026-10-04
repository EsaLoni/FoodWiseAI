# FoodWiseAI
Detecting Food Waste and usaage

# 🍽️ FoodWise AI – Smart Food Demand Intelligence Platform

## 📌 Project Overview
FoodWise AI is a data analytics and machine learning project designed to help restaurants understand food demand patterns, forecast future demand, and identify potential high-demand situations. The platform combines data cleaning, exploratory data analysis (EDA), machine learning, and an interactive Streamlit dashboard to support data-driven restaurant planning.

## 🎯 Project Objectives
- Analyze restaurant food demand patterns across different dates, menu items, and locations.
- Forecast food demand using machine learning regression models.
- Classify potential high-demand situations to support proactive planning.
- Evaluate model performance using appropriate machine learning metrics.
- Visualize demand trends and model performance through an interactive dashboard.

## 🛠️ Technologies Used
- **Python** – Data processing and model development
- **Pandas & NumPy** – Data manipulation and analysis
- **Matplotlib & Seaborn** – Exploratory data visualization
- **Scikit-learn** – Machine learning and model evaluation
- **Plotly** – Interactive charts
- **Streamlit** – Interactive dashboard
- **Jupyter Notebook** – Analysis and experimentation
- **Git & GitHub** – Version control and project hosting

## 📊 Key Features
- Data cleaning and missing-value handling
- Exploratory data analysis of restaurant and menu-item demand
- Demand forecasting using regression models
- High-demand classification using machine learning
- Model evaluation using MAE, RMSE, R², precision, recall, F1-score, and Average Precision
- Error analysis to identify menu items and restaurants where predictions need improvement
- Interactive dashboard for demand analysis and model performance visualization

## 🤖 Machine Learning Approach

### 1. Demand Forecasting
Regression models predict food demand quantities based on historical demand and relevant restaurant, menu-item, calendar, and weather features.

### 2. High-Demand Classification
A classification model identifies potential high-demand cases using a defined demand threshold. Model performance is evaluated with particular attention to precision, recall, and F1-score because high-demand cases are relatively rare.

### 3. Model Evaluation
Models are assessed using validation data and held-out test data to understand prediction accuracy, missed high-demand cases, and false alerts.

## 📈 Business Value
- Helps restaurants understand demand variations.
- Supports better food preparation and inventory planning.
- Highlights menu items and restaurants that may require closer monitoring.
- Provides insights that can support efforts to reduce overproduction and food waste.

**Important limitation:** The current dataset supports demand forecasting and high-demand prediction. It does not directly measure food waste because actual prepared, sold, and discarded quantities are not available.

## 🚀 Run the Dashboard Locally

### Prerequisites
Install Python and the required libraries.

### Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd FoodWiseAI
```

Install the required packages:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn plotly streamlit jupyter
```

Run the Streamlit dashboard:

```bash
python -m streamlit run app.py
```

Ensure the required CSV files are in the same directory as `app.py`.

## 📁 Project Structure

```text
FoodWiseAI/
│
├── app.py
├── foodwise_model_data.csv
├── forecast_evaluation.csv
├── menu_performance.csv
├── high_demand_error_analysis.csv
├── notebooks/
│   └── foodwise_analysis.ipynb
├── requirements.txt
└── README.md
```

*Adjust the structure above to match the files actually included in your repository.*

## 🔮 Future Improvements
- Integrate actual food preparation, sales, and waste records.
- Estimate food waste using prepared quantity minus sold quantity, with adjustments for inventory and other factors.
- Improve forecasting with additional historical demand features.
- Add automated alerts for unusual demand patterns.
- Deploy the dashboard for wider access.

## 👨‍💻 Author
**Esa**  
Aspiring Data Analyst | Python | SQL | Pandas | Machine Learning | Data Visualization

## ⭐ Project Goal
To demonstrate practical skills in data analytics, machine learning, model evaluation, and dashboard development through a restaurant demand intelligence use case.
