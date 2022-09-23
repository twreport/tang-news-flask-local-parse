from api.utils.database import mysql_db
from api.utils.database import ma


class PushWeixinArticles (mysql_db.Model):
    __tablename__ = 'push_weixin_articles'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    title = mysql_db.Column(mysql_db.String(200))
    url = mysql_db.Column(mysql_db.String(200))
    text = mysql_db.Column(mysql_db.Text)
    json_contents = mysql_db.Column(mysql_db.Text)
    issue_date = mysql_db.Column(mysql_db.DateTime)
    push_time = mysql_db.Column(mysql_db.Integer)
    biz = mysql_db.Column(mysql_db.String(45))
    biz_name = mysql_db.Column(mysql_db.String(45))
    biz_level = mysql_db.Column(mysql_db.Integer)
    rate = mysql_db.Column(mysql_db.Integer)
    read_num = mysql_db.Column(mysql_db.Integer)
    score = mysql_db.Column(mysql_db.Integer)
    article_sort = mysql_db.Column(mysql_db.Integer)
    article_local = mysql_db.Column(mysql_db.Integer)
    article_value = mysql_db.Column(mysql_db.Integer)
    article_location = mysql_db.Column(mysql_db.String(500))
    status = mysql_db.Column(mysql_db.Integer)

    def create(self):
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self

    def update_article(self, rate, read_num, score):
        self.rate = rate
        self.read_num = read_num
        self.score = score
        mysql_db.session.commit()

    def update_local(self, local):
        self.article_local = local
        mysql_db.session.commit()

    def update_location(self, location):
        self.article_location = location
        mysql_db.session.commit()

    def update_sort(self, article_sort):
        self.article_sort = article_sort
        mysql_db.session.commit()

    def update_status(self, status):
        self.status = status
        mysql_db.session.commit()

    def __init__(self, title, url, text, json_contents, issue_date, push_time, biz, biz_name, biz_level, rate,
                 read_num, score, article_sort, article_local, article_value, article_location, status):
        self.title = title
        self.url = url
        self.text = text
        self.json_contents = json_contents
        self.issue_date = issue_date
        self.push_time = push_time
        self.biz = biz
        self.biz_name = biz_name
        self.biz_level = biz_level
        self.rate = rate
        self.read_num = read_num
        self.score = score
        self.article_sort = article_sort
        self.article_local = article_local
        self.article_value = article_value
        self.article_location = article_location
        self.status = status

    def __repr__(self):
        return '<Article %d>' % self.id + '|' + 'title %s' % self.title

class PushWeixinArticlesSchema (ma.SQLAlchemySchema):
    class Meta:
        model = PushWeixinArticles
    id = ma.auto_field()
    title = ma.auto_field()
    url = ma.auto_field()
    text = ma.auto_field()
    json_contents = ma.auto_field()
    issue_date = ma.auto_field()
    push_time = ma.auto_field()
    biz = ma.auto_field()
    biz_name = ma.auto_field()
    biz_level = ma.auto_field()
    rate = ma.auto_field()
    read_num = ma.auto_field()
    score = ma.auto_field()
    article_sort = ma.auto_field()
    article_local = ma.auto_field()
    article_value = ma.auto_field()
    article_location = ma.auto_field()
    status = ma.auto_field()