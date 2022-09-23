from api.utils.database import mysql_db
from api.utils.database import ma


class AdminWeixinBizs (mysql_db.Model):
    __tablename__ = 'admin_weixin_bizs'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    biz = mysql_db.Column(mysql_db.String(45))
    name = mysql_db.Column(mysql_db.String(45))
    add_time = mysql_db.Column(mysql_db.Integer)
    update_time = mysql_db.Column(mysql_db.Integer)
    crawl_time = mysql_db.Column(mysql_db.Integer)
    interval = mysql_db.Column(mysql_db.Integer)
    type = mysql_db.Column(mysql_db.Integer)
    db = mysql_db.Column(mysql_db.String(45))
    read_num_avg = mysql_db.Column(mysql_db.Integer)
    read_rate_avg = mysql_db.Column(mysql_db.Integer)
    status = mysql_db.Column(mysql_db.Integer)

    def create(self):
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self

    def update_avg(self, read_num_avg, read_rate_avg):
        self.read_num_avg = read_num_avg
        self.read_rate_avg = read_rate_avg
        mysql_db.session.commit()

    def __init__(self, biz, name, add_time, update_time, crawl_time, interval, type, db, read_num_avg, read_rate_avg, status):
        self.biz = biz
        self.name = name
        self.add_time = add_time
        self.update_time = update_time
        self.crawl_time = crawl_time
        self.interval = interval
        self.type = type
        self.db = db
        self.read_num_avg = read_num_avg
        self.read_rate_avg = read_rate_avg
        self.status = status

    def __repr__(self):
        return '<Biz %d>' % self.id + '|' + 'biz_name %s' % self.name

class AdminWeixinBizsSchema (ma.SQLAlchemySchema):
    class Meta:
        model = AdminWeixinBizs
    id = ma.auto_field()
    biz = ma.auto_field()
    name = ma.auto_field()
    add_time = ma.auto_field()
    update_time = ma.auto_field()
    crawl_time = ma.auto_field()
    interval = ma.auto_field()
    type = ma.auto_field()
    db = ma.auto_field()
    read_num_avg = ma.auto_field()
    read_rate_avg = ma.auto_field()
    status = ma.auto_field()