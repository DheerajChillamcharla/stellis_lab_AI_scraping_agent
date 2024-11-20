from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini")

def llm_single_page(body, url, college, university):
    prompt = PromptTemplate.from_template(
        """You are a python programming expert deployed to write a python code for the given task.

            Task: You are provided with HTML regarding a Five faculty at a university from the faculty directory web page
            Please provide the python code to extract the details of all the faculty on the web page.

            HTML :{input}
            URL : {url}
            College : {college}
            University : {university}

            Please extract the following details of the faculty: email, name, title, department, college, university, description, profile_url, phone_number

            Structure the python code like the following

            #Import Necessary Modules
            <Insert Code>

            # Initialize Selenium WebDriver (assuming Chrome)
            driver = webdriver.Chrome()
            driver.get(URL)

            # Wait for faculty content to load
            <Insert Code>

            # Get the page source and parse with BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Get list of All faculty
            <Insert COde>

            # Loop Through the list
            <Insert COde>

            # Get the details of the faculty
            <Insert Code>
            Follow below instructions while getting the details of the faculty
            Examples for each field is given below

                "email": "jdoe@example.com",
                "name": "John Doe",
                "title": "Assistant Professor",
                "department": "Computer Science",
                "college": "College of Engineering",
                "university": "University of Example",
                "description": "An experienced researcher specializing in artificial intelligence and machine learning.",
                "profile_url": "https://www.exampleuniversity.edu/faculty/jdoe",
                "phone_number": "+1-555-123-4567"

            1. Append any all information about the professor to description.
            2. If a field is missing on that website, leave the respective column blank.
            3. Delete the rows where email addresses are not found.

            # Create a CSV file and store each field in a column
            <Insert COde>

            If unable to find the data in the HTML, acknowledge and politely decline to provide code

            Only return the python code that can run without need for any edits and nothing more """
    )

    chain = prompt | llm
    result = chain.invoke(
        {
            "input": body,
            "url": url,
            "college": college,
            "university": university,
        }
    )
    return result.content


def llm_pagination(body, url, college, university, navigation):


    prompt = PromptTemplate.from_template(
        """You are a python programming expert deployed to write a python code for the given task.

            Task: You are provided with Faculty HTML regarding a Five faculty at a university from the faculty 
            directory web page.Please provide the python code to extract the details of all the faculty on the all 
            the web pages by moving next page available. HTML to the navigation is provided.

            Faculty HTML :{input}
            URL : {url}
            College : {college}
            University : {university}
            Navigation HTML :{navigation}

            Please extract the following details of the faculty: email, name, title, department, college, university, description, profile_url, phone_number

            Structure the python code like the following

            #Import Necessary Modules
            <Insert Code>

            # Initialize Selenium WebDriver (assuming Chrome)
            driver = webdriver.Chrome()
            driver.get(URL)

            # Wait for faculty content to load
            <Insert Code>

            # Get the page source and parse with BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Get list of All faculty
            <Insert COde>

            # Loop Through the list
            <Insert COde>

            # Get the details of the faculty
            <Insert Code>
            Follow below instructions while getting the details of the faculty
                1. Get email of the faculty if not available leave empty
                2. Get name of the faculty if not available leave empty
                3. Get title of the faculty if not available leave empty, title is the position of faculty at the university
                4. Get department of the faculty if not available try deducting from patterns in the title
                5. If unable to deduct from title leave empty
                6. Get college of the faculty if not available leave empty
                7. Get university of the faculty if not available leave empty
                8. Get description of the faculty if not available leave empty,
                description can contain any additional information available about the faculty that is not covered in other fields
                9. Get profile url of the faculty if not available leave empty
                10. Get phone number of the faculty if not available leave empty
                11. Make sure each field contain only the data it has to contain

            # Find if next page is available
            <Insert Code>

            # If yes move to next page and repeat above steps to get the faculty details
            <Insert Code>

            # Create a CSV file and store each field in a column
            <Insert Code>

            If unable to find the data in the HTML, acknowledge and politely decline to provide code

            Only return the python code and nothing more """
    )

    chain = prompt | llm
    result = chain.invoke(
        {
            "input": body,
            "url": url,
            "college": college,
            "university": university,
            "navigation": navigation,
        }
    )
    return result.content


