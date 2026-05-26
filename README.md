Project Title: Personal Performance OS, https://kwasi9911-personal-performance-os.streamlit.app/

The problem: Apps like Strava and Apple Fitness+ show you raw numbers like steps, calories, distance but they don't tell you what to do with them unless you pay for the subscription. They can't tell you whether you're overtraining, on pace to hit a goal, or having an unusually low-activity week compared to your own baseline. Personal Performance OS fills that gap by applying data science techniques such as recovery scoring, trend forecasting, and anomaly detection to your personal fitness data, giving you the kind of analytical clarity that professional sports teams have but everyday athletes don't.

Features:
Training Load & Recovery Score — Calculates a weekly score (0–100) based on your activity volume and intensity, then labels your week as Undertraining, Optimal, or Overtraining so you know whether to push harder or rest.
Goal Forecasting — Set a target (e.g. 70,000 weekly steps) and a linear regression model projects how many weeks it will take to get there based on your current trend, with an interactive chart showing the forecast alongside your actual data.
Anomaly Detection — Automatically flags weeks where your activity deviated significantly from your 4-week rolling average using z-score analysis, with a plain-English explanation for each alert (e.g. "Steps were 58% below your 4-week average").
Personal Dashboard — A clean, multi-page Streamlit interface where you upload your Apple Health export and immediately see all insights — no account creation, no subscription, your data stays on your machine.

Tech Stack
Data Processing: I used Python, Pandas and Numpy because they are the industry standard for tabular data manipulation; strong XML parsing support for Apple Health exports
Visualization: Plotly because I can produce high quality interactive charts
Machine Learning: Scikit-learn because it is simple to use and well-documented; LinearRegression and z-score logic were the right tools for this scope
dashboard framework: Streamlit because it allowed me to ship a working multi-page app significantly faster than a React frontend for V1
Hosting: Streamlit Communith CLoud because it is free, auto-deploys on every Github push, and there is no infrastructure to manage.

Product Decisions
Streamlit over a custom React frontend
I chose Streamlit for V1 because my goal was to validate the core features — scoring, forecasting, anomaly detection — before investing in a custom UI. Streamlit let me ship a working product in a fraction of the time. The tradeoff is limited UI customization and a less polished aesthetic compared to a React app. I've documented this as a known V2 improvement.

Apple Health export file over live API integration
I built around the exported XML file rather than integrating with the Apple Health or Strava APIs. The tradeoff is that users have to manually export and re-upload to refresh their data. I made this call because live API integration would have required OAuth setup, backend infrastructure, and handling refresh tokens — all complexity that adds no value until the core analytics are proven useful. The file-based approach also means no data ever leaves the user's machine, which is a meaningful privacy benefit.

Linear regression over more complex forecasting models
I chose LinearRegression over time-series models like ARIMA or Prophet because the input data (8 weeks of weekly aggregates) is too sparse for more complex models to generalize reliably. A simple trend line is both more interpretable and more honest about what the data can actually support. I display the R² value on the forecast chart so users can judge the model's confidence themselves.

How to Run locally
Prerequisites: Python 3.9+, Git
1. Clone the repo
git clone https://github.com/kwasi9911/personal-performance-os.git
cd personal-performance-os

2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Run the app
streamlit run app.py

The app will open at http://localhost:8501. Upload your Apple Health export.xml file (exported from the Health app on iPhone) to see your personal dashboard. A sample data file is included at data/sample_export.xml if you want to explore the app without your own data.

<img width="1919" height="923" alt="Screenshot 2026-05-25 at 11 25 13 pm" src="https://github.com/user-attachments/assets/bb99f828-79ef-4f66-b10c-56b429d55d9c" />
<img width="1919" height="923" alt="Screenshot 2026-05-25 at 11 24 46 pm" src="https://github.com/user-attachments/assets/93e263ae-9a24-4524-9963-376b0a11b06e" />
<img width="1919" height="923" alt="Screenshot 2026-05-25 at 11 24 06 pm" src="https://github.com/user-attachments/assets/77bdefa4-4d1c-42fc-b6ac-0ca5ca5ed7d8" />
<img width="1919" height="849" alt="Screenshot 2026-05-25 at 11 23 41 pm" src="https://github.com/user-attachments/assets/9095426b-04cc-481e-8e08-ab3ca6dfe22a" />
