from fastapi import APIRouter, Query, HTTPException
from bs4 import BeautifulSoup
import requests
from dependencies.utils import getArticlesData, getTotalPages, BASE_URL

router = APIRouter()


@router.get("/homepage")
def read_homepage(page: int = Query(1)):
    try:
        response = requests.get(BASE_URL + (f"/page/{page}" if page > 1 else ""))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        main = soup.find("main", id="main")
        if not main:
            raise HTTPException(status_code=404, detail="No main element found on page")
        print("llll")
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
