import json
from ast import literal_eval

import streamlit as st

section_examples = {'summary': 'I have passion for new tech',
                    'workExperience': 'Tell about my ability to lead projects',
                    'education': 'Describe my degree type in more detail', 'skills': 'Add soft skills'}


def list_section(section_name, section_data):
    description_key = 'description'

    item_keys = list(section_data[0].keys())
    item_keys.remove(description_key)
    for item_id, section_item in enumerate(section_data):
        cols = st.columns(len(item_keys))
        for col, key in zip(cols, item_keys):
            col.text_input(key, section_item[key], key=f'{section_name}_{item_id}_{key}')
        st.text_area(description_key, section_item[description_key], key=f'{section_name}_{item_id}_{description_key}')

        recruiter_subsection(section_name, section_example=section_examples[section_name], item_id=item_id)
        st.markdown('***')


def skills_section(section_name, skills_data):
    num_columns = 3
    for skills_row in range(0, len(skills_data), num_columns):
        cols = st.columns([3, 1] * num_columns)
        skills_row_names = skills_data[skills_row: skills_row + num_columns]
        for item_id, skill in enumerate(skills_row_names):
            skill_id = skills_row + item_id
            cols[item_id * 2].text_input(' ', value=skill, key=f'{section_name}_{skill_id}', label_visibility='hidden')
            cols[item_id * 2 + 1].markdown('## ')
            if cols[item_id * 2 + 1].button('x', key=f'{section_name}_{skill_id}_remove_skill'):
                _remove_skill(skill_id, skills_data)

    skill_subsection(section_name)
    recruiter_subsection(section_name, section_example=section_examples[section_name])
    st.markdown('***')


def _remove_skill(skill_id, skills_data):
    del skills_data[skill_id]
    st.experimental_rerun()


def skill_subsection(section_name, item_id=0):
    key = f'{section_name}_{item_id}_add_skill'
    cols = st.columns([12, 1])
    new_skill = cols[0].text_input("Add skill", key=key)
    cols[1].markdown('##')
    clicked = cols[1].button("\+")
    if clicked and new_skill:
        st.write(new_skill)
        st.session_state['resume_data'][section_name].append(new_skill)
        st.write(st.session_state['resume_data'][section_name])
        st.experimental_rerun()


def recruiter_subsection(section_name, section_example, item_id=0):
    with st.container():
        cols = st.columns([3, 10], gap='small')
        cols[0].write('\n')
        cols[0].write('\n')
        cols[0].button("Auto Section Improve", key=f'{section_name}_{item_id}_improve_auto')
        cols[1].text_input("section_example",
                           value=f"Send a special request to the bot here... e.g. {section_example}.",
                           key=f'{section_name}_{item_id}_improve_manual', label_visibility='hidden')


def summary_section(section_name, summary_data):
    st.text_area(section_name, summary_data, key=f'{section_name}', label_visibility='hidden')
    recruiter_subsection(section_name, section_examples[section_name])


def contact_info_section(section_name, info_data):
    for key, value in info_data.items():
        if value:
            st.text_input(key.title(), value, key=f'{section_name}_{key}')
    st.markdown('***')


def header():
    st.text_input('name', st.session_state.resume_data['name'], key="name")
    st.text_input('title', st.session_state.resume_data['title'], key="title")


def body():
    section_dict = {'contactInfo': contact_info_section, 'summary': summary_section, 'workExperience': list_section,
                    'education': list_section, 'skills': skills_section}
    tabs_names = [key.replace('_', ' ').title() for key in section_dict.keys()]
    tabs = st.tabs(tabs_names)
    for tab, key in zip(tabs, section_dict):
        section_func = section_dict[key]
        with tab:
            section_func(key, st.session_state['resume_data'][key])


def sidebar():
    with st.sidebar:
        uploaded_file = st.file_uploader('Upload PDF Resume', type="json")
        if uploaded_file and _is_new_file(uploaded_file):
            _init_resume(uploaded_file)

        if is_data_available():
            st.button("Auto Improve All")
            st.button("Give Feedback")
            st.download_button('Download PDF', file_name='output.json', mime="application/json",
                               data=json.dumps(format_resume_data()))


def _is_new_file(uploaded_file):
    return uploaded_file.id != st.session_state.get('file_id', '')


def _init_resume(uploaded_file):
    resume_data = literal_eval(uploaded_file.read().decode('utf8'))
    st.session_state['resume_data'] = resume_data
    st.session_state['file_id'] = uploaded_file.id


def format_resume_data():
    current_state = st.session_state
    resume_data = {}
    contact_info = {}
    work_experience = []
    education = []
    skills = []

    resume_data['name'] = current_state.get('name', '')
    resume_data['title'] = current_state.get('title', '')

    contact_info_keys = ['linkedin', 'github', 'email', 'address']
    for key in contact_info_keys:
        contact_info[key] = current_state.get(f'contactInfo_{key}', '')
    resume_data['contactInfo'] = contact_info

    resume_data['summary'] = current_state.get('summary', '')

    work_experience_keys = ['workExperience_{}_title', 'workExperience_{}_company', 'workExperience_{}_dates',
                            'workExperience_{}_description']
    education_keys = ['education_{}_degree', 'education_{}_school', 'education_{}_dates', 'education_{}_description']

    total_work_experience = count_entries(st.session_state, 'workExperience')
    total_education = count_entries(st.session_state, 'education')

    for i in range(total_work_experience):
        work_experience.append(
            {key.split('_')[2]: current_state.get(key.format(i), '') for key in work_experience_keys})

    for i in range(total_education):
        education.append({key.split('_')[2]: current_state.get(key.format(i), '') for key in education_keys})

    resume_data['workExperience'] = work_experience
    resume_data['education'] = education

    total_skills = count_entries(st.session_state, 'skills')

    for i in range(total_skills):
        skill_key = f'skills_{i}'

        skills.append(current_state.get(skill_key, ''))
    resume_data['skills'] = skills

    return resume_data


def count_entries(input_dict, entry_type):
    max_index = max([int(key.split("_")[1]) for key in input_dict.keys() if key.startswith(f"{entry_type}_")],
                    default=0)
    return max_index + 1


def title():
    st.title("SolidCV - AI Resume Improver")


def upload_resume_header():
    st.success("Upload PDF Resume ")


def is_data_available():
    return st.session_state.get('resume_data')


def _main():
    title()
    sidebar()

    if is_data_available():
        header()
        body()

    else:
        upload_resume_header()


if __name__ == '__main__':
    _main()

    # bootstrap 4 collapse example
