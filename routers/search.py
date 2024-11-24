from fastapi import APIRouter, Query, HTTPException
from bs4 import BeautifulSoup
import requests
from dependencies.utils import getArticlesData, getTotalPages, BASE_URL

router = APIRouter()


@router.get("/search")
def search_data(q: str = Query(""), page: int = Query(1)):
    try:
        response = requests.get(
            BASE_URL + (f"/page/{page}" if page > 1 else "") + "/?s=" + q
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        main = soup.find("main", id="main")
        if not main:
            raise HTTPException(status_code=404, detail="No main element found on page")
        if (
            main.find("h1", text="Nothing found")
            or main.find("section", class_="error-404")
            or main.find("section", class_="not-found")
        ):
            raise HTTPException(status_code=404, detail="No results found")
        articleData = getArticlesData(main)
        return {
            "currentPage": page,
            "totalPages": getTotalPages(main),
            "totalResults": len(articleData),
            "data": articleData,
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {str(e)}")
