import json

data = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])

print(type(data))

data = json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')

print(type(data))
