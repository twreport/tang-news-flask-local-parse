from api.utils.database import mysql_db
from api.utils.database import ma


class AdminSort (mysql_db.Model):
    __tablename__ = 'admin_sort'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    sort_name = mysql_db.Column(mysql_db.String(20))
    sort_power = mysql_db.Column(mysql_db.Integer)
    keywords = mysql_db.Column(mysql_db.String(2000))
    status = mysql_db.Column(mysql_db.Integer)

    def create(self):
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self

    def __init__(self, sort_name, sort_power, keywords, status):
        self.sort_name = sort_name
        self.sort_power = sort_power
        self.keywords = keywords
        self.status = status

    def __repr__(self):
        return '<Article %d>' % self.id + '|' + 'title %s' % self.title

class AdminSortSchema (ma.SQLAlchemySchema):
    class Meta:
        model = AdminSort
    id = ma.auto_field()
    sort_name = ma.auto_field()
    sort_power = ma.auto_field()
    keywords = ma.auto_field()
    status = ma.auto_field()