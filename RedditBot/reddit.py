import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import time

class Reddit:
    def __init__(self, driver, username, password, browse_communities):
        self.init_cookies = False
        self.driver = driver
        self.username = username
        self.password = password
        self.browse_communities = browse_communities
        self.logged = None
        self.post_timestamp = time()
        self.browse_duration = 0.0
        self.browse_timestamp = 0.0
        self.action_duration = 0.0
        self.action_timestamp = 0.0
        self.current_browse_community = ""

        self.driver.add_cdp_listener("Network.responseReceived", self.HandleLoginReceived)

    def HandleLoginReceived(self, response):
        url = response["params"]["response"]["url"]
        
        if (url == "https://www.reddit.com/login" or url == "https://www.reddit.com/login/") and response["params"]["type"] == "XHR":
            self.logged = response["params"]["response"]["status"] == 200

    def IsloggedIn(self):
        if self.logged:
            return True

        cookies = self.driver.get_cookies()

        for cookie in cookies:
            if cookie["domain"] == "www.reddit.com" and cookie["name"] == "session" and cookie["value"] != "":
                return True

        return False
    
    def LogIn(self):
        try:
            # Open the website
            self.driver.get("https://www.reddit.com/login/")

            # Wait for the username and password text boxes to be visible
            wait = WebDriverWait(self.driver, 20)
            username_box = wait.until(EC.visibility_of_element_located((By.ID, "loginUsername")))
            password_box = wait.until(EC.visibility_of_element_located((By.ID, "loginPassword")))

            # Fill in the username and password
            username_box.send_keys(self.username)
            password_box.send_keys(self.password)

            # Wait for the loging button to be clickable
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "AnimatedForm__submitButton.m-full-width")))

            self.logged = None

            button.click()

            # Wait for the login result
            start_time = time()

            while time() - start_time < 60:  # Wait for up to 60 seconds
                if self.logged is not None:
                    return self.logged

            return False
        except:
            print("LogIn: Unknown error.")
            return False
        
    def GoMainPage(self):
        try:
            # Open the website
            self.driver.get("https://www.reddit.com/")
            return True
        except:
            return False

    def CreatePost(self, community, title, text):
        try:
            # Open the website
            self.driver.get("https://www.reddit.com/submit")

            #Todo

            self.post_timestamp = time()
            return True
        except:
            return False
        
    def GoTo(self, community):
        try:
            self.driver.get("https://www.reddit.com/" + community)

            return True
        except:
            return False

    def ScrollDown(self):
        try:
            html = self.driver.find_element(By.TAG_NAME, "html")
            html.send_keys(Keys.PAGE_DOWN)

            return True
        except:
            return False
        
    def CheckActionTime(self):
        return time() - self.action_timestamp > self.action_duration
    
    def ResetActionTime(self):
        self.action_timestamp = time()

    def CheckBrowseDuration(self):
        return time() - self.browse_timestamp > self.browse_duration
    
    def ResetBrowseDuration(self):
        self.browse_timestamp = time()
        
    def GetCurrentUrl(self):
        return str(self.driver.current_url)
    
    def GetInitCookies(self):
        return self.init_cookies
    
    def GetUsername(self):
        return self.username
    
    def GetPassword(self):
        return self.password

    def GetBrowseDuration(self):
        return self.browse_duration
    
    def GetBrowseCommunities(self):
        return self.browse_communities
    
    def GetCurrentBrowseCommunity(self):
        return self.current_browse_community
    
    def SetInitCookies(self, value):
        self.init_cookies = value

    def SetBrowseDuration(self, duration):
        self.browse_duration = duration

    def SetCurrentBrowseCommunity(self, community):
        self.current_browse_community = community

    def SetActionDuration(self, duration):
        self.action_duration = duration