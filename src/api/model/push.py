from api.utils.database import mysql_db
from api.utils.database import ma

class PushWeixinArticlesPool (mysql_db.Model):
    __tablename__ = 'push_weixin_articles_pool'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    title = mysql_db.Column(mysql_db.String(200))
    url = mysql_db.Column(mysql_db.String(200))
    text = mysql_db.Column(mysql_db.Text)
    sci_text = mysql_db.Column(mysql_db.Text)
    json_contents = mysql_db.Column(mysql_db.Text)
    issue_date = mysql_db.Column(mysql_db.DateTime)
    push_time = mysql_db.Column(mysql_db.Integer)
    biz = mysql_db.Column(mysql_db.String(45))
    biz_name = mysql_db.Column(mysql_db.String(45))
    biz_level = mysql_db.Column(mysql_db.Integer)
    rate = mysql_db.Column(mysql_db.Integer)
    read_num = mysql_db.Column(mysql_db.Integer)
    score = mysql_db.Column(mysql_db.Integer)
    sort = mysql_db.Column(mysql_db.Integer)
    sort_ai = mysql_db.Column(mysql_db.Integer)
    is_local = mysql_db.Column(mysql_db.Integer)
    location = mysql_db.Column(mysql_db.String(50000))
    is_value = mysql_db.Column(mysql_db.Integer)
    is_value_ai = mysql_db.Column(mysql_db.Integer)
    is_cloud = mysql_db.Column(mysql_db.Integer)
    is_topic = mysql_db.Column(mysql_db.Integer)
    topic_id = mysql_db.Column(mysql_db.Integer)
    status = mysql_db.Column(mysql_db.Integer)

    def create(self):
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self

    def update_article(self, rate, read_num, score):
        self.rate = rate
        self.read_num = read_num
        self.score = score
        # 凡是更新群晖mysql数据库，都需要将是否同步到云上标记为0，以便于同步程序将变更同步上云
        self.is_cloud = 0
        mysql_db.session.commit()

    def update_is_local(self, is_local):
        self.is_local = is_local
        self.is_cloud = 0
        mysql_db.session.commit()

    def update_location(self, location):
        self.location = location
        self.is_cloud = 0
        mysql_db.session.commit()

    def update_sort(self, sort):
        self.sort = sort
        self.is_cloud = 0
        mysql_db.session.commit()

    def update_status(self, status):
        self.status = status
        self.is_cloud = 0
        mysql_db.session.commit()

    def update_sci_text(self, text):
        self.sci_text = text
        mysql_db.session.commit()

    def update_topic_id(self, topic_id):
        self.is_topic = 1
        self.topic_id = topic_id
        mysql_db.session.commit()

    def __init__(self, title, url, text, sci_text, json_contents, issue_date, push_time, biz, biz_name, biz_level, rate,
                 read_num, score, sort, sort_ai, is_local, location, is_value, is_value_ai, is_cloud, is_topic,
                 topic_id, status):
        self.title = title
        self.url = url
        self.text = text
        self.sci_text = sci_text
        self.json_contents = json_contents
        self.issue_date = issue_date
        self.push_time = push_time
        self.biz = biz
        self.biz_name = biz_name
        self.biz_level = biz_level
        self.rate = rate
        self.read_num = read_num
        self.score = score
        self.sort = sort
        self.sort_ai = sort_ai
        self.is_local = is_local
        self.location = location
        self.is_value = is_value
        self.is_value_ai = is_value_ai
        self.is_cloud = is_cloud
        self.is_topic = is_topic
        self.topic_id = topic_id
        self.status = status

    def __repr__(self):
        return '<Article %d>' % self.id + '|' + 'title %s' % self.title

class PushWeixinArticlesSchema (ma.SQLAlchemySchema):
    class Meta:
        model = PushWeixinArticlesPool
    id = ma.auto_field()
    title = ma.auto_field()
    url = ma.auto_field()
    text = ma.auto_field()
    sci_text = ma.auto_field()
    json_contents = ma.auto_field()
    issue_date = ma.auto_field()
    push_time = ma.auto_field()
    biz = ma.auto_field()
    biz_name = ma.auto_field()
    biz_level = ma.auto_field()
    rate = ma.auto_field()
    read_num = ma.auto_field()
    score = ma.auto_field()
    sort = ma.auto_field()
    sort_ai = ma.auto_field()
    is_local = ma.auto_field()
    location = ma.auto_field()
    is_value = ma.auto_field()
    is_value_ai = ma.auto_field()
    is_cloud = ma.auto_field()
    is_topic = ma.auto_field()
    topic_id = ma.auto_field()
    status = ma.auto_field()