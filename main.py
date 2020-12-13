from urllib.request import urlopen as uOpen
from urllib.request import Request as uReq
from urllib.request import build_opener as bOpener
from urllib.request import HTTPCookieProcessor as httpCP
from urllib.request import install_opener as install_opener
from urllib.parse import urlencode as uEncode
import http.cookiejar
from bs4 import BeautifulSoup as soup
import userInfo


# Opens connection, saves page, closes
ovxUrl = "johnabbott.omnivox.ca/"
https_ovxUrl = "https://"+ovxUrl
ovxLoginUrl = https_ovxUrl + "/login"
userInfo = {
    'username': userInfo.username,
    'password': userInfo.password
}
check_string = "Quit"
headers={"Content-Type":"text/html",
"User-agent":"Mozilla/5.0 Chrome/81.0.4044.92",    # Chrome 80+ as per web search
"Host":ovxUrl,
"Origin":https_ovxUrl,
"Referer":https_ovxUrl}

cookie_jar = http.cookiejar.CookieJar()
opener = bOpener(httpCP(cookie_jar))
install_opener(opener)

# Getting login page and parsing the HTML
request = uReq(https_ovxUrl)
response = uOpen(request)
contents = response.read()

# Getting the token
html = contents.decode("utf-8")
mark_start = '<input id="k" name="k" type="hidden" value="'
mark_end = '">'
start_index = html.find(mark_start) + len(mark_start)
end_index = html.find(mark_end, start_index)
token = html[start_index:end_index]

# Making payload
payload = {
    "k":token,
    "TypeLogin":"PostSolutionLogin",
    "TypeIdentification":"Etudiant",
    "StatsEnvUsersNbCouleurs":"24",
    "StatsEnvUsersResolution":"767",
    "NoDA":userInfo['username'],
    "PasswordEtu":userInfo['password']
}
data = uEncode(payload)
binary_data = data.encode("UTF-8")

# Requesting page
request = uReq(ovxLoginUrl, binary_data, headers)
response = uOpen(request)
contents = response.read()

contents = contents.decode("utf-8")
index = contents.find(check_string)
if index != -1:
    print('we found it')
else:
    print('we messed up')