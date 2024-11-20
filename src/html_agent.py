from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_directory_html(website_url, faculty_card_class, page_type, navigation_card_class):
    url = website_url

    # Initialize Selenium WebDriver (assuming Chrome)
    driver = webdriver.Chrome()
    try:
        driver.get(url)
    except Exception as e:
        return "", "", "Error Loading Website, Please Check url and try again."

    # Wait for content to load (adjust time or use explicit waits)
    # Wait for faculty content to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, faculty_card_class)))
    except:
        return "", "", "No Faculty Cards Found, Please enter correct faculty class"
    # Get the page source and parse with BeautifulSoup
    html = driver.page_source

    driver.quit()

    try:
        soup = BeautifulSoup(html, 'html.parser')

        # Remove unwanted elements
        for tag in ['script', 'style', 'head', 'footer', 'iframe', 'header', 'meta', 'img', 'figure']:
            for element in soup.find_all(tag):
                element.decompose()

        # Extract body content
        body = soup.body if soup.body else soup

        faculty_cards = body.find_all(class_=faculty_card_class, limit=5)
        navigation_cards = []
        if len(faculty_cards) == 0:
            return "", "", "No Faculty Cards Found, Please enter correct faculty class"

        if page_type != "Single Page":
            navigation_cards = body.find_all(class_=navigation_card_class)
            if len(navigation_cards) == 0:
                return "", "", "No Navigation Cards , Please enter correct navigation class"

        return faculty_cards, navigation_cards, ""

    except Exception as e:
        return "", "", "Error parsing HTML, Please Check url and try again."


def get_profile_html(profile_url):
    url = profile_url

    # Initialize Selenium WebDriver (assuming Chrome)
    driver = webdriver.Chrome()
    try:
        driver.get(url)
    except Exception as e:
        return "", "", "Error Loading Website, Please Check url and try again."

    # Wait for content to load (adjust time or use explicit waits)

    WebDriverWait(driver, 5)

    # Get the page source and parse with BeautifulSoup
    html = driver.page_source

    driver.quit()

    try:
        soup = BeautifulSoup(html, 'html.parser')

        # Remove unwanted elements
        for tag in ['script', 'style', 'head', 'footer', 'iframe', 'header', 'meta', 'img', 'figure']:
            for element in soup.find_all(tag):
                element.decompose()

        # Extract body content
        profile_body = soup.body if soup.body else soup

        return profile_body, ""

    except Exception as e:
        return "", "Error parsing Profile HTML, Please Check url and try again."
