from api.utils.database import mysql_db
from api.utils.database import ma


class PushWeixinTopics (mysql_db.Model):
    __tablename__ = 'push_weixin_topics'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    topic_title = mysql_db.Column(mysql_db.String(200))
    topic_keywords = mysql_db.Column(mysql_db.String(500))
    topic_article_num = mysql_db.Column(mysql_db.Integer)
    topic_read_num = mysql_db.Column(mysql_db.Integer)
    topic_read_num_avg = mysql_db.Column(mysql_db.Integer)
    topic_score = mysql_db.Column(mysql_db.Integer)
    topic_sort = mysql_db.Column(mysql_db.Integer)
    is_local = mysql_db.Column(mysql_db.Integer)
    location = mysql_db.Column(mysql_db.Text)
    add_time = mysql_db.Column(mysql_db.Integer)
    is_cloud = mysql_db.Column(mysql_db.Integer)
    status = mysql_db.Column(mysql_db.Integer)

    def create(self):
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self

    def update_datas(self, topic_keywords, topic_article_num, topic_read_num, topic_read_num_avg, topic_score):
        self.topic_keywords = topic_keywords
        self.topic_article_num = topic_article_num
        self.topic_read_num = topic_read_num
        self.topic_read_num_avg = topic_read_num_avg
        self.topic_score = topic_score
        self.is_cloud = 0
        mysql_db.session.commit()

    def __init__(self, topic_title, topic_keywords, topic_article_num, topic_read_num, topic_read_num_avg, topic_score, topic_sort, is_local, location, add_time, is_cloud, status):
        self.topic_title = topic_title
        self.topic_keywords = topic_keywords
        self.topic_article_num = topic_article_num
        self.topic_read_num = topic_read_num
        self.topic_read_num_avg = topic_read_num_avg
        self.topic_score = topic_score
        self.topic_sort = topic_sort
        self.is_local = is_local
        self.location = location
        self.add_time = add_time
        self.is_cloud = is_cloud
        self.status = status

    def __repr__(self):
        return '<Article %d>' % self.id + '|' + 'title %s' % self.title

class PushWeixinTopicsSchema (ma.SQLAlchemySchema):
    class Meta:
        model = PushWeixinTopics
    id = ma.auto_field()
    topic_title = ma.auto_field()
    topic_keywords = ma.auto_field()
    topic_article_num = ma.auto_field()
    topic_read_num = ma.auto_field()
    topic_read_num_avg = ma.auto_field()
    topic_score = ma.auto_field()
    topic_sort = ma.auto_field()
    is_local = ma.auto_field()
    location = ma.auto_field()
    add_time = ma.auto_field()
    is_cloud = ma.auto_field()
    status = ma.auto_field()