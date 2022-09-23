import mongoengine as me

class Logs(me.EmbeddedDocument):
    check_time = me.IntField(required=True)
    read_num = me.IntField(required=True)

class Contents(me.EmbeddedDocument):
    p_type = me.StringField(required=True)
    p_content = me.StringField(required=True)

class Area(me.Document):
    _id = me.StringField(required=True, max_length=200)
    title = me.StringField(required=True)
    url = me.StringField(required=True)
    key_words = me.StringField(required=True)
    locations = me.StringField(required=True)
    text = me.StringField(required=True)
    json_contents = me.ListField(me.EmbeddedDocumentField(Contents), required=False)
    issue_date = me.DateTimeField(required=True)
    add_time = me.IntField(required=True)
    status = me.IntField(required=True)
    biz = me.StringField(required=True)
    name = me.StringField(required=True)
    uin = me.StringField(required=False)
    check_time = me.DateTimeField(required=False)
    logs = me.ListField(me.EmbeddedDocumentField(Logs), required=False)
    rate = me.IntField(required=False)
    read_num = me.IntField(required=False)

