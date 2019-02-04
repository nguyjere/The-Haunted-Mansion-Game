import requests
# https://words.bighugelabs.com/admin/68117b8ed3008c3c79295c7c552364bf
url = 'http://words.bighugelabs.com/api/2/68117b8ed3008c3c79295c7c552364bf/take/json'

response = requests.post(url)

print response.json()


# to get to this work, I updated to the newest version of Python 2.7, which included pip
# i then ran pip install requests to get the requests module

# fortunately, flip already has requests, so we will not need to download any external libraries to use this API in our
# game!