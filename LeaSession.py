import requests
from requests.cookies import RequestsCookieJar
from pyquery import PyQuery as pq
from config import config as ConfigDict
from util import doRequest

class LeaSession:
    def __init__(self, session, config : ConfigDict, lea_html:str):
        self.cfg = config
        self.cookies = RequestsCookieJar()
        self.cookies.update(session.cookies)
        self.lea_html = lea_html
        self.lea_html_query = pq(lea_html)


    def getAssignments(self):
        assignmentURL = self.lea_html_query('a[id="lienDTRV"]').attr("href")

        assignmentsPage = doRequest(self.cfg, self.cookies, requests.get(
            url= self.cfg["https_ovxUrl2"]+assignmentURL,
            headers=self.cfg["headers"],
            cookies=self.cookies,
            allow_redirects=True
        ))
        self.cookies.update(assignmentsPage.cookies)

        d = pq(assignmentsPage.text)
        assignmentDict = {}
        for i in range(1, 3):
            d = pq(assignmentsPage.text)
            assignmentsHTML = d('tr[class="LigneListTrav'+str(i)+'"]')
            for tab in assignmentsHTML :
                d = pq(tab)
                name = d('a[class="RemTrav_Sommaire_NomCours"]')[0].text.strip()
                listAssignmentsOfClassHTML = d('a[class="RemTrav_Sommaire_ProchainsTravaux"]')
                listAssignmentsDescOfClassHTML = d('span[class="RemTrav_Sommaire_ProchainsTravauxDesc"]')
                listAssignmentsOfClass = {}
                for assignment in listAssignmentsOfClassHTML :
                    listAssignmentsOfClass[assignment.text.strip()] = listAssignmentsDescOfClassHTML[listAssignmentsOfClassHTML.index(assignment)].text.replace('\n', '').replace('\r', '').replace(' ', '').replace('\xa0', ' ')
                assignmentDict[name] = listAssignmentsOfClass
        print(assignmentDict)