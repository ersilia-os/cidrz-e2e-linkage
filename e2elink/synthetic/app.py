import streamlit as st

st.sidebar.title('Linkage variables')
st.sidebar.checkbox('Name', True)
st.sidebar.checkbox('Visit date', True)
st.sidebar.checkbox('Date of birth', True)
st.sidebar.checkbox('Year of birth', False)
st.sidebar.checkbox('Location', True)

st.sidebar.title('Statistics')
src_size = st.sidebar.slider(
    'Size of source file',
    100, 10000, 1000
)
trg_size = st.sidebar.slider(
    'Size of target file',
    100, 50000, 5000
)
exp_rate = st.sidebar.slider(
    'Expected linkage rate (%)',
    0, 100, 70
)

compute = st.sidebar.button('Compute!')

if not compute:
    st.title("ESTHER synthetic data generator")
else:
    st.title("Works")
