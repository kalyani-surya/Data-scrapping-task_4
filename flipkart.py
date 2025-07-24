from playwright.sync_api import sync_playwright
import csv

flipkartUrl = 'https://www.flipkart.com/'

def scrapeFlipkart():   

  with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(flipkartUrl)
        
        page.wait_for_timeout(4000)
        page.screenshot(path='flipkart.png', full_page=True)
        searchInput = page.query_selector('input.Pke_EE')
        searchInput.fill('laptop')
        page.wait_for_timeout(1000)
        searchBt = page.query_selector('button._2iLD__')
        searchBt.click()
        page.wait_for_load_state('domcontentloaded')
        page.wait_for_timeout(4000)
        page.screenshot(path='laptop_flipkart.png', full_page=True)

        allTitle = page.query_selector_all('div.KzDlHZ')



        for title in allTitle:
            print('title',title.inner_text())

            allrating_star= page.query_selector_all('div.XQDdHH')
        for rating in allrating_star:
            print(rating.inner_text(),"",'star')

        allrating_number = page.query_selector_all('span.Wphh3N')
        for rating in allrating_number:
            print(rating.inner_text().split("&")[0])
        
        allreviews = page.query_selector_all('span.Wphh3N')
        for review in allreviews:
            print(review.inner_text().split("&")[1])
        
        allLaptop_config = page.query_selector_all('div._6NESgJ')
        allLaptop_config_list = [Laptop_config.inner_text() for Laptop_config in allLaptop_config]
        split_list=[[item.strip() for item in config.split(',')] for config in allLaptop_config_list]
        for config in split_list:
            print(config)

        allOriginal_price = page.query_selector_all('div.yRaY8j.ZYYwLA')
        for price in allOriginal_price:
            print(price.inner_text())
        
        alldiscount_percentage = page.query_selector_all('div.UkUFwK')
        for discount in alldiscount_percentage:
            print(discount.inner_text())

        allDiscounted_price = page.query_selector_all('div.Nx9bqj._4b5DiR')
        for price in allDiscounted_price:
            print(price.inner_text())
        
        # Prepare data for CSV
        titles = [title.inner_text() for title in allTitle]
        ratings = [rating.inner_text() for rating in allrating_star]
        rating_numbers = [rating.inner_text().split("&")[0] for rating in allrating_number]
        reviews = [review.inner_text().split("&")[1] if "&" in review.inner_text() else "" for review in allreviews]
        configs = split_list
        original_prices = [price.inner_text() for price in allOriginal_price]
        discount_percentages = [discount.inner_text() for discount in alldiscount_percentage]
        discounted_prices = [price.inner_text() for price in allDiscounted_price]

        # Find the max length to pad shorter lists
        max_len = max(len(titles), len(ratings), len(rating_numbers), len(reviews), len(configs), len(original_prices), len(discount_percentages), len(discounted_prices))

        def pad(lst):
            return lst + [""] * (max_len - len(lst))

        # Pad all lists to the same length
        titles = pad(titles)
        ratings = pad(ratings)
        rating_numbers = pad(rating_numbers)
        reviews = pad(reviews)
        configs = pad(configs)
        original_prices = pad(original_prices)
        discount_percentages = pad(discount_percentages)
        discounted_prices = pad(discounted_prices)

        # Write to CSV
        with open('flipkart_laptops.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Star Rating', 'Rating Number', 'Reviews', 'Configuration', 'Original Price', 'Discount %', 'Discounted Price'])
            for i in range(max_len):
                writer.writerow([
                    titles[i],
                    ratings[i],
                    rating_numbers[i],
                    reviews[i],
                    ', '.join(configs[i]) if isinstance(configs[i], list) else configs[i],
                    original_prices[i],
                    discount_percentages[i],
                    discounted_prices[i]
                ])

scrapeFlipkart()
 


    
                        

    


