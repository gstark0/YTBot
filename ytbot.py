from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent
from argparse import ArgumentParser
import time
import os


ua = UserAgent()

class WebBrowser():
    def __init__(self, use_tor):
        
        # Generate random user agent
        self.chrome_options = Options()
        self.chrome_options.add_argument(f'user-agent={ua.random}')

        if use_tor:
            # Change TOR node
            with Controller.from_port(port = 9151) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
            
            # Use TOR proxy server (TOR must be running)
            self.chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
        else:
            self.chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
    
    def open(self, url):
        self.driver = webdriver.Chrome(executable_path='./chromedriver', options=self.chrome_options)
        self.driver.get(url)

        # Sometimes video doesn't load itself so click on it twice
        # Catch exceptions just in case youtube video didn't load properly
        try:
            player = self.driver.find_element_by_id('player')
            player.click()
            player.click()
        except:
            pass

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument('--tor', help='Whether to use tor proxy', action='store_true')
    args.add_argument('--url', help='URL to a YouTube video', required=True)
    args.add_argument('--views', help='How many views for a video', default=50, type=int)
    args.add_argument('--delay', help='Time to wait before the browser is closed, starts counting after all windows are loaded', default=10, type=int)
    args.add_argument('--windows', help='How many windows are opened at once', default=2, type=int)

    args = args.parse_args()
    
    use_tor = args.tor
    # Do some calculations to get expected views using specified number of windows opened at once
    for i in range(int(args.views / args.windows)):

        # Open all the browsers and load youtube videos
        browsers = []
        for j in range(args.windows):
            browsers.append(WebBrowser(use_tor))
            browsers[j].open(args.url)

        time.sleep(args.delay)

        # Close all the browsers
        for b in browsers:
            b.close()