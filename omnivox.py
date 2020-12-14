import requests
from requests.cookies import RequestsCookieJar
from pyquery import PyQuery as pq
import asyncio

# Basically a config specific to Omnivox
ovxUrl = "johnabbott.omnivox.ca"
https_ovxUrl = "https://"+ovxUrl
https_ovxUrl2 = "https://www-jac-ovx.omnivox.ca"
ovxLoginUrl = https_ovxUrl + "/intr/Module/Identification/Login/Login.aspx?ReturnUrl=/intr"
headers={
    "User-Agent": "Mozilla/5.0"
}

class LeaSession:
    def __init__(self, session, lea_html:str):
        self.cookies = RequestsCookieJar()
        self.cookies.update(session.cookies)
        self.lea_html = lea_html
        self.lea_html_query = pq(lea_html)


    def getAssignments(self):
        assignmentURL = self.lea_html_query('a[id="lienDTRV"]').attr("href")
        assignmentsPage = requests.get(
            url= https_ovxUrl2+assignmentURL,
            headers=headers,
            cookies=self.cookies,
            allow_redirects=False
        )
        self.cookies.update(assignmentsPage.cookies)
        print(self.cookies)
        print(assignmentsPage.status_code)

        """d = pq(assignmentsPage.text)
        assignmentsHTML = d('tr[class="LigneListTrav1"]')
        print(assignmentsPage.text)"""

        """assignmentDict = {}
        for tab in assignmentsHTML :
            name = tab('a[class="RemTrav_Sommaire_NomCours"]').text
            listAssignmentsOfClassHTML = tab('span[class="RemTrav_Sommaire_ProchainsTravaux"]')
            listAssignmentsOfClass = []
            for assignment in listAssignmentsOfClassHTML :
                listAssignmentsOfClass.append(assignment.text)
            assignmentDict[name] = listAssignmentsOfClass
        #print(assignmentDict)"""

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
        self.cookies.update(lea_page.cookies)
        print(self.cookies)
        print(lea_page.status_code)
        return lea_page

    def startLeaSession(self):
        lea_page = self.getLeaPage()
        return LeaSession(
            self,
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
    print(cookies)

    homepage_response = requests.post(
        url=https_ovxUrl + "/intr/",
        headers=headers,
        cookies=cookies,
        allow_redirects=False
    )
    cookies.update(homepage_response.cookies)
    print(cookies)

    return OmnivoxSession(
        cookies=cookies,
        homepage_html=homepage_response.text
    )