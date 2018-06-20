import base64
import json
import requests
import logging

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename=u'C:\Deleter\mylog.log')

jira_serverurl = 'https://jira.2gis.ru'
username = ""
password = ""

auth_header = "{}:{}".format(username, password)
auth_header_bytes = bytes(auth_header, encoding='ascii')
auth_header_b64 = base64.encodebytes(auth_header_bytes)
auth_header_encoded = str(auth_header_b64, encoding='ascii')
auth_header_encoded_no_trailing_endline = auth_header_encoded[:-1]
headers = {'Authorization': 'Basic ' + auth_header_encoded_no_trailing_endline,
           'Content-type': 'application/json',
           'Accept': 'application/json'}

url = jira_serverurl + '/rest/api/2/search'
url_issue = jira_serverurl + '/rest/api/2/issue'
search_request = '{"startAt": 0, "maxResults": 1000,"jql":"project = SUPPORT AND description is not null AND created >= -1d and assignee is not null"}'

req = requests.post(url, data=search_request, headers=headers)

issues = json.loads(req.text)

def delete_participant (ticket, participant):
    jira_serverurl = '{}/{}/?notifyUsers=false'.format(url_issue, ticket)
    data = {
        "update": {
            "customfield_13843": [{"remove": participant}]
        }
    }
    requests.put(jira_serverurl, data=json.dumps(data), headers=headers)

all_issue=0
update_issue = 0
if issues:
     for issue in issues['issues']:
         issue_key = issue['key']
         assignee = issue['fields']['assignee']['key']

         for ticket in issues['issues']:
            for field in ticket['fields']['customfield_13843']:
                if assignee==field['key']:
                    delete_participant(issue_key, field)
                    test = delete_participant(issue_key, field)
                    if test:
                         update_issue = update_issue + 1
                    all_issue = all_issue + 1
logging.info("All issues %s" %all_issue)
logging.info("Update issues %s" % update_issue)