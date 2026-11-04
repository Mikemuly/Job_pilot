import requests
import streamlit as st

API = "http://127.0.0.1:8000"

st.title("JobPilot")

st.subheader("UPload CV")
cv = st.file_uploader("Choose a PDF", type=["pdf"])

if cv and st.button ("Extract profile"):
    files = {"file": (cv.name, cv.getvalue(), "application/pdf")}
    r = requests.post(f"{API}/upload_cv", files=files)
    if r.status_code == 200:
        st.session_state["profile"] = r.json()
        st.success("Profile created successfully")
    else:
        st.error("Upload failed. Please try again.")

    
profile_id = st.number_input("Profile ID", min_value=1, step=1)

if st.button("Load profile"):
    r = requests.get(f"{API}/profiles/{profile_id}")
    if r.status_code ==200:
        st.session_state["profile"] = r.json()
    else:
        st.error("Profile not found")

if "profile" in st.session_state:
    p = st.session_state["profile"]
    pid = p ["id"]

    full_name = st.text_input("Full Name", value=p["full_name"], key =f"name_{pid}")
    email = st.text_input("Email", value=p["email"], key = f"email_{pid}")
    skills = st.text_area("Skills", value=p["skills"], key = f"skills_{pid}")
    experience = st.text_area("Experience", value=p["experience"], key = f"exp_{pid}")
    education = st.text_area("Education", value=p["education"], key = f"edu_{pid}")

    if st.button ("Save Changes"):
        payload = {
            "full_name": full_name,
            "email": email,
            "skills": skills,
            "experience": experience,
            "education": education,
        }
        r= requests.patch(f"{API}/profiles/{pid}", json=payload)
        if r.status_code == 200:
            st.session_state["profile"] = r.json()
            st.success("Saved successfully")
        else:
            st.error("Could not save changes")
