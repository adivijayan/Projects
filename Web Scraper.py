import requests
from bs4 import BeautifulSoup

res = requests.get("https://news.ycombinator.com/news")
soup = BeautifulSoup(res.text, "html.parser")

# Filter out <a> tags inside .titleline that do NOT have a <span> inside
clean_links = [a for a in soup.select(".titleline a") if not a.find("span")]
votes = soup.select(".score")
subtext = soup.select(".subtext")


def create_custom_news(links, votes):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get("href")
        vote = subtext[idx].select(".score")
        if len(vote):
            points = int(votes[idx].getText().replace(" points", ""))
            hn.append({"title": title, "link:": href, "points:": points})
    return hn


custom_news = create_custom_news(clean_links, votes)
for item in custom_news:
    print(item)
