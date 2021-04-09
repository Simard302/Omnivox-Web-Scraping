from config import config as ConfigDict
import requests

def doRequest(config, cookies, response):
    location = response.headers.get('Location')
    print(response.status_code)
    print(response.url)
    cookies.update(response.cookies)
    if location :
        baseURL = ""
        if config["https_ovxUrl"] in response.url:
           baseURL = config["https_ovxUrl"]
        elif config["https_ovxUrl2"] in response.url:
            baseURL = config["https_ovxUrl2"]
        if not config["https_ovxUrl"] in location and not config["https_ovxUrl2"] in location:
            location = baseURL+location

        page = doRequest(config, cookies, requests.get(
            url=location,
            headers=config["headers"],
            cookies=cookies,
            allow_redirects=False
        ))
        return page
    else :
        return response