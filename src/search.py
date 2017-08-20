import urllib.request
from bs4 import BeautifulSoup
import sys
import argparse
import time
from colorama import Fore


def usage():
    print("""
        When you are trying to find package in all repository of any user
        ,you have to write --repo-name and --query exactly
    """)
def helper(arguments):
    parser = argparse.ArgumentParser(description = "Repo Finder")
    parser.add_argument("--repo-user",dest="repo_user",help="Set Repo User")
    parser.add_argument("--query",dest="query",help="Search Query")
    parser.add_argument("--only-has-name",dest="only_has_name_boolean",help="While searching package,shows only urls that has query without contents query")
    parser.add_argument("--log",dest="log_file",help="Write all events to log file")

    results = parser.parse_args()
    return results



def repo_tester(html_data):
    soup = BeautifulSoup(html_data,"html.parser")
    tag = soup.find(itemprop = "name codeRepository")
    if tag == None:
        return False
    return True
def search_repositories(urls,query,username,only_has_name_boolean,http_errors_list,log_file):
    #https://github.com/pisilinux/main/search?utf8=✓&q=hello&type=
    #/pisilinux/main
    fp = None
    if log_file != None :
        fp = open(log_file,"w")
    repo_urls = urls
    http_errors_list = list()
    for url in repo_urls:
        print("https://github.com"+url+"/search?q="+query)
        html_data = ""
        try:
            html_data = urllib.request.urlopen("https://github.com"+url+"/search?q="+query).read()
        except urllib.error.HTTPError:
            print("HttpError,Waiting for some seconds")
            time.sleep(10)
            print("Continue")
            http_errors_list.append(url)
            pass



        soup = BeautifulSoup(html_data,"html.parser")
        datetimes = soup.find_all("relative-time")
        search_results = soup.find_all("a")

        counter = 0
        for link in search_results:
        
            try:
                l = link.get("href")
                if l[0] == "/":
                    #Sadece linkin icinde query varsa yazdir
                    #diger durumda content icinde query geciyorsa da yazdir
                    if only_has_name_boolean == "1":
                        if query  in l:
                            print(l)
                    else:
                        print(l)


                    if log_file != None :
                        fp.write(l)
                    print(Fore.WHITE)

            except IndexError:
                print("GEC")


    if log_file != None:
        fp.close()
    return http_errors_list



parser = helper(sys.argv)

username = parser.repo_user
query = parser.query
only_has_name_boolean = parser.only_has_name_boolean
log_file = parser.log_file
if query == None or username == None:
    usage()
    sys.exit()

pages = 1

html_datas_for_pages = list()
repo_urls = list()
http_errors_list = list()



print("Searching Repositories")
#https://github.com/pisilinux?page=1
while True:
    html_data = ""
    time.sleep(10)
    try:

        html_data = urllib.request.urlopen("https://github.com/"+username+"?page="+str(pages) + "&tab=repositories").read()
    except ConnectionResetError:
        print("ConnectionResetError")
        print("Trying Again")
        html_data = urllib.request.urlopen("https://github.com/"+username+"?page="+str(pages) + "&tab=repositories").read()
    if repo_tester(html_data) == False:
        break
    html_datas_for_pages.append(html_data)
    pages+=1



if len(html_datas_for_pages) != 0:
    print("Found Repositories")
    for html_data in html_datas_for_pages:
        soup = BeautifulSoup(html_data,"html.parser")
        for url in soup.find_all(itemprop = "name codeRepository"):
            repo_urls.append(url.get("href"))


    if len(repo_urls) != 0:
        print("Found URLS")
        http_errors_list = search_repositories(repo_urls,query,username,only_has_name_boolean,http_errors_list,log_file)
        print("DONE")
        if len(http_errors_list) !=0:
            print(Fore.GREEN+"Trying For given  Http Error urls")
            print(Fore.WHITE)
            search_repositories(http_errors_list,query,username,only_has_name_boolean,http_errors_list,log_file)
    else:
        print("Not Found Any URL")
else:
    print("Not Found Any Repository")
