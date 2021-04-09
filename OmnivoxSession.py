import requests
from pyquery import PyQuery as pq
from config import config as ConfigDict
from LeaSession import LeaSession
from util import doRequest

class OmnivoxSession:
    def __init__ (self, school: str, username: str, password : str):
        self.cfg = ConfigDict[school]
        self.username = username
        self.password = password

    async def login(self):
        username = self.username
        password = self.password

        login_page = requests.get(
            url= self.cfg["https_ovxUrl"] + "/intr/Module/Identification/Login/Login.aspx?ReturnUrl=/intr",
            headers= self.cfg["headers"],
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
            url=self.cfg["ovxLoginUrl"],
            data=payload,
            headers=self.cfg["headers"],
            cookies=login_page.cookies,
            allow_redirects=False
        )
        if login_post_response.status_code != 302:
            return None

        cookies = login_page.cookies
        cookies.update(login_post_response.cookies)

        homepage_response = requests.post(
            url=self.cfg["https_ovxUrl"] + "/intr/",
            headers=self.cfg["headers"],
            cookies=cookies,
            allow_redirects=False
        )
        homepage_response = doRequest(self.cfg, homepage_response.cookies, homepage_response)
        cookies.update(homepage_response.cookies)

        self.cookies = cookies
        self.homepage_html = homepage_response.text
        self.homepage_html_query = pq(homepage_response.text)

        return self

    def getLeaPage(self):
        leaURL = self.homepage_html_query('a[class="raccourci id-service_CVIE   code-groupe_lea"]').attr("href")
        lea_page = doRequest(self.cfg, self.cookies, requests.get(
            url= self.cfg["https_ovxUrl"]+leaURL,
            headers= self.cfg["headers"],
            cookies=self.cookies,
            allow_redirects=False
        ))
        self.cookies.update(lea_page.cookies)
        return lea_page

    def startLeaSession(self):
        lea_page = self.getLeaPage()
        return LeaSession(
            self,
            self.cfg,
            lea_html=lea_page.text
        )


    def getClassNameList(self):
        lea_page = self.getLeaPage()
        d = pq(lea_page.text)
        classesHTML = d('div[class="card-panel-title"]')
        classes = []
        for classLine in classesHTML:
            classes.append(classLine.text)
        return classes