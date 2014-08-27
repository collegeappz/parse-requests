import json
import requests

AUTH_KEYS = {}


def set_keys(app_id, api_key):
    global AUTH_KEYS
    AUTH_KEYS = {
        'app_id': app_id,
        'api_key': api_key
    }


class BaseParseClass(object):
    _connection_error_message = ('Cannot connect to parse.com.')
    _parse_class_name = None
    _parse_special_classes = ['users', 'login', 'roles', 'files', 'events',
                              'push', 'installations', 'functions', 'jobs',
                              'requestPasswordReset', 'events', 'products',
                              'roles']

    def __init__(self, app_id=None, api_key=None):
        self._url = 'https://api.parse.com/1/'

        if self._parse_class_name is None:
            self._parse_class_name = self.__class__.__name__.lower()

        collection = (self._parse_class_name if
                      self._parse_class_name in
                      self._parse_special_classes else
                      'classes/' + self._parse_class_name)

        self._base_url = self._url + collection

        app_id = app_id if app_id else AUTH_KEYS.get('app_id')
        api_key = api_key if api_key else AUTH_KEYS.get('api_key')

        self._headers = {
            "X-Parse-Application-Id": app_id,
            "X-Parse-REST-API-Key": api_key,
            "Content-Type": "application/json"}

    def json(self):
        payload = {k: v for k, v in self.__dict__.iteritems()
                   if not k.startswith('_')}

        return payload

    def get(self, **kwargs):
        objectId = kwargs.pop('objectId', None)
        createdBy = kwargs.pop('createdBy', None)
        parentCategory = kwargs.pop('parentCategory', None)
        status = kwargs.pop('status', None)
        school = kwargs.pop('school', None)
        type = kwargs.pop('type', None)
        emailVerified = kwargs.pop('emailVerified', None)
        params = kwargs

        url = ("{base}/{id}".format(base=self._base_url, id=objectId) if
               objectId else self._base_url)

        where = {}
        if createdBy:
            where["createdBy"] = {"__type": "Pointer", "className": "_User",
                                  "objectId": createdBy}

        if school:
            where["school"] = {"__type": "Pointer", "className": "School",
                               "objectId": school}

        if parentCategory:
            where["parentCategory"] = {
                "__type": "Pointer",
                "className": "TaskCategory",
                "objectId": parentCategory}

        if status:
            where["status"] = status

        if type:
            where["type"] = type

        if emailVerified:
            where["emailVerified"] = True

        if where:
            params['where'] = json.dumps(where)

        try:
            payload = requests.get(url, headers=self._headers, params=params)

            return payload.json()

        except Exception as e:
            return {'error': e.message}

    def save(self):
        data = self.json()

        createdBy = data.pop('createdBy', False)
        if createdBy:
            data['createdBy'] = {"__type": "Pointer", "className": "_User",
                                 "objectId": createdBy}

        if data.get('objectId', False):
            return self.put(data=data)

        try:
            return self.post(data=data)
        except Exception as e:
            return {'error': e.message}

    def post(self, data):
        try:
            payload = requests.post(self._base_url, data=json.dumps(data),
                                    headers=self._headers)
            return payload.json()
        except Exception as e:
            return {'error': e.message}

    def put(self, data):
        url = (self._base_url + "/" + data.get('objectId')
               if data.get('objectId') else self._base_url)

        try:
            payload = requests.put(url=url,
                                   data=json.dumps(data),
                                   headers=self._headers)

            return payload.json()
        except Exception as e:
            return {'error': e.message}

    def delete(self, objectId):
        url = self._base_url + "/" + objectId

        try:
            res = requests.delete(url=url, headers=self._headers)

            return res.json()
        except Exception as e:
            return {'error': e.message}


class User(BaseParseClass):
    _parse_class_name = 'users'