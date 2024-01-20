# importing the modules
import ipaddress
import re
import urllib.request
from urllib.parse import urlparse, urlsplit
import googlesearch
import whois
import requests
from datetime import date
from bs4 import BeautifulSoup


class Features:
    x = []

    def __init__(self, url) -> None:
        self.x = []
        self.url = url
        self.domain = ""
        self.urlparse = ""
        self.whoisResponse = ""
        self.soup = ""

        try:
            self.urlparse = urlparse(url)
            self.domain = self.urlparse.netloc
        except Exception as e:
            print(f"Error {e}")

        try:
            self.response = requests.get(url)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except Exception as e:
            print(f"Error {e}")

        try:
            self.whoisResponse = whois.whois(self.domain)
        except Exception as e:
            print(f"Error {e}")

    # 1. finding IP
    def findIP(self):
        try:
            ip = ipaddress.ip_address(self.url)
            if ip:
                return -1
            return 1
        except Exception as e:
            print(f"Error (findIP): {e}")
            return 1

    # 2. length of url
    def lengthOfURL(self):
        try:
            if len(self.url) < 54:
                return 1
            elif 54 < len(self.url) < 75:
                return 0
        except Exception as e:
            print(f"Error (length of URL): {e}")
            return -1

    # 3. short URL
    def shortURL(self):
        match = r"\b(?:bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net)"
        if re.match(match, self.url):
            print("matches")
            return -1
        return 1

    # 4. finding @ symbol
    def findAtSymbol(self):
        if '@' in str(self.url):
            return -1
        return 1

    # 5. finding the redirection
    def findRedirection(self):
        try:
            redirection = requests.get(self.url, allow_redirects=False)
            if redirection.status_code in (301, 302, 303, 307, 308):
                return -1
            else:
                return 1
        except Exception as e:
            print(f"Error (redirection): {e}")
            return -1

    # 6. finding the prefix and suffix
    def PrefixSuffix(self):
        try:
            if '-' in str(self.domain):
                return -1
            return 1
        except Exception as e:
            print(f"Error (prefixSuffix): {e}")
            return -1

    # 7. finding subdomain
    def subdomain(self):
        split_url = urlsplit(self.url)
        subdomain = split_url.netloc.split('.')
        if len(subdomain) > 2:
            return -1
        return 1

    # 8. finding HTTPS in URL
    def findHTTPS(self):
        try:
            https = self.urlparse.scheme
            print(https)
            if 'https' in https:
                return 1
            return -1
        except Exception as e:
            print(f"Error (findHTTPS): {e}")
            return 1

    # 9. finding the Domain Registered Date
    def domainRegDate(self):
        try:
            creation_date = self.whoisResponse.creation_date
            expiration_date = self.whoisResponse.expiration_date
            try:
                if (len(expiration_date)):
                    expiration_date = expiration_date[0]
            except:
                pass
            try:
                if (len(creation_date)):
                    creation_date = creation_date[0]
            except:
                pass

            age = (expiration_date.year - creation_date.year) * 12 + (expiration_date.month - creation_date.month)
            if age >= 12:
                return 1
            return -1
        except Exception as e:
            print(f"Error (domainRegData): {e}")
            return -1

    # 10. finding the Favicon
    def favicon(self):
        try:
            for head in self.soup.find_all('head'):
                for head.link in self.soup.find_all('link', href=True):
                    dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                    if self.url in head.link['href'] or len(dots) == 1 or self.domain in head.link['href']:
                        return 1
            return -1
        except Exception as e:
            print(f"Error (favicon): {e}")
            return -1

    # 11. non standard port
    def nonStdPort(self):
        try:
            port = self.domain.split(":")
            if len(port) > 1:
                return -1
            return 1
        except Exception as e:
            print(f"Error (non std port): {e}")
            return -1

    # 12. finding https domain in URL
    def httpsDomainUrl(self):
        try:
            if 'https' in self.domain:
                return -1
            return 1
        except Exception as e:
            print(f"Error (https domain): {e}")
            return -1

    # 13. requesting the URL
    def requestURL(self):
        try:
            success, i = 0, 0
            for img in self.soup.find_all('img', src=True):
                dots = [x.start(0) for x in re.finditer('\.', img['src'])]
                if self.url in img['src'] or self.domain in img['src'] or len(dots) == 1:
                    success = success + 1
                i += 1

            for audio in self.soup.find_all('audio', src=True):
                dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
                if self.url in audio['src'] or self.domain in audio['src'] or len(dots) == 1:
                    success = success + 1
                i += 1

            for embed in self.soup.find_all('embed', src=True):
                dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
                if self.url in embed['src'] or self.domain in embed['src'] or len(dots) == 1:
                    success = success + 1
                i += 1

            for iframe in self.soup.find_all('iframe', src=True):
                dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
                if self.url in iframe['src'] or self.domain in iframe['src'] or len(dots) == 1:
                    success = success + 1
                i += 1

            try:
                percentage = success / float(i) * 100
                print(percentage)
                if percentage < 22.0:
                    return 1
                elif ((percentage >= 22.0) and (percentage < 61.0)):
                    return 0
                else:
                    return -1
            except Exception as e:
                print(e)
                return 0
        except Exception as e:
            print(f"Error (request url): {e}")
            return -1

    # 14. anchor URL
    def anchorURL(self):
        try:
            unsafe = i = 0
            for a in self.soup.find_all('a', href=True):
                if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (
                        self.url in a['href'] or self.domain in a['href']):
                    unsafe += 1
                i += 1

            try:
                percentage = unsafe / float(i) * 100
                if percentage < 31.0:
                    return 1
                elif (percentage >= 31.0) and (percentage < 67.0):
                    return 0
                else:
                    return -1
            except Exception as e:
                print(f"Error (anchorURL): {e}")
                return -1

        except Exception as e:
            print(f"Error (anchorURL): {e}")
            return -1

    # 15. link in script tags
    def linkInScriptTags(self):
        try:
            i, success = 0, 0

            for link in self.soup.find_all('link', href=True):
                dots = [x.start(0) for x in re.finditer('\.', link['href'])]
                if self.url in link['href'] or self.domain in link['href'] or len(dots) == 1:
                    success = success + 1
                i = i + 1

            for script in self.soup.find_all('script', src=True):
                dots = [x.start(0) for x in re.finditer('\.', script['src'])]
                if self.url in script['src'] or self.domain in script['src'] or len(dots) == 1:
                    success = success + 1
                i = i + 1

            try:
                percentage = success / float(i) * 100
                if percentage < 17.0:
                    return 1
                elif ((percentage >= 17.0) and (percentage < 81.0)):
                    return 0
                else:
                    return -1
            except Exception as e:
                print(e)
                return 0
        except Exception as e:
            print(f"Error (link in script tags): {e}")
            return -1

    # 16. server for handler
    def serverForHandler(self):
        try:
            if len(self.soup.find_all('form', action=True)) == 0:
                return 1
            else:
                for form in self.soup.find_all('form', action=True):
                    if form['action'] == "" or form['action'] == "about:blank":
                        return -1
                    elif self.url not in form['action'] and self.domain not in form['action']:
                        return 0
                    else:
                        return 1
        except Exception as e:
            print(f"Error (server for handler): {e}")
            return -1

    # 17. info Email
    def infoEmail(self):
        try:
            if re.findall(r"[mail\(\)|mailto:?]", str(self.soup)):
                return -1
            else:
                return 1
        except Exception as e:
            print(f"Error (infoEmail): {e}")
            return -1

    # 18. Abnormal URL
    def abnormalURL(self):
        try:
            if self.response.text and self.whoisResponse:
                return 1
            else:
                return -1
        except Exception as e:
            print(f"Error (abnormal url): {e}")
            return -1

    # 19. website forwarding
    def websiteForwarding(self):
        try:
            if len(self.response.history) <= 1:
                return 1
            elif len(self.response.history) <= 4:
                return 0
            else:
                return -1
        except Exception as e:
            print(f"Error (websiteForwarding): {e}")
            return -1

    # 20. status bar cust
    def statusBarCust(self):
        try:
            if re.findall("<script>.+onmouseover.+</script>", self.response.text):
                return 1
            else:
                return -1
        except Exception as e:
            print(f"Error (status bar cust); {e}")
            return -1

    # 22. disable right click event
    def disabledRightClick(self):
        try:
            if re.findall(r"event.button ?== ?2", self.response.text):
                return 1
            else:
                return -1
        except Exception as e:
            print(f"Error (disabled Right click): {e}")
            return -1

    # 22. iframe redirection
    def iframeRedirection(self):
        try:
            if re.findall(r"[<iframe>|<frameBorder>]", self.response.text):
                return 1
            else:
                return -1
        except Exception as e:
            print(f"Error (iframe Redirection): {e}")
            return -1

    # 23. age of domain
    def ageOfDomain(self):
        try:
            creation_date = self.whoisResponse.creation_date
            today = date.today()
            age = (today.year - creation_date.year) * 12 + (today.month - creation_date.month)
            if age >= 6:
                return 1
            return -1
        except Exception as e:
            print(f"Error (Age of Domain): {e}")
            return -1

    # 24. finding the popup window
    def findPopupWindow(self):
        try:
            if re.findall(r"alert\(", self.response.text):
                return 1
            else:
                return -1
        except Exception as e:
            print(f"Error (find popup window): {e}")
            return -1

    # 25. Enumerating the DNS records
    def enumDNSRecords(self):
        try:
            creation_date = self.whoisResponse.creation_date
            today = date.today()
            age = (today.year - creation_date.year) * 12 + (today.month - creation_date.month)
            if age >= 6:
                return 1
            return -1
        except Exception as e:
            print(f"2. Error (enum DNS Records): {e}")
            return -1

    # 26. website traffix
    def websiteTraffic(self):
        try:
            rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + self.url).read(),"xml").find("REACH")['RANK']
            if int(rank) < 100000:
                return 1
            return 0
        except Exception as e:
            print(f"Error (website Traffic): {e}")
            return -1

    # 27. page rank
    def pageRank(self):
        try:
            rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {"name": self.domain})

            global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
            if global_rank > 0 and global_rank < 100000:
                return 1
            return -1
        except Exception as e:
            print(f"Error (page rank): {e}")
            return -1

    # 28. google index
    def googleIndex(self):
        try:
            site = googlesearch.search(self.url, num_results=1)
            if site:
                return 1
            else:
                return -1
        except Exception as e:
            print(f"Error (google index): {e}")
            return -1

    # 29. link pointing to page
    def linkPointToPage(self):
        try:
            number_of_links = len(re.findall(r"<a href=", self.response.text))
            if number_of_links <= 5:
                return 0
            else:
                return 1
        except Exception as e:
            print(f"Error (Link to page): {e} ")
            return -1

    # 30. stats report
    def statReport(self):
        try:
            url_match = re.search(
                'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',
                self.url)
            ip_address = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            ip_match = re.findall(ip_address, self.domain)
            if url_match:
                return -1
            elif ip_match:
                return -1
            return 1
        except Exception as e:
            print(f"Error (Stat Report): {e}")
            return -1

    def get_features(self):
        self.x.append(self.findIP())
        self.x.append(self.lengthOfURL())
        self.x.append(self.shortURL())
        self.x.append(self.findAtSymbol())
        self.x.append(self.findRedirection())
        self.x.append(self.PrefixSuffix())
        self.x.append(self.subdomain())
        self.x.append(self.findHTTPS())
        self.x.append(self.domainRegDate())
        self.x.append(self.favicon())
        self.x.append(self.nonStdPort())
        self.x.append(self.httpsDomainUrl())
        self.x.append(self.requestURL())
        self.x.append(self.anchorURL())
        self.x.append(self.linkInScriptTags())
        self.x.append(self.serverForHandler())
        self.x.append(self.infoEmail())
        self.x.append(self.abnormalURL())
        self.x.append(self.websiteForwarding())
        self.x.append(self.statusBarCust())
        self.x.append(self.disabledRightClick())
        self.x.append(self.findPopupWindow())
        self.x.append(self.iframeRedirection())
        self.x.append(self.ageOfDomain())
        self.x.append(self.enumDNSRecords())
        # self.x.append(self.websiteTraffic())
        self.x.append(self.pageRank())
        self.x.append(self.googleIndex())
        self.x.append(self.linkPointToPage())
        self.x.append(self.statReport())

        return self.x