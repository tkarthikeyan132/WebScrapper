import khan.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import json
import csv

class Khan(webdriver.Chrome):
    def __init__(self,driver_path=r"/home/tkarthikeyan/IIT Delhi/RP/rp/chromedriver",teardown=False):
        self.driver_path=driver_path
        self.dict_data=[]
        os.environ['PATH']+=self.driver_path
        options=webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)
        options.add_experimental_option("excludeSwitches",['enable-logging'])
        self.teardown = teardown
        super(Khan,self).__init__(options=options)
        self.implicitly_wait(30)
    
    def __exit__(self, exc_type, exc_value, trace):
        if self.teardown:
            self.quit()

    def land_homepage(self):
        self.get(const.BASE_URL)  

    def get_boxes(self):
        progress= self.find_element(By.ID, 'topic-progress')
        
        lesson_cards= progress.find_elements(By.CSS_SELECTOR,'div[data-test-id="lesson-card"]')
        print(len(lesson_cards))
        return lesson_cards

    def get_links(self,lesson_cards):
        all_video_links=[]
        for card in lesson_cards:
            video_lists= card.find_elements(By.CSS_SELECTOR,'ul li:has(span[aria-label="Video"])')
            for v in video_lists:
                a= v.find_element(By.TAG_NAME,'a')
                all_video_links.append(a)
        return all_video_links

        
    def get_content(self,videos):
        links=[]
        for a in videos:
            try:
                links.append(str(a.get_attribute('href')))
            except Exception as e:
                raise
        return links

    # def land_video_page(self):
    #     self.get(const.VIDEO_URL)

    def get_video_link(self):
        vid = self.find_element(By.CSS_SELECTOR, 'iframe[class^="player ka-player-iframe"]')
        video_uid = vid.get_attribute("data-youtubeid")
        # self.temp_dict["video_id"] = video_uid
        return video_uid

    def get_subtitles(self):
        subtitles= {}
        tr_button = self.find_element(By.CSS_SELECTOR, 'button[data-test-id="videoTabTranscript"]')
        tr_button.click()
        ul = self.find_element(By.CSS_SELECTOR, 'ul[itemprop="transcript"]')
        li = ul.find_elements(By.CSS_SELECTOR, 'ul li')
        for l in li:
            spans = l.find_elements(By.CSS_SELECTOR, 'span')
            # for s in spans:
            #     if str(s.text) not in ["", ".",'•']:
            #         print(s.text.strip())
            subtitles[str(spans[-2].text)] = str(spans[-1].text)
            
        # self.temp_dict["subtitles"] = subtitles
        return subtitles

    def get_about(self):
        about = self.find_element(By.CSS_SELECTOR, 'div[id="ka-videoPageTabs-tabbedpanel-content"]')
        # self.temp_dict["about"] = about.text
        return about.text
        
    def get_text_transcript(self):
        transcript= self.find_element(By.CSS_SELECTOR, 'div[itemprop="transcript"]')
        # self.temp_dict["transcript"] = transcript.text
        return transcript.text

    def get_discussion_posts(self):
        discussion_posts = self.find_elements(By.CSS_SELECTOR, 'li[data-test-id="discussion-list-item"]')
        qid = 0
        # self.temp_dict["qa-pairs"] = []
        qa_pairs = []
        for discussion_post in discussion_posts:    
            try:
                question_raw = discussion_post.find_element(By.CSS_SELECTOR, 'div[class="_1t544yo9"]')
                answer_raw = discussion_post.find_element(By.CSS_SELECTOR, 'div[class="_3qeerd"]')

                question = question_raw.find_element(By.CSS_SELECTOR, 'span[class="_1glfes6x"]')
                answer = answer_raw.find_element(By.CSS_SELECTOR, 'span[class="_1glfes6x"]')
                
                temp_temp_dict = {}
                temp_temp_dict["qid"] = qid
                temp_temp_dict["q"] = question.text
                temp_temp_dict["a"] = answer.text
                # self.temp_dict["qa-pairs"].append(temp_temp_dict)
                qa_pairs.append(temp_temp_dict)
                qid += 1
                
                # print("NEW DISCUSSION POST") 
                # print("QUESTION ",question.text)
                # print("ANSWER ",answer.text)
            except:
                continue
            
            # print("ANSWER ",answer.get_attribute("outerHTML"))
        return qa_pairs
    

    def scrape_links(self, links):
        for link in links:
            self.get(link)
            temp_dict = {}
            video_link = self.get_video_link()  #<-- DONE
            about = self.get_about()
            subtitles = self.get_subtitles()

            text_transcript = self.get_text_transcript()
            discussion_posts = self.get_discussion_posts()
            
            temp_dict["vid"] = video_link
            temp_dict["about"] = about
            temp_dict["subtitles"] = subtitles
            temp_dict["transcript"] = text_transcript
            temp_dict["qa-pairs"] = discussion_posts
            self.dict_data.append(temp_dict)

            print("DONE with video : ",video_link)

            self.back()
            ## add your code here
            ## use self as driver/bot

    def dump_to_json(self):
        file = open("video.json",'w')
        json.dump(self.dict_data,file, indent=4)
        
    def dump_to_csv(self):
        csvfile = open("video.csv",'w')
        writer = csv.DictWriter(csvfile, fieldnames=self.temp_dict.keys())
        writer.writeheader()
        writer.writerow(self.temp_dict)
        
        
    
    

