import requests
from bs4 import BeautifulSoup
import os 
import re

def download_file(url):
    # Create target Directory if don't exist
    dirName = 'resources'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists")
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open("resources/"+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

def dnsdumpster(domain):
    
    r = requests.get('https://dnsdumpster.com/')
    csrftoken = r.cookies['csrftoken']
    excel_filename = ''
    s = BeautifulSoup(r.text,'lxml')
    csrf_token=s.find("input",{"name":"csrfmiddlewaretoken"})['value']
    cookies = {'csrftoken':csrf_token}
    referer = {'Referer':'https://dnsdumpster.com'}
    data = {'csrfmiddlewaretoken':csrf_token,'targetip':domain,'user':'free'}
    response = requests.post('https://dnsdumpster.com/', data=data, cookies=cookies,headers=referer)
    soup = BeautifulSoup(response.text,'lxml')
    info = [a['href'] for a in soup.find_all('a', href=True)]
    for i in info:
        if 'xls' in i or 'graph' in i:
            local_filename = download_file('https://dnsdumpster.com/%s' % (i))
            if 'html' in local_filename:
                #we have to edit the dnsdumpster html file in order to view the graph.
                f = open("resources/"+local_filename, "r")
                s = re.sub('/static/','https://dnsdumpster.com/static/',f.read())
                x = open("resources/new_"+local_filename, "w")
                x.write(s)
                f.close()
                os.remove("resources/"+local_filename)
                x.close()
            else:
                excel_filename = local_filename
    return excel_filename

def main():

    dnsdumpster(input('Domain to run ?\n'))


main()
