import streamlit as st

# Sample resume data
DATA_FORMAT = {
    'name': 'John Doe',
    'title': 'Data Scientist',
    'linkedin': 'linkedin.com/in/johndoe',
    'github': 'github.com/johndoe',
    'email': 'johndoe@email.com',
    'address': '123 Main St, Anytown USA',
    'summary': 'Highly motivated and experienced data scientist with a passion for solving complex problems and finding insights in data. Skilled in using data to drive business decisions and improve processes.',
    'work_experience': [
        {
            'title': 'Data Scientist',
            'company': 'ABC Company',
            'dates': 'Jan 2018 - present',
            'description': 'Conducted data analysis and created predictive models to improve company sales and customer satisfaction.'
        },
        {
            'title': 'Data Analyst',
            'company': 'XYZ Company',
            'dates': 'Jan 2015 - Dec 2017',
            'description': 'Collected and analyzed data to support decision-making and improve company operations.'
        },
    ],
    'education': [
        {
            'degree': 'Master of Science in Data Science',
            'school': 'University of Technology',
            'dates': 'Jan 2013 - Dec 2014',
            'description': 'Focus on machine learning and data visualization techniques.'
        },
        {
            'degree': 'Bachelor of Science in Computer Science',
            'school': 'University of Science',
            'dates': 'Jan 2009 - Dec 2012',
            'description': 'Focus on software development and algorithms.'
        },
    ],
    'skills': [
        'Data analysis',
        'Predictive modeling',
        'Machine learning',
        'Data visualization',
        'Software development'
    ]
}
# Set the CSS style for the app
def set_style():
    st.markdown(
        """
        <style>
        .main-header {{
            text-align: center;
            font-size: 3em;
            margin-bottom: 10px;
        }}
        .sub-header {{
            text-align: center;
            font-size: 1.5em;
            margin-bottom: 30px;
        }}
        .input-field {{
            width: 100%;
            padding: 10px;
            font-size: 1.5em;
            border-radius: 5px;
            border: 1px solid lightgrey;
            margin-bottom: 20px;
        }}
        </style>
        """
    )

# Use the set_style function to add CSS to the app

# Add header and input fields to the app

def section(section_name,section_data):
    st.write(section_name.replace('_', ' ').title())
    item_keys = list(section_data[0].keys())
    item_keys.remove('description')
    for section_item in section_data:
        for col_idx
        for key, value in section_item.items():
            st.text_input(key, value)




if __name__ == '__main__':
    section('work_experience',DATA_FORMAT['work_experience'])