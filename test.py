import requests

data=[{"likes":10,"name":"Saurav","views":50},
      {"likes":20,"name":"Deepak","views":500},
      {"likes":50,"name":"Puja","views":10000}]
BASE="http://127.0.0.1:5000/"

"""for i in range(1,len(data)+1):
    response=requests.put(BASE+"video/"+str(i)+'/',data[i-1])
    print(response.json())

#input()"""
response=requests.patch(BASE+"video/1/",{'views':75})
print(response.json())

