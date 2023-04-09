import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("start-maximized")
# Initialize the browser
browser = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
# Navigate to the page
browser.get("https://www.thesparksfoundationsingapore.org/")

# page1- homepage
print("***** Homepage *****")
# test 1.1 - page load
print("Test 1.1: Page loading")
# Wait for the page to load
try:
    WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    if "Home" in browser.title:
        print(f'\tPage loaded successfully: {browser.title}')
    else:
        print('\tPage failed to load')
except:
    print(f'\tPage failed to load: {browser.title}')

# test 1.2 - navbar load
print("Test 1.2: Navbar loading")
# Wait for the page to load
try:
    navbar_element = WebDriverWait(browser, 10).until(
        expected_conditions.visibility_of_element_located((By.TAG_NAME, 'nav'))
    )
    print('\tNavbar loaded successfully')
except:
    print('\tNavbar failed to load')
time.sleep(1)

# test 1.3 - navbar brand logo load
print("Test 1.3: Navbar brand logo loading")
# Wait for the page to load
try:
    logo_attribute_name = 'src'
    logo_attribute_value = '/images/logo_small.png'
    logo_element = WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//img[@{logo_attribute_name}='{logo_attribute_value}']"))
    )
    # Check if the logo image has loaded
    if logo_element.get_attribute('complete'):
        print('\tLogo on navbar loaded successfully')
    else:
        print('\tLogo on navbar failed to load')
except:
    print('\tLogo on navbar not found')
time.sleep(1)

# test 1.4 - test about us links on navabr
print("Test 1.4: About Us links loading")
element_attribute_name = "data-hover"
element_attribute_value = "About"
about_us_element = browser.find_element(
    By.XPATH, f"//a[@{element_attribute_name}='{element_attribute_value}']")
about_us_element.click()
print('\tAbout Us on navbar clicked')
time.sleep(2)
parent_element_locator = (By.CSS_SELECTOR, 'ul.dropdown-menu')

# Find all the child <li> elements of the parent <ul> element
list_elements = browser.find_elements(*parent_element_locator)

# Iterate over the list of elements and test each link
link_urls = []
for element in list_elements:
    link_element = element.find_element(By.TAG_NAME, 'a')
    link_urls.append(link_element.get_attribute('href'))
for url in link_urls:
    browser.get(url)
    if browser.current_url == url:
        print(f'\tLink {url} works')
    else:
        print(f'\tLink {url} is broken')
    time.sleep(1)
    browser.back()
    time.sleep(1)

# testing pages that come under About Us

# page2
print("***** Page 2 *****")
# test 2.1 - page load
url = link_urls.pop(0)
browser.get(url)
print(f"Test 2.1: Page loading- {url}")
# Wait for the page to load
try:
    WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    print('\tPage loaded successfully')
except:
    print('\tPage failed to load')
time.sleep(1)

# test 2.2 - navbar load
print("Test 2.2: Navbar loading")
# Wait for the page to load
try:
    navbar_element = WebDriverWait(browser, 10).until(
        expected_conditions.visibility_of_element_located((By.TAG_NAME, 'nav'))
    )
    print('\tNavbar loaded successfully')
except:
    print('\tNavbar failed to load')
time.sleep(1)

# test 2.3 - navbar brand logo load
print("Test 2.3: Navbar brand logo loading")
# Wait for the page to load
try:
    logo_attribute_name = 'src'
    logo_attribute_value = '/images/logo_small.png'
    logo_element = WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//img[@{logo_attribute_name}='{logo_attribute_value}']"))
    )
    # Check if the logo image has loaded
    if logo_element.get_attribute('complete'):
        print('\tLogo on navbar loaded successfully')
    else:
        print('\tLogo on navbar failed to load')
except:
    print('\tLogo on navbar not found')
time.sleep(1)

# test 2.4 - heading load
print("Test 2.4: Page heading loading")
# Find all the <h2> elements
h2_elements = browser.find_elements(By.TAG_NAME, 'h2')
# Create a list of the text content of each <h2> element
h2_text_list = [element.text.lower() for element in h2_elements]
h2_words_list = []
for string in h2_text_list:
    h2_words_list.extend([word.replace(",", "") for word in string.split()])

check_url = browser.current_url
words = check_url.split("/")[-2:]
words.pop()
words[0] = words[0].replace("-", " ")
check_words = words[0].split()
# print(check_words)
# print(h2_text_list)
if (all(item in h2_words_list for item in check_words)):
    print("\tCorrect heading loaded successfully")
else:
    print("\tCorrect heading loading failed")
time.sleep(1)
browser.back()
time.sleep(1)

# back to homepage
# scroll down to footer
# test 3- footer
print("***** Footer *****")
# Get the current height of the page
page_height = browser.execute_script('return document.body.scrollHeight')

# Set the scroll position to 0
scroll_position = 0

# Set the scrolling increment
scroll_increment = 10

# Scroll down the page gradually
while scroll_position < page_height:
    browser.execute_script('window.scrollTo(0, {});'.format(scroll_position))
    scroll_position += scroll_increment
    browser.implicitly_wait(0.1)
# check social media link - linkedIn
print("Test 3.1: LinkedIn link loading")
# select and click linkedin icon
linkedin_icon = browser.find_element(By.CSS_SELECTOR, "i.fa-linkedin")
time.sleep(0.5)
linkedin_icon.click()


# Switch the driver's focus to the new tab
browser.switch_to.window(browser.window_handles[1])

