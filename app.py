import os
import subprocess
import sys
import gradio as gr
from src.html_agent import get_directory_html, get_profile_html
from src.llm import *



def scrape(college_name, university_name, website_url, faculty_card_class, page_type, navigation_card_class, profile_flag, profile_url, retry_count=0):
    return_str = ""
    MAX_RETRIES = 2

    if university_name == "":
        return_str = "Please enter your university name"
        return return_str
    if college_name == "":
        return_str = "Please enter your college name"
        return return_str

    # Check if website_url, faculty_card_class is provided
    if (website_url) and (faculty_card_class):
        pass
    else:

        if website_url == "":
            return_str = "Please enter your website URL"
            if faculty_card_class == "":
                return_str = return_str + " and " + "Please enter your faculty card class."
        else:
            return_str = "Please enter your faculty card class."
        return return_str

    # Check if navigation_class_card is provided if page_type is not single
    if page_type != "Single Page":
        if navigation_card_class == "":
            return_str = "Please enter your navigation card class."
            return return_str

    # Check if profile_url is provided if profile_flag is yes
    if profile_flag == "Yes":
        if profile_url == "":
            return_str = "Please enter your profile url to faculty that has all the fields."
            return return_str

    faculty_card, navigation_card, return_str = get_directory_html(website_url, faculty_card_class, page_type,
                                                         navigation_card_class)

    # Check any error occurred during getting html content
    if return_str != "":
        return return_str

    if page_type == "Single Page":
        generated_code = llm_single_page(body = faculty_card, url = website_url, college=college_name, university=university_name)
    elif page_type == "Pagination":
        generated_code = llm_pagination(body = faculty_card, url = website_url, college=college_name, university=university_name, navigation=navigation_card)
    elif page_type == "Load More":
        generated_code = llm_load_more(body=faculty_card, url=website_url, college=college_name, university=university_name,
                       navigation=navigation_card)



    if profile_flag == "Yes":

        profile_html, return_str = get_profile_html(profile_url)

        if return_str != "":
            return return_str

        generated_code = continution_llm(body=profile_html, url=profile_url, prev_output=generated_code)

    generated_code = generated_code.replace('```python', '').replace('```', '')

    # Step 1: Save the code to a file
    file_path = os.path.join("generated_codes",
                             f"{college_name.replace(' ', '_')}_{university_name.replace(' ', '_')}.py")
    with open(file_path, "w") as file:
        file.write(generated_code)

    # Step 2: Using subprocess.run()
    return_code = subprocess.run([sys.executable, file_path]).returncode

    if return_code == 0:
        return_str = "Code has run successfully."
    else:
        if retry_count < MAX_RETRIES:
            print(f"Retrying... Attempt {retry_count + 1}")
            return_str = scrape(college_name, university_name, website_url, faculty_card_class, page_type,
                               navigation_card_class, profile_flag, profile_url, retry_count + 1)
        else:
            return_str = "Something went wrong while running the code. Maximum retry attempts exceeded."


    return return_str


# Create the Gradio app
with gr.Blocks() as demo:
    # Create the input components
    college_name = gr.Textbox(label="College Name")
    university_name = gr.Textbox(label="University Name")
    website_url = gr.Textbox(label="Website URL")
    faculty_card_class = gr.Textbox(label="Faculty Card Class")
    page_type = gr.Dropdown(choices=["Single Page", "Pagination", "Load More"], label="Page Type")
    navigation_card_class = gr.Textbox(label="Navigation Card Class")
    profile_page_flag = gr.Dropdown(choices=["No", "Yes"], label="Do we need to enter into each profile to get any details?")
    profile_url = gr.Textbox(label="If yes, Please provide a link to one profile that contains all the required fields")

    examples = gr.Examples(
        examples=[
            ['UCB', "UC Berkeley", 'https://vcresearch.berkeley.edu/faculty-expertise','views-field', 'Load More', 'pager__item', 'Yes', 'https://vcresearch.berkeley.edu/faculty/elizabeth-abel'],
            ['Curry College', "Curry College", 'https://www.curry.edu/directory', 'faculty-tile', 'Single Page',
             '', 'No', ''],
            ['College of Engineering', "Northeastern University", 'https://coe.northeastern.edu/faculty-staff-directory/', 'block-small', 'Pagination','page-numbers', 'No', ''],
            ['College of Veterinary Medicine', 'Purdue University', 'https://vet.purdue.edu/directory/index.php?classification=all', 'profile-entry', 'Single Page', '', 'Yes', 'https://vet.purdue.edu/directory/person.php?id=147']
        ],
        inputs=[college_name, university_name, website_url,faculty_card_class ,page_type, navigation_card_class, profile_page_flag, profile_url,],
    )

    # Create the output component
    output = gr.Textbox(label="Output Box")

    # Create the button and attach the event listener
    greet_btn = gr.Button("GO!")
    greet_btn.click(fn=scrape, inputs=[college_name, university_name, website_url, faculty_card_class, page_type,
                                      navigation_card_class, profile_page_flag, profile_url], outputs=output, api_name="greet")

# Launch the app
if __name__ == "__main__":
    demo.launch()

