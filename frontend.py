import requests
import streamlit as st

API = "http://127.0.0.1:8000"

st.title("JobPilot")

st.subheader("Get Jobs")
search = st.text_input("Search term", value="python")
if st.button ("Fetch jobs"):
    r=requests.post(f"{API}/jobs/fetch",params={"search": search})
    if r.status_code == 200:
        st.success(f"Saved {r.json()['saved']} new jobs")
    else:
        st.error("Could not fetch jobs")

st.subheader("Upload CV")
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


    st.subheader("Top job matches")
    if st.button("Find matches"):
        r = requests.get(f"{API}/profile/{pid}/matches")
        if r.status_code == 200:
            st.session_state["matches"] = r.json()
        else:
            st.error("Could not load matches")

        
    for m in st.session_state.get("matches", []):
        st.markdown(f"**{m['title']}** at {m['company']}:{m['score']}%")
        st.caption(f"Matched: {', '.join(m['matched']) or 'none'}")
        st.link_button("View job", m["url"])

        exp_key = f"explanation_{m['job_id']}"
        if st.button("Explain", key=f"explain_{m['job_id']}"):
            r=requests.get(f"{API}/profiles/{pid}/explain/{m['job_id']}")
            if r.status_code == 200:
                st.session_state[exp_key] = (r.json()["explanation"])
            else:
                st.error("Could not Explain")
        if exp_key in st.session_state:
            st.info(st.session_state[exp_key])

        letter_key = f"letter_{m['job_id']}"
        if st.button("Write cover letter", key=f"btn_letter_{m['job_id']}"):
            with st.spinner("Writing..."):
                r = requests.post(f"{API}/profile/{pid}/cover-letter/{m['job_id']}")
            if r.status_code == 200:
                st.session_state[letter_key] = r.json()["cover_letter"]
            else:
                st.error("Could not write the letter")

        if letter_key in st.session_state:
            st.text_area("Cover letter (edit brfore using)", key=letter_key, height=300)
            
            if st.button("Approve and save", key=f"approve_{m['job_id']}"):
                letter = st.session_state.get(letter_key, "")
                r = requests.post(
                    f"{API}/applications",
                    params={
                        "profile_id": pid,
                        "job_id": m["job_id"],
                        "cover_letter": st.session_state[letter_key],
                    },
                )
                if r.status_code == 200:
                    st.success("Saved to your applications")
                elif r.status_code == 409:
                    st.warning("You already saved this job")
                else:
                    st.error("Could not save")
                
    st.subheader("My applications")
    if st.button("Refresh applications"):
        r = requests.get(f"{API}/profiles/{pid}/applications")
        if r.status_code ==200:
            st.session_state["applications"] = r.json()
            
    statuses = ["saved", "approved", "applied", "interview", "offer", "rejected"]
    for a in st.session_state.get("applications", []):
        st.markdown(f"**{a['job_title']}** at {a['company']}")
        st.link_button("View job", a["url"])
        new_status = st.selectbox(
            "Status",
            statuses,
            index=statuses.index(a["status"]),
            key=f"status_{a['id']}",
        )
        if new_status != (a["status"]):
            r=requests.patch(
                f"{API}/applications/{a['id']}",param= {"status": new_status}
            )
            if r.status_code == 200:
                a["status"] = new_status
                st.success("Status updated")