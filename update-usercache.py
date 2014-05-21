#!/usr/bin/env python3
# Example of a more "useful" python script: appending UUIDs to usercache.json
from datetime import datetime, timedelta
import json
import os
from shutil import copy
import sys
from tempfile import NamedTemporaryFile

from mojang_accounts import HttpProfileRepository

def main(args):
    args = args[1:]
    if not args:
        print("Pass me a few players to add to your usercache.json")
        return 1

    def to_cache_entry(profile):
        return {'id': profile.format_id(),
                'name': profile.name,
                'expiresOn': (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S +0000")}

    users_path = os.path.join(os.getcwd(), 'usercache.json')
    users = json.load(open(users_path)) or []
    for user in HttpProfileRepository().find_profiles_by_names(*args):
        users.append(to_cache_entry(user))
    tmpfile = NamedTemporaryFile('w+t')
    json.dump(users, tmpfile)
    tmpfile.flush()
    copy(tmpfile.name, users_path)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
