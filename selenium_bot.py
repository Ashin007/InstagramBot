import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

following_list = []


class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Chrome(executable_path="C:\\Users\\ashin\\Downloads\\chromedriver_win32\\chromedriver.exe")

    def login(self):
        bot = self.bot
        bot.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        bot.find_element_by_name("username").send_keys(self.username)
        bot.find_element_by_name("password").send_keys(self.password + Keys.RETURN)
        time.sleep(3)
        bot.find_element_by_class_name("y3zKF").click()
        time.sleep(3)
        bot.find_element_by_class_name("HoLwm").click()

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
                time.sleep(3)
                bot.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
                i += 1
                time.sleep(3)
        except:
            print("some error")

        bot.get("https://www.instagram.com/" + self.username + "/")

    def get_followers(self):
        bot = self.bot
        bot.get("https://www.instagram.com/" + self.username + "/")
        time.sleep(3)
        dialog = bot.find_element_by_xpath("//a[contains(@href,'followers')]").click()
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
        print(following_list)
        print(len(following_list))
        return following_list

    def unfollow(self, not_following_back):
        global following_list
        self.not_following_back = not_following_back
        bot = self.bot
        bot.get("https://www.instagram.com/ashin_v7/")
        following_assumed = int(bot.find_element_by_xpath("//li[3]/a/span").text)
        i = 0
        for numbers in not_following_back:
            # followers = int(bot.find_element_by_xpath("//li[2]/a/span").text)
            bot.get("https://www.instagram.com/" + not_following_back[i] + "/")
            print(numbers)
            time.sleep(random.randint(2, 6))
            bot.find_element_by_xpath("//span[@class='glyphsSpriteFriend_Follow u-__7']").click()
            time.sleep(3)
            bot.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
            following_list.remove(numbers)
            time.sleep(4)
            bot.get("https://www.instagram.com/ashin_v7/")
            following_assumed -= 1
            following = int(bot.find_element_by_xpath("//li[3]/a/span").text)
            if following == following_assumed:
                i += 1
            else:
                time.sleep(random.randint(10, 50))
                break


loop = True
following_loop = True
following = []
followers = []
random_topics = ["likes", "follow", "likeforlikes", "love", "instagood", "instagram", "followforfollowback", "followme",
                 "followforfollowback", "photooftheday", "photography", "instadaily", "me", "likeforfollow", "fashion",
                 "smile", "bhfyp", "likes", "summer", "foodporn", "motivation", "amazing", "family", "dog", "sun",
                 "sky"]
insta = InstagramBot("username", "password")  # username and password
insta.login()
while (loop):
    if following_loop:
        following = insta.get_following()
        followers = insta.get_followers()
        following_loop = False

    print(following_list)
    print(following)
    not_following_back = [item for item in following_list if item not in followers]
    if not_following_back:
        with open('following_list.txt', 'w') as f:
            for item in not_following_back:
                f.write("%s\n" % item)
        print(not_following_back)
        insta.unfollow(not_following_back)
        insta.search_for_hash_tag(random.choice(random_topics))
        insta.like_photos(random.randint(2, 5))

    else:
        print("task complete")
        loop = False

