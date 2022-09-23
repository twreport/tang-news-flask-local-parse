from api.utils.database import mysql_db
from api.utils.database import ma


class PushWeixinArticlesAi (mysql_db.Model):
    __tablename__ = 'push_weixin_articles_ai'
    article_id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    article_keywords = mysql_db.Column(mysql_db.Text)
    article_sort = mysql_db.Column(mysql_db.Integer)
    article_ai_sort = mysql_db.Column(mysql_db.Integer)
    status = mysql_db.Column(mysql_db.Integer)

    def create(self):
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self
    #
    # def update_article(self, rate, read_num, score):
    #     self.rate = rate
    #     self.read_num = read_num
    #     self.score = score
    #     mysql_db.session.commit()
    #
    # def update_local(self, local):
    #     self.article_local = local
    #     mysql_db.session.commit()
    #
    # def update_location(self, location):
    #     self.article_location = location
    #     mysql_db.session.commit()
    #
    # def update_sort(self, article_sort):
    #     self.article_sort = article_sort
    #     mysql_db.session.commit()

    def __init__(self, article_id, article_keywords, article_sort, article_ai_sort, status):
        self.article_id = article_id
        self.article_keywords = article_keywords
        self.article_sort = article_sort
        self.article_ai_sort = article_ai_sort
        self.status = status

    def __repr__(self):
        return '<Article %d>' % self.id + '|' + 'title %s' % self.title

class PushWeixinArticlesAiSchema (ma.SQLAlchemySchema):
    class Meta:
        model = PushWeixinArticlesAi
    article_id = ma.auto_field()
    article_keywords = ma.auto_field()
    article_sort = ma.auto_field()
    article_ai_sort = ma.auto_field()
    status = ma.auto_field()