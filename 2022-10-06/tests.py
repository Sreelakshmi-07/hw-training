from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.webkit.launch(headless=False)
    page = browser.new_page()
    page.goto(
        'https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723')
    title = '//span[@data-aut-id="itemTitle"]'
    price = '//span[@data-aut-id="itemPrice"]'
    details = '//span[@data-aut-id="itemDetails"]'
    title_ = page.query_selector_all(title)
    price_ = page.query_selector(price)
    details_ = page.query_selector(details)
    for item in title_:
        title = item
        print("Title: ",title.inner_text())
    # print("Title: ", title_.inner_text(), "\n"
    #       "Price: ", price_.inner_text(), "\n",
    #       "Details: ", details_.inner_text())

    page.wait_for_timeout(6000)

    browser.close()
