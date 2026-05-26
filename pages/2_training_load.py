import streamlit as st
import plotly.graph_objects as go

st.title('💪 Training Load & Recovery')

if 'scored' not in st.session_state:
    st.warning('Please upload your data on the Overview page first.')
else:
    scored = st.session_state['scored']
    latest = scored.iloc[-1]

    col1, col2 = st.columns(2)
    col1.metric('This Week Load Score', f"{latest['load_score']}/100")
    col2.metric('Recovery Zone', latest['zone'])

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=scored['week_str'], y=scored['load_score'],
        marker_color=scored['zone_color'], name='Load Score'
    ))
    fig.update_layout(title='Weekly Training Load Score', xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader('Zone Legend')
    st.markdown('- 🟡 **Undertraining** (0–30): Increase activity')
    st.markdown('- 🟢 **Optimal** (30–70): Great balance')
    st.markdown('- 🔴 **Overtraining** (70–100): Consider rest days')
