import json
import base64
import urllib
import urllib2
import time

def chunks(data_list, size):

    for i in xrange(0, len(data_list), size):
        yield data_list[i:i+size]


client_key = "wjyQEZVQEUfO6msw0wiODitfk"
client_secret = "yBjFQjl2TLTZNGgqft2Ish42rBmJagGMBigSgdVAgZS1ksq2Oo"

credentials = "%s:%s" % (client_key, client_secret)
encoded_credentials = base64.b64encode(credentials)

# print(credentials)
# print(encoded_credentials)

params = {
	"grant_type": "client_credentials"
}

url = "https://api.twitter.com/oauth2/token"
headers = {"Authorization": "Basic %s" % encoded_credentials}
data = urllib.urlencode(params)

request = urllib2.Request(url, data, headers)

response = urllib2.urlopen(request)
raw_data = response.read()
json_data = json.loads(raw_data)

access_token = json_data["access_token"]


# print (access_token)


# FIRST ACCOUNT TO CHECK
url = "https://api.twitter.com/1.1/followers/ids.json"
params = {
    "screen_name": "ManUtd"
}
data = urllib.urlencode(params)
url = url + "?" + data
headers = {"Authorization": "Bearer %s" % (access_token)}

# print(url)
# print(data)
# print(headers)
print ("HOLD THE DOOR")

request = urllib2.Request(url, headers=headers)

try: 
    response = urllib2.urlopen(request)
except urllib2.HTTPError, e:
    print e
    print(e.message)
    print(e.info())

raw_data = response.read()
json_data = json.loads(raw_data)

club_followers = json_data["ids"]




# SECOND ACCOUNT TO CHECK
url = "https://api.twitter.com/1.1/followers/ids.json"
params = {
    "screen_name": "UKLabour"
}
data = urllib.urlencode(params)
url = url + "?" + data
headers = {"Authorization": "Bearer %s" % (access_token)}

# print(url)
# print(data)
# print(headers)
print ("HOLDTHEDOOR")

url_path = url

request = urllib2.Request(url, headers=headers)

try: 
    response = urllib2.urlopen(request)
except urllib2.HTTPError, e:
    print e
    print(e.message)
    print(e.info())

raw_data = response.read()
json_data = json.loads(raw_data)

n = json_data["next_cursor"]
while n is not 0:
	cursor_url = url_path + "&cursor=" + str(n)
	request = urllib2.Request(cursor_url, headers=headers)
	try: 
	    response = urllib2.urlopen(request)
	except urllib2.HTTPError, e:
		time.sleep(60 * 15)
		print e
		print(e.message)
		print(e.info())
		continue
	except StopIteration:
	        break
	raw_data = response.read()
	json_data = json.loads(raw_data)
	n = json_data["next_cursor"]


polpar_followers = json_data["ids"]

print("lenght : " + str(len(club_followers)))
print("lenght : " + str(len(polpar_followers)))

common_followers = set(club_followers) & set(polpar_followers)




# PRINT COMMON USERS
for chunk in chunks(list(common_followers), 100):

    user_id_str = "%s" % chunk[0]
    for user_id in chunk[1:]:
        user_id_str += ",%s" % (user_id)

    # print(user_id_str)
    print ("HOLDDOOR")

    url = "https://api.twitter.com/1.1/users/lookup.json"
    params = {
     "user_id": user_id_str
    }
    data = urllib.urlencode(params)
    url = url + "?" + data
    headers = {"Authorization": "Bearer %s" % (access_token)}

    # print(url)
    # print(data)
    # print(headers)
    print ("HODOR")

    request = urllib2.Request(url, headers=headers)

    try: 
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e
        print(e.message)
        print(e.info())

    raw_data = response.read()
    json_data = json.loads(raw_data)

    for user in json_data:
        print(user["screen_name"])