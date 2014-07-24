import json
from urllib.request import Request, urlopen

PROFILES_PER_REQUEST = 100

class Profile(object):
    """Profile(id, name)

    A Mojang Account profile, represented by their UUID and their current username.
    """
    __slots__ = ['id', 'name']

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def format_id(self):
        """Format the UUID as a dash-separated hex string
        
        Suited for ban lists, usercache.json, etc."""
        # Who decided it was a good idea to format a random number using dashes
        return "%s-%s-%s-%s-%s" % (self.id[:8], self.id[8:12], self.id[12:16], self.id[16:20], self.id[20:])

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.id, self.name)

    def to_json(self):
        """Turn the Profile into JSON of the same kind you would expect from Mojang's account server"""
        return json.dumps({'id': self.id, 'name': self.name})

    @staticmethod
    def from_json(data):
        """Convert the JSON representation of a Profile from Mojang's account server into a Profile"""
        return Profile(data['id'], data['name'])


class HttpProfileRepository(object):
    """A "profile respository" that communicates with Mojang's official HTTP servers
    See the java class this was based on: https://github.com/Mojang/AccountsClient/blob/master/src/main/java/com/mojang/api/profiles/HttpProfileRepository.java#L17"""
    def __init__(self, agent="minecraft"):
        self._profiles_url = "https://api.mojang.com/profiles/%s" % agent

    # May raise URLError while iterating
    def find_profiles_by_names(self, *names):
        """Look up profiles in the repository by name and yield each of them one by one.
        May raise a URLError while iterating."""
        headers = {"Content-Type": "application/json"}
        while names:
            batch, names = names[:PROFILES_PER_REQUEST], names[PROFILES_PER_REQUEST:]
            body = self.make_http_body(*batch)
            response = urlopen(Request(self._profiles_url, body, headers)).read()
            profiles = self.parse_http_response(response)
            yield from profiles

    def make_http_body(self, *names):
        """Turn a list of names into a HTTP body suitable for POSTing to Mojang's servers"""
        return json.dumps(names).encode()

    def parse_http_response(self, response):
        """Parse a response from Mojang's servers into a list of Profiles"""
        return [Profile.from_json(data) for data in json.loads(response.decode())]