def llm_load_more(body, url, college, university, navigation):

    prompt = PromptTemplate.from_template(
        """You are a python programming expert deployed to write a python code for the given task.

            Task: You are provided with Faculty HTML regarding a Five faculty at a university from the faculty 
            directory web page.Please provide the python code to extract the details of all the faculty on the 
            the web pages by loading more until available. HTML to the load more button is provided.

            Faculty HTML :{input}
            URL : {url}
            College : {college}
            University : {university}
            Load more HTML :{navigation}

            Please extract the following details of the faculty: email, name, title, department, college, university, description, profile_url, phone_number

            Structure the python code like the following

            #Import Necessary Modules
            <Insert Code>

            # Initialize Selenium WebDriver (assuming Chrome)
            driver = webdriver.Chrome()
            driver.get(URL)

            # Wait for faculty content to load
            <Insert Code>

            # Click on load more button and wait for 2 seconds and then wait until load more button is loaded
            <Insert Code>

            # Do it until you reach end of the page
            <Insert Code>

            # Get the page source and parse with BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Get list of All faculty
            <Insert COde>

            # Loop Through the list
            <Insert COde>

            # Get the details of the faculty
            <Insert Code>
            Follow below instructions while getting the details of the faculty
                1. Get email of the faculty if not available leave empty
                2. Get name of the faculty if not available leave empty
                3. Get title of the faculty if not available leave empty, title is the position of faculty at the university
                4. Get department of the faculty if not available try deducting from patterns in the title
                5. If unable to deduct from title leave empty
                6. Get college of the faculty if not available leave empty
                7. Get university of the faculty if not available leave empty
                8. Get description of the faculty if not available leave empty,
                description can contain any additional information available about the faculty that is not covered in other fields
                9. Get profile url of the faculty if not available leave empty
                10. Get phone number of the faculty if not available leave empty
                11. Make sure each field contain only the data it has to contain


            # Create a CSV file and store each field in a column
            <Insert Code>

            If unable to find the data in the HTML, acknowledge and politely decline to provide code

            Only return the python code and nothing more """
    )

    chain = prompt | llm
    result = chain.invoke(
        {
            "input": body,
            "url": url,
            "college": college,
            "university": university,
            "navigation": navigation,
        }
    )
    return result.content


def continution_llm(body, url, prev_output):


    prompt = PromptTemplate.from_template(
        """You are a python programming expert deployed to write a python code for the given task.

            Task: You are provided with HTML of a faculty page at a university.Also you have provided with code that 
            opens directory page of the university and scrapes information about all the faculty on the page. Now 
            that you have html of individual faculty page, Please provide the continuation python code to extract the 
            details of the faculty on the the personal web page. The python code should be able to open 20 faculty 
            profile links from the faculty data at a time and store data for the faculty in the related column.

            Faculty HTML :{input}
            URL : {url}
            Previous Output : {prev_output}

            Please extract the following details of the faculty: email, title, department, college, university, description, phone_number

            Structure the python code like the following

            #Import Necessary Modules
            <Insert Code>

            # Previous code
            <Insert Code>

            # Loop in a batch of 20 links
            <Insert Code>

            # Open simultaneous tabs
            <Insert Code>

            # Go to next window and wait for faculty name to load, do not explicitly wait for fixed time
            <Insert Code>

            # Get the details of the faculty in the particular tab
            <Insert Code>
            Follow below instructions while getting the details of the faculty
                1. Get email of the faculty if not available leave empty
                2. Get name of the faculty if not available leave empty
                3. Get title of the faculty if not available leave empty, title is the position of faculty at the university
                4. Get department of the faculty if not available leave empty
                5. Get college of the faculty if not available leave empty
                6. Get university of the faculty if not available leave empty
                7. Get description of the faculty if not available leave empty,
                8. Description can contain any additional information available about the faculty that is not covered in other fields
                9. Get profile url of the faculty if not available leave empty
                10. Get phone number of the faculty if not available leave empty
                11. Make sure each field contain only the data it has to contain

            # Find the row in data using faculty profile link and store the related data in the related column
            <Insert Code>

            # Close the tab and move to the main tab
            <Insert Code>

            # Save data into a CSV file after each loop and store each field in a column
            <Insert Code>

            # Print the time it took to run the code
            <Insert Code>

            Only return the python code and nothing more """
    )

    chain = prompt | llm
    result = chain.invoke(
        {
            "input": body,
            "url": url,
            "prev_output": prev_output,
        }
    )
    return result.content