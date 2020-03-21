#!/usr/bin/env python3

import datetime
import http.client
import json
import os.path
import sys
import uuid


class GroupMeClient:
    def __init__(self, token):
        self.token = token

    def get_groups(self):
        conn = http.client.HTTPSConnection("api.groupme.com")
        conn.request("GET", "/v3/groups?token=%s" % self.token)
        resp = conn.getresponse()
        if resp.status != 200:
            raise Exception("Bad status code")
        return json.loads(resp.read().decode())["response"]

    def set_name(self, group_id, name):
        conn = http.client.HTTPSConnection("api.groupme.com")
        conn.request("POST", "/v3/groups/%s/update?token=%s" % (group_id, self.token), body=json.dumps({"name": name}), headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        if resp.status != 200:
            raise Exception("Bad status code")

    def post_message(self, group_id, message):
        conn = http.client.HTTPSConnection("api.groupme.com")
        msg = {
            "message": {
                "source_guid": str(uuid.uuid4()),
                "text": message,
                "attachments": [],
            }
        }
        conn.request("POST", "/v3/groups/%s/messages?token=%s" % (group_id, self.token), body=json.dumps(msg), headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        if resp.status != 201:
            raise Exception("Bad status code")


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "groupme.conf"), "r") as f:
        conf = json.load(f)
    client = GroupMeClient(conf["token"])

    if sys.argv[1] == "list_groups":
        groups = client.get_groups()
        for g in groups:
            print("%s - \"%s\"" % (g["id"], g["name"]))
    elif sys.argv[1] == "ghost_house":
        diff = datetime.date.today() - datetime.date(2020, 3, 12)
        client.set_name(sys.argv[2], "Day %i in Quarantine" % diff.days)
    elif sys.argv[1] == "post_message":
        client.post_message(sys.argv[2], sys.argv[3])
    else:
        raise Exception("Invalid command: %s" % sys.argv[1])
