import streamlit as st
import tempfile
import os
from src.agent import run_job_agent, format_results

st.set_page_config(
    page_title="AI Job Search Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Job Search Agent")
st.markdown("Upload your resume — get matched job postings instantly")

st.divider()

# inputs
col1, col2 = st.columns(2)

with col1:
    role = st.text_input(
        "Target role",
        placeholder="AI Engineer"
    )

with col2:
    location = st.text_input(
        "Location",
        placeholder="United States"
    )

k = st.slider("Number of results", 1, 10, 3)

resume_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

st.divider()

if st.button("🔍 Find matching jobs", use_container_width=True):
    
    # validate inputs
    if not resume_file:
        st.error("Please upload your resume")
        st.stop()
    
    if not role:
        st.error("Please enter a target role")
        st.stop()
    
    if not location:
        st.error("Please enter a location")
        st.stop()
    
    # save uploaded PDF to temp file
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:
        tmp.write(resume_file.read())
        tmp_path = tmp.name
    
    try:
        with st.spinner("Parsing resume..."):
            pass
        
        with st.spinner(f"Searching {role} jobs in {location}..."):
            pass
        
        with st.spinner("Matching jobs against your resume..."):
            results, profile = run_job_agent(
                resume_path=tmp_path,
                role=role,
                location=location,
                k=k
            )
        
        # show profile
        with st.expander("📄 Your extracted profile"):
            st.text(profile)
        
        st.divider()
        
        # show results
        if not results:
            st.warning("No jobs found — try a different role or location")
        else:
            st.success(f"Found {len(results)} matched jobs")
            st.markdown(format_results(results))
    
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")
    
    finally:
        # clean up temp file
        os.unlink(tmp_path)

st.divider()
st.caption("Built with LangChain · JSearch API · ChromaDB · Streamlit")