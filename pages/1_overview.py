import streamlit as st
import plotly.express as px
from src.parser import load_health_data, weekly_summary
from src.scoring import compute_training_load

st.title('📊 Overview')

uploaded = st.file_uploader('Upload your Apple Health export.xml', type=['xml'])

if uploaded:
    import tempfile, os
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as f:
        f.write(uploaded.read())
        tmp_path = f.name

    data = load_health_data(tmp_path)
    weekly = weekly_summary(data)
    scored = compute_training_load(weekly)
    st.session_state['data']   = data
    st.session_state['weekly'] = weekly
    st.session_state['scored'] = scored
    os.unlink(tmp_path)

    col1, col2, col3 = st.columns(3)
    col1.metric('Avg Weekly Steps',    f"{int(scored['steps'].mean()):,}")
    col2.metric('Avg Exercise (min)',   f"{int(scored['exercise_min'].mean())}")
    col3.metric('Current Load Score',  f"{scored['load_score'].iloc[-1]}/100")

    fig = px.line(scored, x='week_str', y='steps', title='Weekly Steps Over Time')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info('Upload your export.xml file above to see your dashboard.')
