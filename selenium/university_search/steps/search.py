
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# Given
@given("I am on Google homepage")
def open_google(context):
    context.driver = webdriver.Chrome()

    # IMPORTANT FIX: avoid regional redirects
    context.driver.get("https://www.google.com/ncr")

    context.wait = WebDriverWait(context.driver, 20)


# WHhen: search for query
@when('I search for "{query}"')
def search_google(context, query):
    wait = context.wait

    # wait page load
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # cookie popup (more robust)
    try:
        buttons = context.driver.find_elements(By.XPATH, "//button")
        for b in buttons:
            if "accept" in b.text.lower() or "acept" in b.text.lower():
                b.click()
                break
    except:
        pass

    # IMPORTANT FIX: wait for clickable, NOT just presence
    search_box = wait.until(
        EC.element_to_be_clickable((By.NAME, "q"))
    )

    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)

    # wait results fully loaded
    wait.until(
        EC.presence_of_element_located((By.ID, "search"))
    )



# When: click first result
@when("I click the first result")
def click_first_result(context):
    wait = context.wait

    first_result = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))
    )
    first_result.click()



# Then: domain check
@then('the page should contain "{domain}"')
def verify_domain(context, domain):
    wait = context.wait
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    assert domain.lower() in context.driver.page_source.lower()


# Then: keyword check
@then('results should contain "{keyword}"')
def verify_results(context, keyword):
    wait = context.wait
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    assert keyword.lower() in context.driver.page_source.lower()

    context.driver.quit()