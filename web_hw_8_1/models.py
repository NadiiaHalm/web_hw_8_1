from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)
