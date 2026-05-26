import streamlit as st
import plotly.graph_objects as go
from src.forecasting import forecast_goal

st.title('🎯 Goal Forecasting')

if 'weekly' not in st.session_state:
    st.warning('Please upload your data on the Overview page first.')
else:
    weekly = st.session_state['weekly']
    metric = st.selectbox('Choose a metric to forecast', ['steps', 'exercise_min'])
    current_val = weekly[metric].iloc[-1]
    target = st.number_input(
        f'Set your target {metric.replace("_", " ")}',
        min_value=float(current_val),
        value=float(current_val * 1.2)
    )

    result = forecast_goal(weekly, metric, target)

    if 'error' in result:
        st.error(result['error'])
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric('Current', f"{result['current']:,}")
        col2.metric('Target', f"{result['target']:,}")
        wk = result['weeks_to_go']
        col3.metric('Projected Weeks', str(wk) if wk else 'Target may not be reached in 26 weeks')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=result['history_x'], y=result['history_y'], mode='lines+markers', name='Actual', line=dict(color='#2563EB')))
        fig.add_trace(go.Scatter(x=result['future_x'], y=result['future_y'], mode='lines', name='Forecast', line=dict(color='#10B981', dash='dash')))
        fig.add_hline(y=target, line_color='#EF4444', line_dash='dot', annotation_text='Target')
        fig.update_layout(title=f'{metric.replace("_", " ").title()} Forecast')
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f'Model R² = {result["r2"]} | Weekly trend: {result["trend"]:+.1f} per week')
