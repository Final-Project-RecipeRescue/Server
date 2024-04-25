import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_dropdown(driver):
    try:
        container_xpath = '//*[@id="select2-ingredients-list0-container"]'
        # Find the ingredients container and click on it
        ingredients_container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, container_xpath))
        )
        ingredients_container.click()

        # Wait for the dropdown to appear
        id = "select2-ingredients-list0-results"
        dropdown_list = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, id))
        )

        # Return the dropdown element
        return dropdown_list

    except Exception as e:
        print("An error occurred while opening the dropdown:", e)
        return None


def get_categories_with_elements(dropdown: WebElement):
    try:
        categories_with_elements = {}

        # Find all the categories with the specified class
        categories = WebDriverWait(dropdown, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.select2-results__option--group'))
        )
        for category in categories:
            category_name = category.accessible_name
            options = WebDriverWait(category, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.select2-results__option--selectable'))
            )
            options = WebDriverWait(category, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.select2-results__option--selectable'))
            )
            elements = [option.text.strip() for option in options]
            categories_with_elements[category_name] = elements

        return categories_with_elements
    except Exception as e:
        print("An error occurred while printing categories:", e)


def perform_search(driver, ingredient):
    try:
        search_bar_xpath = '/html/body/span[2]/span/span[1]/input'
        search_bar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, search_bar_xpath))
        )
        search_bar.clear()
        search_bar.send_keys(ingredient)

        search_bar.send_keys(Keys.ENTER)

        ###TODO


        id = "select2-ingredients-list0-results"
        dropdown_list = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, id))
        )

        categories = WebDriverWait(dropdown_list, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'select2-results__option select2-results__option--group')))

        res = WebDriverWait(categories, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/span[2]/span/span[2]/ul/li/ul'))
        )
        res.click()
        time.sleep(2)

        gram_bar_xpath = '//*[@id="unit_quantity0"]'
        gram_bar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, gram_bar_xpath))
        )
        gram_bar.clear()
        gram_bar.send_keys('100')
        # Wait for search results to load (you can adjust the time as needed)
        time.sleep(2)
        calculate_xpath = '//*[@id="submit-button"]'
        calculate_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, calculate_xpath))
        )
        calculate_button.click()
        time.sleep(3)
        # Reopen the dropdown
        open_dropdown(driver)
        # Perform further actions with search results if needed

    except Exception as e:
        print(f"An error occurred while performing search for '{ingredient}':", e)


def get_all_ingredients():
    # Initialize Selenium WebDriver (assuming you're using Chrome)
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Open the website
    driver.get("https://myemissions.green/food-carbon-footprint-calculator/")

    try:
        # Open the dropdown and wait for it
        dropdown = open_dropdown(driver)
        print("dropdown opened")
        if dropdown:
            # Get categories with elements
            categories_with_elements = get_categories_with_elements(dropdown)
            if categories_with_elements:
                for category, elements in categories_with_elements.items():
                    for ingredient in elements:
                        perform_search(driver, ingredient)

            else:
                print("Failed to get categories with elements.")
        else:
            print("Dropdown failed to open.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the browser
        driver.quit()


# Example usage
get_all_ingredients()
