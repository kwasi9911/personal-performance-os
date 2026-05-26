import streamlit as st
from src.anomaly import detect_anomalies

st.title('🚨 Anomaly Alerts')

if 'weekly' not in st.session_state:
    st.warning('Please upload your data on the Overview page first.')
else:
    weekly = st.session_state['weekly']
    metric = st.selectbox('Metric to analyze', ['steps', 'exercise_min'])
    result = detect_anomalies(weekly, metric)
    anomalies = result[result['is_anomaly']]

    if anomalies.empty:
        st.success('No anomalies detected in your training data.')
    else:
        st.warning(f'{len(anomalies)} anomalous week(s) detected')
        for _, row in anomalies.iterrows():
            st.error(f"Week {row['week_str']}: {row['explanation']}")

    st.subheader('All Weeks')
    display = result[['week_str', metric, 'z_score', 'is_anomaly']].copy()
    display.columns = ['Week', metric.replace('_',' ').title(), 'Z-Score', 'Anomaly?']
    st.dataframe(display, use_container_width=True)
