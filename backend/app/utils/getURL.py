from app.core.config import settings


async def getURL(url):
    return settings.API_V1_STR + url
