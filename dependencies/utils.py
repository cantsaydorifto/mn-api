import re
from sec.vals import base_uri

BASE_URL = base_uri


def getTotalPages(main):
    pagination_div = main.find("div", class_="pagination") if main else None
    if not pagination_div:
        return 1
    paginationDivs = pagination_div.find_all("a")
    if len(paginationDivs) <= 1:
        return 1
    url = paginationDivs[-1]
    if "href" in url.attrs:
        return int(re.search(r"\d+", url["href"]).group())
    if paginationDivs[-2].text != "Last":
        firstOccurence = re.search(r"\d+", paginationDivs[-2].text)
        return (int(firstOccurence.group()) + 1) if firstOccurence else 1
    return 1


def getArticlesData(main):
    articles = main.find_all("article") if main else []
    articles_data = []
    for article in articles:
        entryArticle = article.find("header", class_="entry-header")
        articleText = entryArticle.find("span") if entryArticle else None
        title = articleText.text if articleText else ""

        url = article.find("a")["href"] if article.find("a") else "No URL"

        img_tag = article.find("img")
        img_src = (
            img_tag["data-src"]
            if img_tag and "data-src" in img_tag.attrs
            else "No Image"
        )

        duration_tag = article.find("span", class_="duration")
        duration = (
            duration_tag.text.strip().split()[-1] if duration_tag else "No Duration"
        )

        hd_tag = article.find("span", class_="hd-video")
        hd = bool(hd_tag)

        articles_data.append(
            {
                "title": title,
                "url": url,
                "imgSrc": img_src,
                "duration": duration,
                "hd": hd,
            }
        )
    return articles_data
