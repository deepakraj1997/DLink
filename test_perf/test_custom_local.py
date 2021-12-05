import requests
import threading

def miniworker():
    url = "http://127.0.0.1:57978/level3ab/api/custom_query?data={%20%20%20%20%22location%22:%20%22level1%22,%20%20%20%20%22operation%22:%20%22COUNT%22,%20%20%20%20%22type%22:%20%22bus%22,%20%20%20%20%22data%22:%20%22temperature%22,%20%20%20%20%22filter%22:%20{%20%20%20%20%20%20%20%20%22polygon%22:%20[[-75,%2040],%20[-75,%2041],[-74,%2041],%20[-74,%2040]%20],%20%20%20%20%20%20%20%20%22properties.status.description%22:%20%22running%20or%20not?%20not%20important%22%20%20%20%20}}"
    res = requests.get(url)
    print(res.status_code)

def localworker():
    url = "http://localhost:5005/api/custom_query?data={%20%20%20%20%22location%22:%20%22level1%22,%20%20%20%20%22operation%22:%20%22COUNT%22,%20%20%20%20%22type%22:%20%22bus%22,%20%20%20%20%22data%22:%20%22temperature%22,%20%20%20%20%22filter%22:%20{%20%20%20%20%20%20%20%20%22polygon%22:%20[[-75,%2040],%20[-75,%2041],[-74,%2041],%20[-74,%2040]%20],%20%20%20%20%20%20%20%20%22properties.status.description%22:%20%22running%20or%20not?%20not%20important%22%20%20%20%20}}"
    res = requests.get(url)
    print(res.status_code)

threads = []
for i in range(1500):
    t = threading.Thread(target=localworker)
    threads.append(t)
    t.start()