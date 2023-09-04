from khan.khan import Khan
with Khan() as bot:
    # bot.land_homepage()
    # # bot.get_boxes()
    bot.land_homepage()
    cards = bot.get_boxes()
    a_tags = bot.get_links(cards)
    href_tags= bot.get_content(a_tags)
    bot.scrape_links(href_tags)

    # bot.land_video_page()
    # bot.get_video_link()  #<-- DONE
    # bot.get_about()
    # bot.get_subtitles()

    # bot.get_text_transcript()
    # bot.get_discussion_posts()
    bot.dump_to_json() 
    # bot.dump_to_csv()
    # cards = bot.get_boxes()
    # links = bot.get_links(cards)
    # bot.get_content(links)