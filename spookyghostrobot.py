#!/usr/bin/env python3

import datetime
import http.client
import json
import os.path
import sys


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
        conn.request("POST", "/v3/groups/" + group_id + "/update?token=%s" % self.token, body=json.dumps({"name": name}))
        resp = conn.getresponse()
        if resp.status != 200:
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
        diff = datetime.date.today() - datetime.date(2019, 1, 23)
        if 25 <= diff.days <= 29:
            client.set_name(sys.argv[2], "Day %i in the Ghost House Cracker Barrel" % diff.days)
        elif 35 <= diff.days <= 39:
            client.set_name(sys.argv[2], "Day %i in the Ghost House ER" % diff.days)
        else:
            client.set_name(sys.argv[2], "Day %i in the Ghost House" % diff.days)
