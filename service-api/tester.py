import requests
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

response = requests.get('https://api.rolnik-pro.lm.r.appspot.com/')
print(response)