import json
from urllib.request import Request, urlopen

PROFILES_PER_REQUEST = 100

class Profile(object):
    __slots__ = ['id', 'name']

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.id, self.name)

    def to_json(self):
        return json.dumps({'id': self.id, 'name': self.name})

    @staticmethod
    def from_json(data):
        return Profile(data['id'], data['name'])


class HttpProfileRepository(object):
    def __init__(self, agent="minecraft"):
        self._profiles_url = "https://api.mojang.com/profiles/%s" % agent

    # May raise URLError while iterating
    def find_profiles_by_names(self, *names):
        headers = {"Content-Type": "application/json"}
        while names:
            batch, names = names[:PROFILES_PER_REQUEST], names[PROFILES_PER_REQUEST:]
            body = self.make_http_body(*batch)
            response = urlopen(Request(self._profiles_url, body, headers)).read()
            profiles = self.parse_http_response(response)
            for profile in profiles:
                yield profile

    def make_http_body(self, *names):
        return json.dumps(names).encode()

    def parse_http_response(self, response):
        return [Profile.from_json(data) for data in json.loads(response.decode())]