# Wait for the overlay to appear
try:
    overlay_element = WebDriverWait(browser, 10).until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, '.modal__overlay--visible'))
    )
    # Check if the overlay is displayed
    if overlay_element.is_displayed():
        # Close the overlay
        close_button = browser.find_element(
            By.CSS_SELECTOR, '.modal__overlay--visible.modal__dismiss')
        close_button.click()
except:
    print('\tLinkedIn profile failed to load')


# Continue with the rest of the script
# Check elements in the new tab
# Wait for the page to load
try:
    profile_name_element = WebDriverWait(browser, 10).until(
        expected_conditions.visibility_of_element_located(
            (By.CLASS_NAME, "top-card-layout__title"))
    )
    # Check if the element is found
    if profile_name_element.is_displayed():
        # Check if the profile opened in of tsf
        if profile_name_element.text == "The Sparks Foundation":
            print('\tLinkedIn profile loaded successfully')
        else:
            print('\tLinkedIn profile failed to load')
except:
    print('\tLinkedIn profile failed to load')
# Close the new tab
browser.close()
# Switch the driver's focus back to the original tab
browser.switch_to.window(browser.window_handles[0])


# page4
print("***** Page 4 *****")
# test 4.1 - page load
url = "https://www.thesparksfoundationsingapore.org/contact-us/"
browser.get(url)
print(f"Test 4.1: Page loading- {url}")
# Wait for the page to load
try:
    WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    print('\tPage loaded successfully')
except:
    print('\tPage failed to load')
time.sleep(1)

# test 4.2 - navbar load
print("Test 4.2: Navbar loading")
# Wait for the page to load
try:
    navbar_element = WebDriverWait(browser, 10).until(
        expected_conditions.visibility_of_element_located((By.TAG_NAME, 'nav'))
    )
    print('\tNavbar loaded successfully')
except:
    print('\tNavbar failed to load')
time.sleep(1)

# test 4.3 - navbar brand logo load
print("Test 4.3: Navbar brand logo loading")
# Wait for the page to load
try:
    logo_attribute_name = 'src'
    logo_attribute_value = '/images/logo_small.png'
    logo_element = WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//img[@{logo_attribute_name}='{logo_attribute_value}']"))
    )
    # Check if the logo image has loaded
    if logo_element.get_attribute('complete'):
        print('\tLogo on navbar loaded successfully')
    else:
        print('\tLogo on navbar failed to load')
except:
    print('\tLogo on navbar not found')
time.sleep(1)

# test 4.4 - heading load
print("Test 4.4: Page heading loading")
# Find all the <h2> elements
h2_elements = browser.find_elements(By.TAG_NAME, 'h2')
# Create a list of the text content of each <h2> element
h2_text_list = [element.text.lower() for element in h2_elements]
h2_words_list = []
for string in h2_text_list:
    h2_words_list.extend([word.replace(",", "") for word in string.split()])

check_url = browser.current_url
words = check_url.split("/")[-2:]
words.pop()
words[0] = words[0].replace("-", " ")
check_words = words[0].split()
# print(check_words)
# print(h2_text_list)
if (all(item in h2_words_list for item in check_words)):
    print("\tCorrect heading loaded successfully")
else:
    print("\tCorrect heading loading failed")
time.sleep(1)
browser.back()
time.sleep(1)

# page5
print("***** Page 5 *****")
# test 5.1 - page load
url = "https://www.thesparksfoundationsingapore.org/join-us/why-join-us/"
browser.get(url)
print(f"Test 5.1: Page loading- {url}")
# Wait for the page to load
try:
    WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    print('\tPage loaded successfully')
except:
    print('\tPage failed to load')
time.sleep(1)

# test 5.2 - navbar load
print("Test 5.2: Navbar loading")
# Wait for the page to load
try:
    navbar_element = WebDriverWait(browser, 10).until(
        expected_conditions.visibility_of_element_located((By.TAG_NAME, 'nav'))
    )
    print('\tNavbar loaded successfully')
except:
    print('\tNavbar failed to load')
time.sleep(1)

# test 5.3 - navbar brand logo load
print("Test 5.3: Navbar brand logo loading")
# Wait for the page to load
try:
    logo_attribute_name = 'src'
    logo_attribute_value = '/images/logo_small.png'
    logo_element = WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f"//img[@{logo_attribute_name}='{logo_attribute_value}']"))
    )
    # Check if the logo image has loaded
    if logo_element.get_attribute('complete'):
        print('\tLogo on navbar loaded successfully')
    else:
        print('\tLogo on navbar failed to load')
except:
    print('\tLogo on navbar not found')
time.sleep(1)

# test 5.4 - heading load
print("Test 5.4: Page heading loading")
# Find all the <h2> elements
h2_elements = browser.find_elements(By.TAG_NAME, 'h2')
# Create a list of the text content of each <h2> element
h2_text_list = [element.text.lower() for element in h2_elements]
h2_words_list = []
for string in h2_text_list:
    h2_words_list.extend([word.replace(",", " ") for word in string.split()])

check_url = browser.current_url
words = check_url.split("/")[-2:]
words.pop()
words[0] = words[0].replace("-", " ")
check_words = words[0].split()
if (all(item in check_words for item in h2_words_list)):
    print("\tCorrect heading loaded successfully")
else:
    print("\tCorrect heading loading failed")
time.sleep(1)
browser.back()
time.sleep(1)

time.sleep(2)
# close the browser
browser.quit()
