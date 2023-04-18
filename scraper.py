import selenium
from webdriver_manager.chrome import ChromeDriverManager
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# https://www.youtube.com/watch?v=Xjv1sY630Uc


# setting up driver session
driver = webdriver.Chrome()

#take action on browser
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

#request browser info
title = driver.title

#establish waiting strategy
driver.implicitly_wait(0.5)

#find an element
text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

#take action
text_box.send_keys("Selenium")
submit_button.click()

#request element information
value = message.text

#end session
driver.quit()

# if __name__ == '__main__':