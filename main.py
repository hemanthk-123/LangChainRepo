import streamlit as st
import PyPDF2
import re

# Function to extract text from a PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

# Function to extract skills from text (reference resumes and user resumes)
def extract_skills_from_text(text):
    # A simple way to extract skills based on words in the resume.
    # This can be more advanced by integrating NER (Named Entity Recognition) or using predefined skill lists.
    skills = re.findall(r'\b[A-Za-z]+\b', text.lower())  # Extract words
    skills = set(skills)  # Remove duplicates
    return skills

# Function to evaluate user's resume based on job description
def evaluate_resume(candidate_text, job_description_text):
    # Extract skills dynamically from job description
    job_description_skills = extract_skills_from_text(job_description_text)

    # Extract skills from candidate's resume
    candidate_skills = extract_skills_from_text(candidate_text)

    # Calculate matching skills
    matching_skills = job_description_skills.intersection(candidate_skills)
    missing_skills = job_description_skills.difference(candidate_skills)

    # Calculate improvement skills (skills present in the JD but not in candidate's resume)
    improvement_skills = job_description_skills.difference(matching_skills)

    # Calculate matching percentage (based on skills)
    matching_percentage = (len(matching_skills) / len(job_description_skills)) * 100 if len(job_description_skills) > 0 else 0

    result = {
        "matching_skills": list(matching_skills),
        "missing_skills": list(missing_skills),
        "improvement_skills": list(improvement_skills),
        "matching_percentage": round(matching_percentage, 2)
    }

    return result

# Streamlit UI
st.title("📄 Resume Screening with Job Description Matching")
st.write("Upload a candidate's resume and provide a job description to check the matching percentage based on skills.")

# Upload job description
st.subheader("Upload Job Description")
job_description_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

# Upload candidate resume
st.subheader("Upload Candidate Resume")
uploaded_file = st.file_uploader("Upload Candidate Resume (PDF)", type=["pdf"])

if uploaded_file and job_description_file:
    st.write("🔍 **Processing resume and job description...**")

    # Extract text from candidate resume
    candidate_text = extract_text_from_pdf(uploaded_file)

    # Extract text from job description
    job_description_text = extract_text_from_pdf(job_description_file)

    # Evaluate resume based on job description
    evaluation = evaluate_resume(candidate_text, job_description_text)

    # Display results
    st.subheader("📌 Evaluation Result:")
    st.write(f"**🔢 Matching Percentage:** {evaluation['matching_percentage']}%")
    # st.write(f"**✅ Matching Skills:** {', '.join(evaluation['matching_skills']) or 'None'}")
    # st.write(f"**❌ Missing Skills:** {', '.join(evaluation['missing_skills']) or 'None'}")
    st.write(f"**💡 Improvement Skills (Required but Missing):** {', '.join(evaluation['improvement_skills']) or 'None'}")


    if evaluation["matching_percentage"] > 70:
        st.success("✅ Resume is a strong match for the job description!")
    elif evaluation["matching_percentage"] > 40:
        st.warning("⚠️ Resume is a partial match for the job description.")
    else:
        st.error("❌ Resume does not match well with the job description.")
else:
    st.write("Please upload both the job description and candidate resume.")
