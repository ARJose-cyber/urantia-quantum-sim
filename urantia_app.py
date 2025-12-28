import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from urantia_engine import run_urantia_simulation

st.set_page_config(page_title="Urantia Quantum Lab", page_icon="⚛️")

st.title("⚛️ Urantia Electronic Simulator")
st.markdown("""
Exploring **Paper 42: Energy—Mind and Matter**. 
This lab simulates the transition of Ultimatons into the 'Electronic Stage' of matter.
""")

# --- Sidebar: Urantia Parameters ---
st.sidebar.header("Cosmological Constants")
ultimaton_count = st.sidebar.number_input("Ultimatons per Electron", value=100)
slow_down = st.sidebar.slider("Slowing Down Factor (Activity)", 0.1, 1.0, 1.0, 
                               help="Transition from pure energy to organized matter")

bond_dist = st.sidebar.slider("Atomic Revolution Radius (Å)", 0.3, 2.5, 0.735)

# --- Analysis Logic ---
if st.button("Calculate Atomic Stability"):
    with st.spinner("Analyzing Electronic Stage..."):
        # Run Simulation
        energy = run_urantia_simulation(bond_dist, slow_down)
        
        # Calculate Urantia Mass Ratios
        # "1/2000th of hydrogen atom" & "1/10th of an ounce if Earth-sized"
        u_mass = (1/2000) * slow_down
        
        # UI Display
        st.subheader("Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Ground State Energy", f"{energy:.4f} Ha")
        col2.metric("Ultimaton Density", f"{ultimaton_count}%")
        col3.metric("Relative Mass", f"{u_mass:.6f}")

        # Unpredictability Visualization
        st.write("### Individual Electron Unpredictability")
        st.caption("While large groups follow laws, individual units show 'unpredictability'.")
        
        # Generate some 'unpredictable' noise based on quantum fluctuations
        noise_data = pd.DataFrame({
            'Measurement': range(50),
            'Energy Variation': [energy + (np.random.normal(0, 0.05)) for _ in range(50)]
        })
        fig = px.line(noise_data, x='Measurement', y='Energy Variation', 
                      title="Single Unit Fluctuation vs. Statistical Law")
        st.plotly_chart(fig)

st.divider()
st.info("📜 Paper 42, Section 4: 'Electrons are formed when ultimatons aggregate and slow down...'")
