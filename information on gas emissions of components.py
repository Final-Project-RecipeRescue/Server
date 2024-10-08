import json
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_dropdown(driver):
    try:
        container_xpath = '//*[@id="select2-ingredients-list0-container"]'
        # Find the ingredients container and click on it
        ingredients_container = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, container_xpath))
        )
        ingredients_container.click()
        time.sleep(1)
        # Return the dropdown element
        return ingredients_container

    except Exception as e:
        print("An error occurred while opening the dropdown:", e)
        return None


def get_categories_with_elements(driver):
    try:
        categories_with_elements = {}
        # Wait for the dropdown to appear
        id = "select2-ingredients-list0-results"
        dropdown_list = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, id))
        )
        # Find all the categories with the specified class
        categories = WebDriverWait(dropdown_list, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.select2-results__option--group'))
        )
        for category in categories:
            category_name = category.accessible_name

            options = WebDriverWait(category, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.select2-results__option--selectable'))
            )
            elements = [option.text.strip() for option in options]
            categories_with_elements[category_name] = elements

        return categories_with_elements
    except Exception as e:
        print("An error occurred while get categories:", e)


def search_ingredient(driver, ingredient):
    try:
        search_bar_xpath = '/html/body/span[2]/span/span[1]/input'
        search_bar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, search_bar_xpath))
        )
        search_bar.clear()
        time.sleep(1)
        search_bar.send_keys(ingredient)

        search_bar.send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred while search_ingredient {ingredient}")


def enterGram(driver):
    try:
        gram_bar_xpath = '//*[@id="unit_quantity0"]'
        gram_bar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, gram_bar_xpath))
        )
        gram_bar.clear()
        time.sleep(1)
        gram_bar.send_keys('100')
        gram_bar.click()
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred while entering gram")


def calc(driver):
    try:
        calculate_xpath = '//*[@id="submit-button"]'
        calculate_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, calculate_xpath))
        )
        calculate_button.click()
    except Exception as e:
        print(f"An error occurred while entering calculation")


def get_gCo2e(driver):
    try:
        xpath_co2_per_serving = '//*[@id="total_emissions"]'
        gCO2e_per_serving = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_co2_per_serving))
        )
        return gCO2e_per_serving
    except Exception as e:
        print(f"An error occurred while getting gCO2e")


def get_description(driver):
    try:
        web_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div[4]/main/div/section[2]/div/div/div/div/div/div[1]/div/div[4]/div[1]/div/div[2]/div/div[2]/div[2]'))
        )
        description_co2_per_serving = WebDriverWait(web_element, 10).until(
            EC.element_to_be_clickable((By.ID, 'emissions_category_desc'))
        )
        return description_co2_per_serving
    except Exception as e:
        print(f"An error occurred while getting description")


def get_amount_grams_per_serving(driver):
    try:
        xpath_amount_grams_per_serving = '/html/body/div[4]/main/div/section[2]/div/div/div/div/div/div[1]/div/div[1]/div/form/div[2]/div[3]/div[2]'
        amount_grams_per_serving = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_amount_grams_per_serving))
        )
        return amount_grams_per_serving
    except Exception as e:
        print(f"An error occurred while getting amount")


def perform_search(driver, ingredient):
    try:
        search_ingredient(driver, ingredient)
        time.sleep(2)
        enterGram(driver)
        time.sleep(2)
        amount_per_serving = get_amount_grams_per_serving(driver).text
        time.sleep(2)
        calc(driver)
        time.sleep(5)
        gCO2e = get_gCo2e(driver).text
        time.sleep(2)
        description = get_description(driver).text
        return {
            "name": ingredient,
            "amount_per_serving": amount_per_serving,
            "gCO2e_per_100g": gCO2e,
            "description": description
        }

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
            categories_with_elements = get_categories_with_elements(driver)
            if categories_with_elements:
                all_ingredients = {}
                for category, elements in categories_with_elements.items():
                    category_dict = {}
                    for ingredient in elements:
                        print(f"search for {ingredient}...")
                        ingredient_data = perform_search(driver, ingredient)
                        if ingredient_data:
                            print(f"successfully search for {ingredient} ")
                            category_dict[ingredient] = ingredient_data
                        else:
                            print(f"no {ingredient}")
                            category_dict[ingredient] = {
                                "name": ingredient,
                                "amount_per_serving": '0',
                                "gCO2e_per_100g": '0',
                                "description": ""
                            }
                        open_dropdown(driver)
                        time.sleep(2)
                    all_ingredients[category] = category_dict

                return all_ingredients

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
ingredients_data = get_all_ingredients()
# Save the data to a JSON file
if ingredients_data:
    with open("ingredients_data.json", "w") as json_file:
        json.dump(ingredients_data, json_file, indent=4)
