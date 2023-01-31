import requests
import json


def get_access_token(username='micahjcfull@gmail.com', password="##$zewjyC-giqvi4"):
    url = "https://api.rapaygo.com/v1/auth/access_token"

    payload = "{\n    \"username\": \"" + username + "\",\n    \"pass_phrase\": \"" + password + "\",\n    \"type\": \"wallet_owner\"\n}"
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)

    ret = json.loads(response.text)['access_token']
    print(ret)
    return ret



token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiJtaWNhaGpjZnVsbEBnbWFpbC5jb20iLCJzY29wZXMiOlsid2FsbGV0Lm93biIsIndhbGxldC52aWV3Iiwid2FsbGV0LnRyYW5zZmVyIiwiaW52b2ljZV9wYXltZW50LmNyZWF0ZSIsImludm9pY2VfcGF5bWVudC52aWV3IiwiaW52b2ljZV9wYXltZW50LnVwZGF0ZSIsImN1c3RvbWVyLmNyZWF0ZSIsImN1c3RvbWVyLnZpZXciLCJjdXN0b21lci51cGRhdGUiLCJvcmRlci5jcmVhdGUiLCJvcmRlci52aWV3Iiwib3JkZXIudXBkYXRlIiwidm91Y2hlci5jcmVhdGUiLCJ2b3VjaGVyLnVwZGF0ZSIsInZvdWNoZXIuZGVsZXRlIiwidXNlcl9zZXR0aW5nLnZpZXciLCJ1c2VyX3NldHRpbmcuY3J1ZCIsInByb2R1Y3QudmlldyIsInByb2R1Y3QuY3J1ZCJdLCJleHAiOjE2NzUyMDkzMDEsInBvc19pZCI6IjVmYWEzIn0.DR6dQkaS3s6tngjr90db7NAsxSfkCh1S6brzfWUXVVU"



hash = "5cc270e3d2daccd00deb09f038b3ec950e117ad87566a1d9d5c3f896adfd4630"
url = f"https://api.rapaygo.com/v1/invoice_payment/{hash}"

payload = "{\n    \"amount_sats\": 334,\n    \"memo\": \"rapaygo POS voucher payment invoice 6a91e\"\n}"
headers = {
  'Authorization': token
}

response = requests.request("GET", url, headers=headers, data=payload)

rrr = json.loads(response.text)
print(rrr)
print()
print(rrr['status'])
