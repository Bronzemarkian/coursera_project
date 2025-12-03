
import requests

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/t4-Vy4iOU19i8y6E3Px_ww/spacex-dash-app.py"
r = requests.get(url)

with open("spacex-dash-app.py", "wb") as f:
    f.write(r.content)



