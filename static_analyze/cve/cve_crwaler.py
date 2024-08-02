import requests
from bs4 import BeautifulSoup
import pandas as pd


class CVECrawler:
    def __init__(self, keyword_list):
        self.keyword_list = keyword_list
        self.url_templete = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="

    def get_url(self, keyword):
        return self.url_templete + keyword

    def get_html(self, url):
        content = requests.get(url).text
        html = BeautifulSoup(content, "html.parser")
        return html

    def get_cve_list(self, html):
        cve_list = []
        for link in html.find_all("a"):
            if "/cgi-bin/cvename.cgi?" in link.get("href"):
                cve_id = link.get("href").split("=")[1]
                cve_desc = link.find_next("td")
                cve_list.append({"id": cve_id, "desc": cve_desc.text})
        return cve_list

    def add2df(self, df, cve_list, url, keyword):
        for cve in cve_list:
            if cve["id"] in df["cve_id"]:
                loc = df["cve_id"].index(cve["id"])
                df["keyword"][loc] += f",{keyword}"
                continue
            df["cve_id"].append(cve["id"])
            df["cve_desc"].append(cve["desc"])
            df["url"].append(url)
            df["keyword"].append(keyword)

        return df

    def run(self):
        df = {"keyword": [], "cve_id": [], "cve_desc": [], "url": []}
        amount = len(self.keyword_list)
        for cnt, keyword in enumerate(self.keyword_list):
            url = self.get_url(keyword)
            html = self.get_html(url)
            cve_list = self.get_cve_list(html)
            df = self.add2df(df, cve_list, url, keyword)
            print(f"[progress] {cnt+1}/{amount}")
        df = pd.DataFrame(df)
        cve_name = "cves.csv"
        df.to_csv(cve_name, index=False)


if __name__ == "__main__":
    keyword_list = ["android+lite", "android+lite+application"]
    crawler = CVECrawler(keyword_list)
    crawler.run()
