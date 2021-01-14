import random
import pickle
import os.path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

following_list = []
login_count = 0


class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Chrome(executable_path="C:\\Users\\ashin\\Downloads\\chromedriver_win32\\chromedriver.exe")

    def login(self):
        global login_count
        bot = self.bot
        bot.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        bot.find_element_by_name("username").send_keys(self.username)
        bot.find_element_by_name("password").send_keys(self.password + Keys.RETURN)
        time.sleep(3)
        bot.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        time.sleep(3)
        if login_count <= 0:
            bot.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        login_count += 1

    def search_for_hash_tag(self, hashtags):
        bot = self.bot
        bot.get("https://www.instagram.com/" + hashtags)

    def like_photos(self, number_of_photos_to_like):
        bot = self.bot
        i = 1
        try:
            bot.find_element_by_class_name("v1Nh3").click()
            time.sleep(1)
            while i <= number_of_photos_to_like:
                bot.find_element_by_class_name("fr66n").click()
                time.sleep(2)
                bot.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
                i += 1
                time.sleep(2)
        except:
            print("Page not found error")

        bot.get("https://www.instagram.com/" + self.username + "/")
        time.sleep(3)
        bot.find_element_by_xpath("//img[@class='_6q-tv']").click()
        print("clicking profile")
        time.sleep(3)
        bot.find_element_by_xpath("//div[contains(text(), 'Log Out')]").click()
        print("clicking logout")
        time.sleep(3)
        bot.quit()

    def get_followers(self):
        bot = self.bot
        bot.get("https://www.instagram.com/" + self.username + "/")
        time.sleep(3)
        bot.find_element_by_xpath("//a[contains(@href,'followers')]").click()
        time.sleep(3)
        scroll_box = bot.find_element_by_xpath("//div[@class='isgrP']")
        followers = int(bot.find_element_by_xpath("//li[2]/a/span").text)
        print(followers)
        # # scroll down the page
        for i in range(int(followers / 2)):
            bot.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
            time.sleep(random.randint(500, 1000) / 1000)
            print("Extracting friends %", round((i / (followers / 2) * 100), 2), "from", "%100")
        followers_list = []
        links = bot.find_elements_by_css_selector('li a')
        for a in links:
            name = a.get_attribute('title')
            if name != "":
                followers_list.append(name)
        with open('followers_list_file.data', 'wb') as filehandle:
            pickle.dump(followers_list, filehandle)
        print(followers_list)
        print(len(followers_list))
        return followers_list

    def get_following(self):
        global following_list
        bot = self.bot
        bot.get("https://www.instagram.com/" + self.username + "/")
        time.sleep(3)
        dialog = bot.find_element_by_xpath("//a[contains(@href,'following')]").click()
        time.sleep(3)
        scroll_box = bot.find_element_by_xpath("//div[@class='isgrP']")
        following = int(bot.find_element_by_xpath("//li[3]/a/span").text)
        print(following)
        # # scroll down the page
        for i in range(int(following / 2)):
            bot.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
            time.sleep(random.randint(500, 1000) / 1000)
            print("Extracting friends %", round((i / (following / 2) * 100), 2), "from", "%100")

        links = bot.find_elements_by_css_selector('li a')
        for a in links:
            name = a.get_attribute('title')
            if name != "":
                following_list.append(name)
        with open('following_list_file.data', 'wb') as filehandle:
            pickle.dump(following_list, filehandle)
        print(following_list)
        print(len(following_list))
        return following_list

    def unfollow(self, not_following_back):
        global following_list
        self.not_following_back = not_following_back
        bot = self.bot
        bot.get("https://www.instagram.com/" + self.username + "/")
        following_assumed = int(bot.find_element_by_xpath("//li[3]/a/span").text)
        i = 0
        for numbers in not_following_back:
            bot.get("https://www.instagram.com/" + not_following_back[i] + "/")
            print(numbers)
            time.sleep(random.randint(2, 6))
            bot.find_element_by_xpath("//span[@class='glyphsSpriteFriend_Follow u-__7']").click()
            time.sleep(3)
            bot.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
            time.sleep(4)
            bot.get("https://www.instagram.com/" + self.username + "/")
            following_assumed -= 1
            following = int(bot.find_element_by_xpath("//li[3]/a/span").text)
            if following == following_assumed:
                following_list.remove(numbers)
                i += 1
            else:
                # updating the file if dead lock encountered and login again
                with open('following_list_file.data', 'wb') as filehandle:
                    pickle.dump(following_list, filehandle)
                time.sleep(2)
                for count in range(25):
                    time.sleep(1)
                    print(str(count) + "sec")
                break


not_following_back = []
loop = True
following_loop = True
following = []
followers = []
random_topics = ["foodporn", "motivation", "amazing", "family", "dog", "sun", "sky"]
while loop:
    insta = InstagramBot("username", "password")  # username and password
    insta.login()
    if not not_following_back:
        if not os.path.isfile('following_list_file.data'):
            print("file  doesnt exist")
            # file does not exist
            following = insta.get_following()
            followers = insta.get_followers()
        else:
            print("file exist")
            # opening a file called following_list_file.data and assign that data into following list
            with open('following_list_file.data', 'rb') as filehandle:
                following_list = pickle.load(filehandle)

            # opening a file called followers_list_file.data and assign that data into followers list
            with open('followers_list_file.data', 'rb') as filehandle:
                followers = pickle.load(filehandle)
        following_loop = False
    # comparing both the followings and followers
    # and making the list whoever not following back
    not_following_back = [item for item in following_list if item not in followers]
    if not_following_back:
        insta.unfollow(not_following_back)
        insta.search_for_hash_tag(random.choice(random_topics))
        insta.like_photos(random.randint(2, 5))
    else:
        # removing followers and following list files
        os.remove('followers_list_file.data')
        os.remove('following_list_file.data')
        print("task complete")
        loop = False
