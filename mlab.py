import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds131512.mlab.com:31512/haihoa



host = "ds131512.mlab.com"
port = 31512
db_name = "haihoa"
user_name = "admin"
password = "MlaDagon5"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())