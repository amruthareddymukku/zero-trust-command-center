import streamlit as st
from supabase_client import supabase

st.set_page_config(page_title="Zero Trust")

st.title("🔐 Zero Trust Command Center")

st.write("Supabase connection working!")

# Resources
response = supabase.table("RESOURCES").select("*").execute()

st.subheader("📦 Resources")
st.dataframe(response.data)

# Identities
identity_response = supabase.table("IDENTITIES").select("*").execute()

st.subheader("👤 Identities")
st.dataframe(identity_response.data)