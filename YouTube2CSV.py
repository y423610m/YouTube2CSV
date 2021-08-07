from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

#number番目までのsearchword検索結果のタイトル取得
class YouTube():
    def __init__(self, searchword, number = 10, _sort = "関連度"):
        self.word = searchword
        options = Options()
        #options.add_argument("--disable-gpu")
        browser = webdriver.Chrome("chromedriver.exe",options = options)
        #url = "https://www.youtube.com/"#default youtube
        url_cite = "https://www.youtube.com/results?search_query="
        sort = {"関連度":"&sp=CAASAhAB","アップロード日":"&sp=CAISAhAB","視聴回数":"&sp=CAMSAhAB","評価":"&sp=CAESAhAB"}#関連度,アップロード日,視聴回数,評価
        browser.get(url_cite+searchword+sort[_sort])

        videos = browser.find_elements_by_id("video-title")
        height = 0
        while len(videos) < number:
            browser.execute_script("window.scrollTo("+str(height)+","+ str(height+2000)+");")
            height = height + 2000
            sleep(2)
            videos = browser.find_elements_by_id("video-title")
        

        watched = browser.find_elements_by_id("metadata-line")
        channels = browser.find_elements_by_id("channel-info")

        self.titles = []
        self.urls = []
        self.watched = []
        self.channels = []
        cnt = 0
        for video in videos:
            self.titles.append( video.text )
            self.urls.append( video.get_attribute("href") )
            self.watched.append( watched[cnt].text.split(" ")[0] )
            self.channels.append( channels[cnt].text )
            cnt = cnt + 1
            if cnt > number:
                break
        #return titles,urls


    def save(self):
        filename = "YouTube_"+self.word+".csv"
        df = pd.DataFrame()
        df.to_csv(filename)
        df["タイトル"],df["URL"],df["視聴回数"],df["チャンネル"] = self.titles,self.urls,self.watched,self.channels
        """
        df["タイトル"] = self.titles
        df["URL"] = self.urls
        df["視聴回数"] = self.watched
        df["チャンネル"] = self.channels
        """
        with open(filename, mode="w", encoding="cp932", errors="ignore",newline = "") as f:
            df.to_csv(f)


if __name__ == "__main__":

    word = "Python入門"
    Ins = YouTube(word, 100, "視聴回数")
    Ins.save()

    print("finish")
    input()