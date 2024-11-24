from fastapi import APIRouter, Query, HTTPException
from bs4 import BeautifulSoup
import requests
from dependencies.utils import getArticlesData, getTotalPages, BASE_URL

router = APIRouter()


@router.get("/actor/{actor}")
def read_actor_page(page: int = Query(1), actor: str = None):
    response = requests.get(
        BASE_URL + (f"/actor/{actor}") + (f"/page/{page}" if page > 1 else "")
    )
    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.find("main", id="main")
    if (
        main.find("h1", text="Nothing Found")
        or main.find("section", class_="error-404")
        or main.find("section", class_="not-found")
    ):
        raise HTTPException(status_code=404, detail="Page not found")
    articleData = getArticlesData(main)
    return {
        "currentPage": page,
        "totalPages": getTotalPages(main),
        "totalResults": len(articleData),
        "data": articleData,
    }
