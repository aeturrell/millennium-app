

import streamlit as st
st.title('Minimal example')
x = st.slider('x')
st.write(x, 'squared is', x * x)
