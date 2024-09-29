import streamlit as st
import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

X_MASTER_KEY = os.environ["X_MASTER_KEY"]

# Function to get dynamic inputs for a section
def get_dynamic_input(section_title, fields):
    st.header(section_title)
    entries = []
    count = st.number_input(f"How many {section_title.lower()} entries do you want to add?", min_value=0, step=1)
    for i in range(int(count)):
        st.subheader(f"{section_title[:len(section_title)]} {i + 1}")
        entry = {}
        for field in fields:
            entry[field] = st.text_input(f"{field.capitalize()} for {section_title[:len(section_title)]} {i + 1}")
        entries.append(entry)
    return entries

# Streamlit UI to generate the JSON file
st.title("Resume JSON Generator")

# Basic Information
st.header("Basic Information")
name = st.text_input("Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
address = st.text_input("Address")
role = st.text_input("Role")

# Education Section
education_fields = ["type eg. university, high school", "name", "graduation_year", "course", "GPA"]
education = get_dynamic_input("Education", education_fields)

# Experience Section
experience_fields = ["title", "organization", "start and end date", "description"]
experience = get_dynamic_input("Experience", experience_fields)

# Projects Section
project_fields = ["title", "description"]
projects = get_dynamic_input("Projects", project_fields)

# Achievements Section
achievement_fields = ["title", "description"]
achievements = get_dynamic_input("Achievements", achievement_fields)

# Certificates Section
certificate_fields = ["title", "link"]
certificates = get_dynamic_input("Certificates", certificate_fields)

# Skills Section
st.header("Skills")
skills = st.text_area("Enter your skills separated by commas")



# Generate JSON button
if st.button("Generate JSON"):
    # Create a dictionary with all the data
    resume_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "role": role,
        "Education": education,
        "experience": experience,
        "projects": projects,
        "Achievements": achievements,
        "certificates": certificates,
        "skills": skills
    }

    # Convert to JSON and save
    json_data = json.dumps(resume_data, indent=4)
    file = str(datetime.now())
    url = 'https://api.jsonbin.io/v3/b'
    headers = {
    'Content-Type': 'application/json',
    'X-Master-Key': f'{X_MASTER_KEY}'
    }
    data = resume_data

    req = requests.post(url, json=data, headers=headers)
    print(req.text)
    #with open(f"resume/{file}.json", "w") as json_file:
    #    json_file.write(json_data)
    
    st.success("JSON file generated successfully!")
    st.json(json_data)
