import mongoengine as me

class Test(me.Document):
    _id = me.StringField(required=True, max_length=200)
    test = me.StringField(required=True)
    add_time = me.IntField(required=True)
