import glob
import os
from bs4 import BeautifulSoup
import requests
import csv

# app.buzz.share.lite
url_templete = "https://play.google.com/store/apps/details?id=xxx&hl=en-SG"


def fetch_url(url=None):
    if url is None:
        return None
    response = requests.get(url=url)
    try:
        code = response.status_code  # Check if the request was successful
    except requests.exceptions.HTTPError as e:
        code = response.status_code
    return code, response.text


def parse_html(html=None):
    if html is None:
        return None
    print(f"parse_html: {html}")
    review = ""
    with open(html, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    elements = soup.select(".EGFGHd .h3YV2d")
    for element in elements:
        review += element.text
        review += "\n\n"
    app_name = soup.find("h1", itemprop="name").text
    # app_name = soup.find("h1", class_="Fd93Bb ynrBgc xwcR9d").text
    # if app_name == "":
    #     app_name = soup.find("h1", itemprop="name").text
    return app_name, review


def csv_to_txt():
    with open("reviews.txt", "w") as fw:
        with open("reviews.csv", "r") as fr:
            reader = csv.DictReader(fr)
            for row in reader:
                app_name = row["app_name"]
                review = row["review"]
                fw.write(f"App Name: {app_name}\n")
                fw.write(f"Review: {review}\n\n")


def anayze(csv_file):
    keywords = {
        "ads": ["ads", "advertisements", "too many ads"],
        "permission": ["permission", "permissions", "access denied", "grant access"],
        "runtime": ["runtime error", "runtime issue", "runtime problem"],
        "functionality": [
            "login",
            "log in",
            "sign in",
            "signing in",
            "connection",
            "connect",
            "disconnect",
            "connectivity",
            "functionality",
        ],
        "interface": ["interface", "UI", "user interface", "design"],
        "compatibility": ["compatibility", "compatible", "incompatible"],
        "performance": ["slow", "lag", "performance", "speed", "overhead", "overload"],
        "security": ["security", "secure", "insecure", "vulnerability", "privacy"],
        "memory": ["memory", "ram", "storage", "disk", "leak", "leaking", "leakage"],
        "stability": [
            "stability",
            "stable",
            "unstable",
            "crash",
            "crashing",
            "stops working",
            "stopped working",
            "timeout",
            "timed out",
            "time out",
        ],
    }
    # statistic
    keywords_cnt = {k: 0 for k in keywords}
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        for i in range(len(rows)):
            review = rows[i]["review"]
            for keyword in keywords:
                for k in keywords[keyword]:
                    if k in review:
                        keywords_cnt[keyword] += 1

        print("apps: ", len(rows))
    keywords_cnt = {
        k: v
        for k, v in sorted(keywords_cnt.items(), key=lambda item: item[1], reverse=True)
    }
    for k in keywords_cnt:
        print(f"{k}: {keywords_cnt[k]}")
    # complete problem field
    # with open(csv_file, "r") as f:
    #     reader = csv.DictReader(f)
    #     rows = list(reader)
    #     for i in range(len(rows)):
    #         review = rows[i]["review"]
    #         matching_keywords = []
    #         for keyword in keywords:
    #             for k in keywords[keyword]:
    #                 if k in review:
    #                     matching_keywords.append(keyword)
    #         rows[i]["problem"] = ", ".join(set(matching_keywords))

    # with open("reviews_analyzed.csv", "w") as f:
    #     fieldnames = ["app_name", "app_id", "review", "problem"]
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for row in rows:
    #         writer.writerow(row)


def main():
    # get html files
    # with open("urls.txt", "r") as f:
    #     for line in f.readlines():
    #         url = url_templete.replace("xxx", line.strip())
    #         html_code, html_text = fetch_url(url=url)
    #         print(f"URL: {url}, Status Code: {html_code}")
    #         if html_code == 200:
    #             with open(os.path.join("html", line.strip() + ".html"), "w") as fw:
    #                 fw.write(html_text)
    # parse html files
    # with open("reviews.csv", "w") as f:
    #     wt = csv.DictWriter(f, fieldnames=["app_name", "app_id", "review", "problem"])
    #     wt.writeheader()
    #     html_cnt = 0
    #     for html_path in glob.glob(os.path.join("html", "*.html")):
    #         app_name, review = parse_html(html=html_path)
    #         app_id = os.path.basename(html_path)[:-5]
    #         wt.writerow(
    #             {
    #                 "app_name": app_name,
    #                 "app_id": app_id,
    #                 "review": review,
    #                 "problem": "",
    #             }
    #         )
    #         html_cnt += 1

    #     print(f"Processed {html_cnt} html files")
    # csv_to_txt()
    anayze("reviews.csv")


if __name__ == "__main__":
    main()
