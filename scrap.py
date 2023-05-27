from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time


# Open new CSV file
csv_file = open("output.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Product URL", "Product Name", "Price", "Rating", "Number of Reviews", "Description", "ASIN", "Product Description", "Manufacturer"])

page_no = 1
url = f"https://www.amazon.in/s?k=bags&page={page_no}&crid=2M096C61O4MLT&qid=1685098187&sprefix=ba%2Caps%2C283&ref=sr_pg_2"
driver = webdriver.Chrome(ChromeDriverManager().install())
##driver.get(url)
product_urls = driver.find_elements(by=By.XPATH, value="*//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")

product_names = driver.find_elements(By.XPATH, value="*//span[@class='a-size-medium a-color-base a-text-normal']")

prices = driver.find_elements(By.XPATH, value="*//span[@class='a-price-whole']")

for page in range(20):
    url = f"https://www.amazon.in/s?k=bags&page={page}&crid=2M096C61O4MLT&qid=1685098187&sprefix=ba%2Caps%2C283&ref=sr_pg_2"
    driver.get(url)
##    product_urls = driver.find_elements(by=By.XPATH, value="*//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
##
##    product_names = driver.find_elements(By.XPATH, value="*//span[@class='a-size-medium a-color-base a-text-normal']")
##
##    prices = driver.find_elements(By.XPATH, value="*//span[@class='a-price-whole']")
    
    for i in range(10):
        product_urls = driver.find_elements(by=By.XPATH, value="*//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
        product_names = driver.find_elements(By.XPATH, value="*//span[@class='a-size-medium a-color-base a-text-normal']")
        prices = driver.find_elements(By.XPATH, value="*//span[@class='a-price-whole']")

        product_url = product_urls[i].get_attribute("href")
        name = product_names[i].text
        price = prices[i].text
        driver.get(product_url)
        try:
            rating = driver.find_element(By.XPATH, value="*//i[@class='a-icon a-icon-star a-star-4-5 cm-cr-review-stars-spacing-big']")
            rating = rating.get_attribute("innerHTML").split(">")[1].split("<")[0]
        except:
            rating = "0 out of 5 stars"
        try:
            number_of_reviews = driver.find_element(By.XPATH, value="*//span[@id='acrCustomerReviewText']").text
        except:
            number_of_reviews = "0 ratings"

        description_ul = driver.find_element(By.XPATH, value="*//ul[@class='a-unordered-list a-vertical a-spacing-mini']")
        description_texts = description_ul.find_elements(By.CLASS_NAME, "a-list-item")
        description = ""
        for txtHtml in description_texts:
            description += txtHtml.text

        ASIN = driver.current_url.split("/dp/")[1].split("/")[0]
        try:
            product_description = driver.find_element(By.ID, "productDescription").text
        except:
            product_description = ""
        manufacturer = name.split()[0]
        print("working")
        print(product_url, name, price, rating, number_of_reviews, description, ASIN, product_description, manufacturer)
        driver.get(url)
        time.sleep(3)
        

        csv_writer.writerow([product_url, name, price, rating, number_of_reviews, description, ASIN, product_description, manufacturer])
        
        driver.get(url)
        time.sleep(3)


# Close CSV file
csv_file.close()