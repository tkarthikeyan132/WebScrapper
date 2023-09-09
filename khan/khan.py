import khan.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import json
import csv
import time

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
        self.implicitly_wait(60)
        self.video_links=[]
    
    def __exit__(self, exc_type, exc_value, trace):
        if self.teardown:
            self.quit()

    def land_homepage(self):
        self.get(const.BASE_URL)

    def get_units(self):
        units=[]
        sidebar = self.find_element(By.CSS_SELECTOR,'nav[data-test-id = "course-unit-sidebar"]')
        unit_a = sidebar.find_elements(By.TAG_NAME,'a')
        for u in unit_a:
            units.append(str(u.get_attribute('href')))
        return units[1:]

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
    
    def get_unit_title(self):
        title = self.find_element(By.CSS_SELECTOR, 'h1[data-test-id="course-unit-title"]')
        return title.text

        
    def get_content(self,videos):
        links=[]
        for a in videos:
            try:
                video_title = (a.find_element(By.CLASS_NAME,"_14hvi6g8")).text
                links.append((video_title,(str(a.get_attribute('href')))))
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
        # about = self.find_element(By.CSS_SELECTOR, 'div[id="ka-videoPageTabs-tabbedpanel-content"]')
        about = self.find_element(By.ID, 'ka-videoPageTabs-tabbedpanel-content')
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
                question_raw = discussion_post.find_element(By.CLASS_NAME, "_1t544yo9")
                answer_raw = discussion_post.find_element(By.CLASS_NAME, "_3qeerd")
                question = question_raw.find_element(By.CLASS_NAME, "_1glfes6x")
                answer = answer_raw.find_element(By.CLASS_NAME, "_1glfes6x")
                
                my_dict = {}
                my_dict["qid"] = qid
                my_dict["q"] = question.text
                my_dict["a"] = answer.text
                # self.temp_dict["qa-pairs"].append(temp_temp_dict)
                qa_pairs.append(my_dict)
                qid += 1
                
                # print("NEW DISCUSSION POST") 
                # print("QUESTION ",question.text)
                # print("ANSWER ",answer.text)
            except:
                continue
            
            # print("ANSWER ",answer.get_attribute("outerHTML"))
        return qa_pairs
    

    def scrape_units(self,units,filename):
        num_links = 0
        for u in units:
            self.get(u)
            unit_title = self.get_unit_title()
            cards = self.get_boxes()
            a_tags = self.get_links(cards)
            href_tags= self.get_content(a_tags)

            num_links += len(href_tags)

            existing_data=[]

            try:
                with open(filename,'r') as f:
                    existing_data= json.load(f)
                    f.close()
            except:
                continue
            t1= time.time()

            for video_title,link in href_tags:
                self.get(link)
                temp_dict = {} 
                
                try:
                    video_link = self.get_video_link()
                except:
                    print("Could not find video link .. SKIPPED")
                    continue

                # t2= time.time()
                # print('timevid:',t2-t1)

                try:
                    about = self.get_about()
                except:
                    print("No about for ",video_link)
                    about = ""
                # t3= time.time()
                # print('timeabout:',t3-t2)

                try:
                    subtitles = self.get_subtitles()
                except:
                    print("No subtitles for ",video_link)
                    subtitles = {}
                # t4= time.time()
                # print('tsubs:',t4-t3)

                try:
                    text_transcript = self.get_text_transcript()
                except:
                    print("No text transcript found .. SKIPPED ", video_link)
                    continue
                # t5= time.time()
                # print('timetranscript:',t5-t4)

                try:
                    discussion_posts = self.get_discussion_posts()
                except:
                    print("No discussion posts found.. SKIPPED ", video_link)
                    continue
                # t6= time.time()
                # print('disscn:', t6-t5)



                temp_dict["unit-title"]=unit_title
                temp_dict["video-title"]=video_title
                temp_dict["vid"] = video_link
                temp_dict["about"] = about
                temp_dict["subtitles"] = subtitles
                temp_dict["transcript"] = text_transcript
                temp_dict["qa-pairs"] = discussion_posts

                existing_data.append(temp_dict)
                self.dict_data.append(temp_dict)
                self.video_links.append(video_link)

                print("DONE with video : ",video_link)
            t2= time.time()
            print("UNIT SCRAPED ",t2-t1)
            with open(filename,'w') as f:
                json.dump(existing_data,f,indent=4)
                f.close()
        print('Total videos scraped : ',num_links)
        return self.dict_data
    
    def dump_video_links(self,grade):
        file = open(f'video_uid_class_{grade}_MATH_INDIA.txt','w')
        for item in self.video_links:
            file.write(item+"\n")
        file.close()

    def dump_to_json(self, grade):
        file = open(f'class_{grade}_MATH_INDIA.json','w')
        json.dump(self.dict_data,file, indent=4)
        file.close()
        
    def dump_to_csv(self):
        csvfile = open("video.csv",'w')
        writer = csv.DictWriter(csvfile, fieldnames=self.temp_dict.keys())
        writer.writeheader()
        writer.writerow(self.temp_dict)
        csvfile.close()
