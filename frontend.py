import streamlit as st
from Alchemydb import Applicants, search_applicant, clear_applicant_table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine  


def personal_info():
    st.header("Personal Information")

    st.session_state.name = st.text_input("First Name", st.session_state.get("name", ""))
    st.session_state.last = st.text_input("Last Name", st.session_state.get("last", ""))
    st.session_state.dob = st.date_input("Date of Birth", st.session_state.get("dob", None))

    st.session_state.gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], 
                                           index=["Male", "Female", "Other", "Prefer not to say"].index(st.session_state.get("gender", "Male")))

    st.session_state.caste = st.selectbox("Caste", ["SC", "ST", "OBC", "Other"], 
                                          index=["SC", "ST", "OBC", "Other"].index(st.session_state.get("caste", "SC")))

    if st.session_state.caste == "Other":
        st.session_state.final_caste = st.text_input("Please state caste:", st.session_state.get("final_caste", ""))
    else:
        st.session_state.final_caste = st.session_state.caste


def contact_info():
    st.header("Contact Information")

    st.session_state.email = st.text_input("Email Address", st.session_state.get("email", ""))
    st.session_state.phone = st.text_input("Phone Number", st.session_state.get("phone", ""))
    st.session_state.address = st.text_area("Residential Address", st.session_state.get("address", ""))


def academic_info():
    st.header("Academic Information")

    st.session_state.university = st.text_input("College/University Name", st.session_state.get("university", ""))
    st.session_state.year_of_study = st.selectbox("Year of Study", ["Freshman", "Sophomore", "Junior", "Senior"], 
                                                  index=["Freshman", "Sophomore", "Junior", "Senior"].index(st.session_state.get("year_of_study", "Freshman")))
    st.session_state.gpa = st.number_input("Current GPA", min_value=0.0, max_value=4.0, step=0.1, value=st.session_state.get("gpa", 0.0))
    st.session_state.major = st.text_input("Major/Field of Study", st.session_state.get("major", ""))
    st.session_state.transcript = st.file_uploader("Upload Transcript (PDF)", type=["pdf"])


def activities():
    st.header("Extracurricular Activities")

    st.session_state.activities = st.text_area("List any extracurricular activities, leadership roles, or community involvement:", 
                                               st.session_state.get("activities", ""))


def financial_info():
    st.header("Financial Information")

    st.session_state.family_income = st.number_input("Annual Family Income (in USD)", min_value=0, step=1000, value=st.session_state.get("family_income", 0))
    st.session_state.scholarship_need = st.text_area("Why do you need this scholarship?", st.session_state.get("scholarship_need", ""))



def consent():
    st.header("Consent")

    st.session_state.consent = st.checkbox("I consent to the terms and conditions", value=st.session_state.get("consent", False))


    engine = create_engine("sqlite:///applications.db")
    session = sessionmaker(bind=engine)
    sess = session()

    if st.button("Submit Application", key="submit"):
        if st.session_state.consent:
            try:
                entry = Applicants(first_name = st.session_state.name , last_name = st.session_state.last, dob = st.session_state.dob,
                                gender = st.session_state.gender, caste = st.session_state.final_caste, email = st.session_state.email, 
                                phone = st.session_state.phone, address = st.session_state.address, university = st.session_state.university, 
                                gpa = st.session_state.gpa)
                sess.add(entry)
                sess.commit()
                st.success("Data added to database")
            except Exception as e:
                st.error(f"Some error occured: {e}")


            st.success("Your application has been successfully submitted!")
            st.write("### Application Details:")
            st.write(f"**Name:** {st.session_state.get('name', '')} {st.session_state.get('last', '')}")
            st.write(f"**DOB:** {st.session_state.get('dob', '')}")
            st.write(f"**Gender:** {st.session_state.get('gender', '')}")
            st.write(f"**Caste:** {st.session_state.get('final_caste', '')}")
            st.write(f"**Email:** {st.session_state.get('email', '')}")
            st.write(f"**Phone:** {st.session_state.get('phone', '')}")
            st.write(f"**Address:** {st.session_state.get('address', '')}")
            st.write(f"**University:** {st.session_state.get('university', '')}")
            st.write(f"**Year of Study:** {st.session_state.get('year_of_study', '')}")
            st.write(f"**GPA:** {st.session_state.get('gpa', '')}")
            st.write(f"**Major:** {st.session_state.get('major', '')}")
            st.write(f"**Activities:** {st.session_state.get('activities', '')}")
            st.write(f"**Family Income:** {st.session_state.get('family_income', '')}")
            st.write(f"**Need for Scholarship:** {st.session_state.get('scholarship_need', '')}")
            
            if st.session_state.get('transcript'):
                st.write(f"**Uploaded Transcript:** {st.session_state.transcript.name}")
        else:
            st.error("You must consent to the terms and conditions to submit.")


def search():

    st.title("Search Applicants")

    search_query= st.text_input("Enter Applicant FIRST Name: ")

    if st.button("Enter"):
        results = search_applicant(search_query)
        if results:
            for applicant in results:
                st.write(f"**Name:** {applicant.first_name} {applicant.last_name}")
                st.write(f"**DOB:** {applicant.dob}")
                st.write(f"**Gender:** {applicant.gender}")
                st.write(f"**Caste:** {applicant.caste}")
                st.write(f"**Email:** {applicant.email}")
                st.write(f"**Phone:** {applicant.phone}")
                st.write(f"**University:** {applicant.university}")
                st.write(f"**GPA:** {applicant.gpa}")
                st.write("---")
        else:
            st.write("No applicants found")


def admin():

    st.title("Admin page")

    if st.button("Clear applicant table"):
        clear_applicant_table()
        st.success("Table has been cleared")
        


def app():
    st.title("SHDF Scholarship in partnership with SES Chandigarh (Here after SHDF-SES).")

    st.write("Please fill out the form below to apply for the scholarship.")
    st.markdown("_Note: ONLY STUDENTS BELONGING TO NEEDY FAMILIES SHOULD APPLY._")

 

    tabs = st.tabs(["Personal Info", "Contact", "Academics", "Activities", "Financial Info", "Consent", "Search", "Admin"])


    with tabs[0]:  # Personal Info
        personal_info()
    with tabs[1]:  # Contact Info
        contact_info()
    with tabs[2]:  # Academic Info
        academic_info()
    with tabs[3]:  # Activities
        activities()
    with tabs[4]:  # Financial Info
        financial_info()
    with tabs[5]:  # Consent
        consent()
    with tabs[6]:
        search()
    with tabs[7]:
        admin()


if __name__ == "__main__":
    app()
