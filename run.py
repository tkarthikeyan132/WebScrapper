# from selenium import webdriver
# from selenium.webdriver import Chrome
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

from khan.khan import Khan

with Khan() as bot:
    bot.land_homepage()
    units= bot.get_units()
    units.pop()
    print('unit Links scraped')
    units=units[5:]
    print(len(units))

    bot.scrape_units(units,'check.json')

    print("dumping files")
    bot.dump_video_links(6)
    bot.dump_to_json(6)







