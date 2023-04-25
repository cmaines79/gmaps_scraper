# DON'T FORGET TO PIP FREEZE
# playwright install chromium
# to run the script from the cli "pyton(3) scraper.py -l=bozeman -s=lasers"

from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse

@dataclass
class Business:
	name: str = None
	address: str = None
	website: str = None
	phone_number: str = None

@dataclass
class BusinessList:
	business_list : list[Business] = field(default_factory=list)

	# return pandas dataframe so we can save the data to Excel and/or CSV.
	def dataframe(self):
		return pd.json_normalize((asdict(business) for business in self.business_list), sep='')

	def save_to_excel(self, filename):
		self.dataframe().to_excel(f'{filename}.xlsx', index = False)

	def save_to_csv(self, filename):
		self.dataframe().to_csv(f'{filename}.csv', index = False)

def main():
	# init playwright
	with sync_playwright() as p:
		# init browers and launch a new page
		browser = p.chromium.launch(headless=False)
		page = browser.new_page()

		# drive the browser to a specific page with the timeout set to 60 seconds.
		page.goto('https://www.google.com/maps', timeout=60000)
		
		# remove this in production or set to 1 second
		page.wait_for_timeout(5000)

		# get the input box and place some text in it.
		page.locator('//input[@id="searchboxinput"]').fill(search_for)
		page.wait_for_timeout(3000)

		# pressing the enter button in the search box rather than using the x-path.
		page.keyboard.press('Enter')
		page.wait_for_timeout(3000)

		# NEED TO FIGURE OUT THE INFINITE SCROLL PROBABLY HERE...
		
		# getting all of the business listings from the webpage by their x-path.
		listings = page.locator('//div[@role="article"]').all()
		print(len(listings))

		# create business list object
		business_list = BusinessList()

		# loop through the listings to allow the pop up with all of the business info to show.  
		# In this test database, we're only going after the first five
		for listing in listings[:5]:
			#click on each listing and wait some time
			listings.click()
			listings.wait_for_timeout(5000)

			# x-paths of the needed elements
			name_xpath = '//h1[contains(@class, "fontHeadlineLarge")]'
			address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
			website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
			phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
			# reviews_span_xpath = '//span[@role="img"]'

			# creating a new business object using the x-paths above
			business = Business()
			business.name = page.locator(name_xpath).inner_text()
			business.address = page.locator(address_xpath).inner_text()
			business.website = page.locator(website_xpath).inner_text()
			business.phone_number = page.locator(phone_number_xpath).inner_text()	

			# append our Businesses to our BusinessList
			business_list.business_list.append(business)

			# save our data to excel and/or CSV - SHOULD WE THROUGH THIS INTO ITS OWN FUNCTION WITH ACCESS TO THE ARGS FOR USE IN THE FILENAME?
			business_list.save_to_excel(f'gmaps_data')
			business_list.save_to_csv(f'gmpas_data')

		# close the browser
		browser.close()

if __name__ == '__main__':
	
	# gives us a way to enter arguemnts in the command line so they will passed to the CLI.
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--search", type=str)
	parser.add_argument("-l", "--location", type=str)
	args = parser.parse_args()

	# if we have valid arguments, then assign the f-string
	if(args.location and args.search):
		search_for = f'{args.search} {args.location}'
	else:
		# if the user has not entered valid args, we'll use the default
		search_for = 'YAG Lasers Bozeman, MT'

	main()