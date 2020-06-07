from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import youtube_dl
from getpass import getpass
from sys import platform

config = {
    'EMAIL': '',
    'PASSWORD': ''
}

login_url = 'https://video.dtu.dk/user/login'


def main():
    # Prompt for login details
    config['EMAIL'] = input("Please enter your DTU email (xxx@dtu.dk or s123456@student.dtu.dk): ")
    config['PASSWORD'] = getpass("Please enter your DTU password: ")

    # Prompt for video URL
    video_url = input("Please enter the video URL: ")
    print("Hold tight, magic is happening!")

    # Specify window to not open
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    # Specify window to not open
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    if platform == "linux" or platform == "linux2" or platform == "darwin":
        # If Linux or MacOS
        driver = webdriver.Chrome('./chromedriver', options=options)
    elif platform == "win32":
        # Or if Windows
        driver = webdriver.Chrome('./chromedriver.exe', options=options)
    else:
        raise Exception("Unknown operating system.")

    driver.get(login_url)
    assert 'Login - DTU - MediaSpace' in driver.title
    elem = driver.find_element_by_name('Login[username]')
    elem.clear()
    elem.send_keys(config['EMAIL'])
    elem = driver.find_element_by_name('Login[password]')
    elem.clear()
    elem.send_keys(config['PASSWORD'])
    elem.send_keys(Keys.RETURN)

    i = True
    while i:
        try:
            expected_url = driver.current_url
            actual_url = "https://video.dtu.dk/"
            assert expected_url == actual_url
            i = False
        except AssertionError:
            time.sleep(1)
            continue

    # Load video page
    driver.get(video_url)
    
    #Check if video_url starts with video.dtu.dk/category/. In that case, we should download all of videos in said category.
    if 'video.dtu.dk/category/' in video_url:
        j = True
        multiple_videos = True
        while j:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #Scroll down 
            time.sleep(2)
            try:   
                elem = driver.find_element_by_xpath('//*[@id="channelGallery"]/div/a')
                elem.click()
            except: #Perhaps some errortype here?
                #No more media items to load. Scroll back to the top.
                j = False
                driver.execute_script("window.scrollTo(0, 0);")
                continue
        
        #Now, we want to extract all of the URL from the gallery links.
        j = True
        idx = 1
        video_urls = []
        while j:
            try:
                elem = driver.find_element_by_xpath('//*[@id="gallery"]/li[' + str(idx) + ']/div[1]/div[1]/div/p/a')
                driver.execute_script("arguments[0].scrollIntoView()", elem)
                link = elem.get_attribute('href')
                video_urls.append(link)
                idx = idx + 1
            except:
                #All links are fetched. Scroll back to top.
                j = False
                driver.execute_script("window.scrollTo(0, 0);")
                continue
    else:
        multiple_videos = False
        video_urls = [video_url] #Make a list with a single element.
    
    for url in video_urls:
        #Loop over the videos to be downloaded.
        if multiple_videos: driver.get(url) #otherwise, we're already on that page.
        
        driver.switch_to.frame(driver.find_element_by_css_selector('#kplayer_ifp'))
        # Get the script
        script = driver.find_element_by_css_selector('body script:nth-child(2)').get_attribute("innerHTML")
        data = (script.splitlines()[2])[37:-1]
        # Load the data into json format
        js = json.loads(data)
        dl_link = js["entryResult"]["meta"]["downloadUrl"]
        title = js["entryResult"]["meta"]["name"]
    # Download video
        ydl_opts = {"outtmpl": title + ".mp4"}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([dl_link])


main()
