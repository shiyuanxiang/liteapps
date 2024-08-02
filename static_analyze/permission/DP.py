import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_html(url):
    content = requests.get(url).text
    html = BeautifulSoup(content, "html.parser")
    return html


def search_cve(html):
    cve_list = []
    for link in html.find_all("a"):
        if "/cgi-bin/cvename.cgi?" in link.get("href"):
            cve_id = link.get("href").split("=")[1]
            cve_desc = link.find_next("td")
            cve_list.append({"id": cve_id, "desc": cve_desc.text})
    return cve_list


def add2df(df, permission, cve_list, url):
    for cve in cve_list:
        if cve["id"] in df["cve_id"]:
            continue
        df["permission"].append(permission)
        df["cve_id"].append(cve["id"])
        df["cve_desc"].append(cve["desc"])
        df["url"].append(url)
    return df


def main():
    url_templete = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="
    df = {"permission": [], "cve_id": [], "cve_desc": [], "url": []}
    cnt = 0
    amount = 0
    with open("./dangerous_permissions", "r") as fr:
        amount = len(fr.readlines())
    with open("./dangerous_permissions", "r") as fr:
        for line in fr.readlines():
            permission = line.strip()
            if permission != "CAMERA":
                url = url_templete + permission
                html = get_html(url)
                cve_list = search_cve(html)
                df = add2df(df, permission, cve_list, url)

            url = url_templete + "android.permission." + permission
            html = get_html(url)
            cve_list = search_cve(html)
            df = add2df(df, permission, cve_list, url)

            cnt += 1
            print(f"[progress] {cnt}/{amount}")
    print("[total cve] ", len(df["cve_id"]))
    df = pd.DataFrame(df)
    df.to_csv("cve_list_result.csv", index=False)


if __name__ == "__main__":
    main()


# UNP: unneccessary permission
# GED: Get Extra Data that not suppose to get by the permission, like log file
