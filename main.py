import requests
from requests.cookies import RequestsCookieJar
from pyquery import PyQuery as pq
import asyncio
from bs4 import BeautifulSoup as soup
import userInfo

# Basically a config specific to Omnivox
ovxUrl = "johnabbott.omnivox.ca"
https_ovxUrl = "https://"+ovxUrl
ovxLoginUrl = https_ovxUrl + "/intr/Module/Identification/Login/Login.aspx?ReturnUrl=/intr"
userInfo = {
    'username': userInfo.username,
    'password': userInfo.password
}
check_string = "Quit"
headers={
    "User-Agent": "Mozilla/5.0"
}


class OmnivoxSession:
    def __init__ (self, cookies: RequestsCookieJar, homepage_html: str):
        self.cookies = cookies
        self.homepage_html = homepage_html
        self.homepage_html_query = pq(homepage_html)


    def getLeaPage(self):
        leaURL = self.homepage_html_query('a[class="raccourci id-service_CVIE   code-groupe_lea"]').attr("href")
        lea_page = requests.get(
            url=https_ovxUrl+leaURL,
            headers=headers,
            cookies=self.cookies,
            allow_redirects=True
        )
        return lea_page


    def getClassNameList(self):
        lea_page = self.getLeaPage()
        d = pq(lea_page.text)
        classesHTML = d('div[class="card-panel-title"]')
        classes = []
        for classLine in classesHTML:
            classes.append(classLine.text)
        return classes


async def login(username, password):
    login_page = requests.get(
        url=https_ovxUrl + "/intr/Module/Identification/Login/Login.aspx?ReturnUrl=/intr",
        headers=headers,
    )

    # Making payload
    d = pq(login_page.text)
    token = d("input[name='k']").attr("value")
    payload = {
        "NoDA": username,
        "PasswordEtu": password,
        "TypeIdentification": "Etudiant",
        "k": token
    }

    login_post_response = requests.post(
        url=ovxLoginUrl,
        data=payload,
        headers=headers,
        cookies=login_page.cookies,
        allow_redirects=False
    )
    if login_post_response.status_code != 302:
        return None

    cookies = login_page.cookies
    cookies.update(login_post_response.cookies)

    homepage_response = requests.post(
        url=https_ovxUrl + "/intr/",
        headers=headers,
        cookies=cookies,
        allow_redirects=True
    )
    cookies.update(homepage_response.cookies)

    return OmnivoxSession(
        cookies=cookies,
        homepage_html=homepage_response.text
    )


async def main():
    username = input("What is your Omnivox username: ")
    password = input("What is your Omnivox password: ")
    session = await login(username, password)
    if not session:
        return print('Login failed')

    print(session.getClassNameList())

asyncio.run(main())