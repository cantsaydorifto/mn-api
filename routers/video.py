from fastapi import APIRouter, Query, HTTPException
from bs4 import BeautifulSoup
import requests
from dependencies.utils import BASE_URL

router = APIRouter()


class Actor:
    def __init__(self, name, tag):
        self.name = name
        self.tag = tag

    def __str__(self):
        return {"name": self.name, "tag": self.tag}


class Video:
    def __init__(self):
        self.title: str = ""
        self.thumbnail: str = ""
        self.url: str = ""
        self.date: str = ""
        self.actor: list[Actor] = []

    def __str__(self):
        return {
            "title": self.title,
            "thumbnail": self.thumbnail,
            "url": self.url,
            "date": self.date,
            "actor": [str(i) for i in self.actor],
        }


@router.get("/video/{video_name}")
def read_actor_page(video_name: str = None):
    try:
        response = requests.get(f"{BASE_URL}/{video_name}/")
        response.raise_for_status()
        vid = Video()
        soup = BeautifulSoup(response.text, "html.parser")
        meta_tag_thumbnail = soup.find("meta", itemprop="thumbnailUrl")
        meta_tag = soup.find("meta", itemprop="contentURL")
        heading = soup.find("h1", class_="entry-title")
        videoDate = soup.find("div", id="video-date")
        videoActor = soup.find("div", id="video-actors")
        vid.thumbnail = (
            ""
            if not meta_tag_thumbnail or not meta_tag_thumbnail.get("content")
            else meta_tag_thumbnail.get("content")
        )
        vid.url = (
            ""
            if not meta_tag or not meta_tag.get("content")
            else meta_tag.get("content")
        )
        vid.title = "" if not heading else heading.text
        vid.date = (
            ""
            if not videoDate
            else videoDate.text.replace("\n", "")
            .replace("\t", "")
            .replace("Date:", "")
            .strip()
        )
        vidActorsAnchorTag = [] if not videoActor else videoActor.findAll("a")
        for i in vidActorsAnchorTag:
            vid.actor.append(Actor(i.text, "" if "href" not in i.attrs else i["href"]))
        return {"video": vid}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {str(e)}")
