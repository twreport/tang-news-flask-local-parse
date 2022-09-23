from api.model.province import Province
from api.model.area import Area
from api.model.county import County
from api.service.location import LocationService
import re
from api.model.biz import AdminWeixinBizs
from api.model.article import PushWeixinArticles
from api.model.push import PushWeixinArticlesPool
from mongoengine.queryset.visitor import Q
import api.utils.constants as cons
import time
import numpy as np
import json


class ParseService:
    def __init__(self):
        pass

    def parse_article(self):
        now_time = int(time.time())
        time_limit = now_time - cons.PARSE_TIME

        query_area = Area.objects(add_time__gte=time_limit)
        print("----------------Area Article Numbers-----------------------------")
        print(len(query_area))
        for qa in query_area:
            if qa.logs is not []:
                res_tuple_qa = self.parse_logs(qa.logs, qa.issue_date)
                if res_tuple_qa is not False:
                    print(qa._id)
                    print(qa.title)
                    print(res_tuple_qa)
                    Area.objects(_id=qa._id).update_one(set__rate=res_tuple_qa[0], set__read_num=res_tuple_qa[1])
                    result = self.handle_article(res_tuple_qa, qa)

        query_province = Province.objects(add_time__gte=time_limit)
        print("----------------Province Article Numbers-----------------------------")
        print(len(query_province))
        for qp in query_province:
            if qp.logs is not []:
                res_tuple_qp = self.parse_logs(qp.logs, qp.issue_date)
                if res_tuple_qp is not False:
                    print(qp._id)
                    print(qp.title)
                    print(res_tuple_qp)
                    Province.objects(_id=qp._id).update_one(set__rate=res_tuple_qp[0], set__read_num=res_tuple_qp[1])
                    result = self.handle_article(res_tuple_qp, qp)

        query_county = County.objects(add_time__gte=time_limit)
        print("----------------County Article Numbers-----------------------------")
        print(len(query_county))
        for qc in query_county:
            if qc.logs is not []:
                res_tuple_qc = self.parse_logs(qc.logs, qc.issue_date)
                if res_tuple_qc is not False:
                    print(qc._id)
                    print(qc.title)
                    print(res_tuple_qc)
                    County.objects(_id=qc._id).update_one(set__rate=res_tuple_qc[0], set__read_num=res_tuple_qc[1])
                    result = self.handle_article(res_tuple_qc, qc)

        return time_limit

    # 新版函数思路：只考虑计算增长瞬时斜率
    def parse_logs(self, logs, issue_date):
        if len(logs) > 0:
            issue_time = self.date_to_num(issue_date)
            last_log = logs[-1]
            last_update_time = int(last_log.check_time)
            x = int(last_update_time - issue_time)
            y = int(last_log.read_num)
            # rate为文章的"阅读量/每小时"增长速率
            # 如果是10W+热文，两天的每小时增长率为2083
            # 如果是1000的文章，两天的每小时增长率为20.83
            # 一般的文章阅读量来自于发稿后的6小时，因此将瞬时增长速率门槛可适当提高！！！
            rate = int( y * 3600 / x )
            return rate, y
        else:
            return False



    # 旧版函数，暂停用！！！
    # 返回对象，最大阅读数num和增长斜率k，lg增长斜率lgk
    '''
    def parse_logs(self, logs, issue_date):
        if len(logs) > 0:
            print('parse_logs!')
            X = []
            Y = []
            # 先把初始值赋予数组
            x0 = self.date_to_num(issue_date)
            y0 = 0
            # 因为log0 = -无穷，所以x轴第一个数字应该为1
            X.append(1)
            Y.append(0)
            for log in logs:
                X.append(int(log.check_time - x0))
                Y.append(int(log.read_num))
            x = np.array(X)
            y = np.array(Y)
            x_log = np.log(x)
            # print(x)
            # print(y)
            # print(x_log)
            # 拟合log曲线
            result = np.polyfit(x_log, y, 1)
            # # 线性拟合
            # result = np.polyfit(x, y, 1)
            # print("This Article's Rate is:")
            # print(int(result[0]))
            # print("This Article's Max Read Number is:")
            # print(y[-1])
            # print(result)
            return int(result[0]), int(y[-1])
        return False
        '''

    def handle_article(self, res_tuple, article):
        # print("------------------in handle_article-----------------------")
        # print(res_tuple)
        # print(article.title)
        # article.rate = res_tuple[0]
        # article.read_num = res_tuple[1]
        # article.save()
        return False

    def date_to_num(self, issue_date):
        struct_time = time.strptime(issue_date, '%Y-%m-%d %H:%M:%S')
        timestamp = int(time.mktime(struct_time))
        return timestamp

    def count_avg_of_bizs(self):
        bizs = AdminWeixinBizs.query.all()
        now_time = int(time.time())
        time_limit = now_time - cons.AVG_TIME
        print("======================in count_avg_of_bizs!=======================")
        for biz in bizs:
            if biz.type == 1:
                print("---------------in province!----------------")
                query_province = Province.objects(biz=biz.biz, add_time__gte=time_limit)
                i = 0
                total_num = 0
                total_rate = 0
                for qp in query_province:
                    if qp.logs is not [] and qp.read_num is not None:
                        i = i + 1
                        total_num = total_num + qp.read_num
                        total_rate = total_rate + qp.rate

                if i == 0:
                    continue

                final_num = int(total_num / i)
                final_rate = int(total_rate / i)
                biz.update_avg(final_num, final_rate)
            elif biz.type == 2:
                print("---------------in area!----------------")
                query_area = Area.objects(biz=biz.biz, add_time__gte=time_limit)
                j = 0
                total_num = 0
                total_rate = 0
                for qa in query_area:
                    if qa.logs is not [] and qa.read_num is not None:
                        j = j + 1
                        total_num = total_num + qa.read_num
                        total_rate = total_rate + qa.rate

                if j == 0:
                    continue

                final_num = int(total_num / j)
                final_rate = int(total_rate / j)
                biz.update_avg(final_num, final_rate)
            else:
                query_county = County.objects(biz=biz.biz, add_time__gte=time_limit)
                print("---------------in county!----------------")
                k = 0
                total_num = 0
                total_rate = 0
                for qc in query_county:
                    if qc.logs is not [] and qc.read_num is not None:
                        k = k + 1
                        total_num = total_num + qc.read_num
                        total_rate = total_rate + qc.rate

                if k == 0:
                    continue

                final_num = int(total_num / j)
                final_rate = int(total_rate / j)
                biz.update_avg(final_num, final_rate)
        return True

    def scan_articles(self):
        score = 0
        now_time = int(time.time())
        time_limit = now_time - cons.PARSE_TIME
        province_articles = Province.objects(add_time__gte=time_limit, read_num__ne=None)
        i = 0
        for province_article in province_articles:
            # score = self.get_score(province_article)
            # 省级公众号，只要超过预定分值，且阅读数超过预定阅读量，即push
            # 暂不考虑score, 以省市县不同门槛区分文章活性
            # if score is not None and score > cons.PROVINCE_PUSH_LIMIT and province_article.read_num > cons.PROVINCE_READ_NUM_LIMIT:
            if province_article.rate > cons.PROVINCE_RATE_LIMIT or province_article.read_num > cons.PROVINCE_READ_NUM_LIMIT:
                print(province_article.title)
                self.push_article_to_pool(province_article, 0, 1)
                i = i + 1

        area_articles = Area.objects(add_time__gte=time_limit, read_num__ne=None)
        j = 0
        for area_article in area_articles:
            # score = self.get_score(area_article)
            # 地区级公众号，只要超过预定分值，且阅读数超过预定阅读量，即push
            if area_article.rate > cons.AREA_RATE_LIMIT or area_article.read_num > cons.AREA_READ_NUM_LIMIT:
                print(area_article.title)
                self.push_article_to_pool(area_article, 0, 2)
                j = j + 1

        county_articles = County.objects(add_time__gte=time_limit, read_num__ne=None)
        k = 0
        for county_article in county_articles:
            # score = self.get_score(county_article)
            # 地区级公众号，只要超过预定分值，且阅读数超过预定阅读量，即push
            if county_article.rate > cons.COUNTY_RATE_LIMIT or county_article.read_num > cons.COUNTY_READ_NUM_LIMIT:
                print(county_article.title)
                self.push_article_to_pool(county_article, 0, 3)
                k = k + 1

        result = str(i) + ' articles from province is pushed! ' + str(j) + ' articles from area is pushed! ' + str(k) + ' articles from area is pushed!'
        return result


    # 计算文章传播数据得分
    # 旧版函数，暂不用
    def get_score(self, article):
        # 取出文章所在公众号的平均值
        biz_name = article.biz
        biz_object = AdminWeixinBizs.query.filter_by(biz=biz_name).first()
        # 如果公众号平均值尚未算出，则跳过！
        if biz_object.read_num_avg != 0 and biz_object.read_rate_avg != 0 and biz_object.read_num_avg is not None and biz_object.read_rate_avg is not None:
            read_num_avg = biz_object.read_num_avg
            read_rate_avg = biz_object.read_rate_avg
        else:
            return None
        # 时效性越强的得分越高, 得分范围在0-100，有可能略微负分：）
        now_time = int(time.time())
        issue_time = self.change_time(article.issue_date)
        time_score = 100 - int(((now_time - issue_time) / cons.PARSE_TIME) * 100)

        # 绝对阅读量占比100分,超过1w访问量的文章即算满分
        # 20220709-加大绝对阅读量的占比，毕竟要以阅读数为最重要因素
        # 得分范围 0-1000分
        read_num = article.read_num
        read_num_score = read_num / 100

        # 阅读量相对于所在公众号平均值偏离量
        # 正常得分范围在-1000到1000之间
        read_num_avg_score = ((read_num - read_num_avg) / read_num_avg) * 100

        # 增长率相对于所在公众号平均值偏离量
        # 正常得分范围在-10到1000之间
        read_rate_avg_score = ((article.rate - read_rate_avg) / read_rate_avg) * 100

        final_score = int(time_score + read_num_score + read_num_avg_score + read_rate_avg_score)
        return final_score


    # 单元测试函数(旧版）
    # def test_push_article(self, article_add_time=1657255794, score=0, biz_level=1):
    #     articles = Province.objects(add_time=article_add_time)
    #     for article in articles:
    #         print(article.title)
    #         self.push_article_to_pool(article, score, biz_level)

    '''
    # 迁移函数, 已废弃
    def test_push_article(self, article_add_time=1657255794, score=0, biz_level=1):
        articles = PushWeixinArticles.query.all()

        for article in articles:
            print(article.title)
            article_obj = PushWeixinArticlesPool.query.filter_by(url=article.url).first()
            if article_obj is not None:
                print("Article is Exist, None Push!")
            else:
                print("Article is Exist, None Push!")
                px = PushWeixinArticlesPool(article.title, article.url, article.text, article.json_contents, article.issue_date,
                                        article.push_time, article.biz, article.biz_name, article.biz_level, article.rate, article.read_num,
                                        article.score, article.article_sort, 0, article.article_local, article.article_location, 0, 0, 0, 1)
                px.create()
        return len(articles)

    # 旧版函数，已废弃
    def push_article(self, article, score, biz_level):
        # 取出已经push的article，如果不存在则新增
        article_obj = PushWeixinArticles.query.filter_by(url=article.url).first()
        if article_obj is not None:
            print("Article is Exist, None Push!")
            article_obj.update_article(article.rate, article.read_num, score)
        else:
            print("Article To Push")
            print(article.title)
            print("==============Article is Not Exist, Now Push It!=============")
            now_time = int(time.time())
            if hasattr(article, 'json_contents'):
                print("json_content is exist!")
                json_contents = []
                for json_content in article.json_contents:
                    new_json_content = {
                        'p_type': json_content.p_type,
                        'p_content': json_content.p_content
                    }
                    print(new_json_content)
                    json_contents.append(new_json_content)
                print(json_contents)
                json_contents_str = json.dumps(json_contents)
            else:
                print("json_content is None!")
                data = []
                json_contents = json.dumps(data)
            article_text = self.del_spec_str(article.text)
            # article_title = self.del_spec_str(article.title)
            px = PushWeixinArticles(article.title, article.url, article_text, json_contents_str, article.issue_date,
                                    now_time, article.biz, article.name, biz_level, article.rate, article.read_num,
                                    score, 0, 0, 0, '', 1)
            px.create()
        return None
        '''

    def push_article_to_pool(self, article, score, biz_level):
        # 取出已经push的article，如果不存在则新增
        article_obj = PushWeixinArticlesPool.query.filter_by(url=article.url).first()
        if article_obj is not None:
            print("Article is Exist, None Push!")
            article_obj.update_article(article.rate, article.read_num, score)
        else:
            print("Article To Push")
            print(article.title)
            print("==============Article is Not Exist, Now Push It!=============")
            now_time = int(time.time())
            json_contents = []
            if hasattr(article, 'json_contents'):
                print("json_content is exist!")
                for json_content in article.json_contents:
                    new_json_content = {
                        'p_type': json_content.p_type,
                        'p_content': json_content.p_content
                    }
                    print(new_json_content)
                    json_contents.append(new_json_content)
                print(json_contents)
                json_contents_str = json.dumps(json_contents)
            else:
                print("json_content is None!")
                data = []
                json_contents_str = json.dumps(data)
            article_text = self.del_spec_str(article.text)
            article_title = self.del_spec_title_str(article.title)
            px = PushWeixinArticlesPool(article_title, article.url, article_text, '', json_contents_str, article.issue_date,
                                    article.add_time, article.biz, article.name, biz_level, article.rate, article.read_num,
                                    score, 0, 0, 0, '', 0, 0, 0, 0, 0, 1)
            px.create()
        return None

    # 字符串时间转为时间戳
    def change_time(self, str1):
        unixtime = time.mktime(time.strptime(str1, '%Y-%m-%d %H:%M:%S'))
        return int(unixtime)

    # 处理异常字符
    def del_spec_str(self, text_str):
        if isinstance(text_str, str):
            text_str = re.sub('[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘！[\\]^_`{|}~\s]+', "", text_str)
            # 去除不可见字符
            text_str = re.sub(
                '[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+',
                '', text_str)
            text_str = re.sub('👆', "", text_str)
            text_str = re.sub('🤙', "", text_str)
            text_str = re.sub('🤩', "", text_str)
            text_str = re.sub('\xF0\x9F\xA4\xA9', "", text_str)
            print(text_str)
            text_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", text_str)
            return text_str
        else:
            return ''


    # 处理异常字符
    def del_spec_title_str(self, text_str):
        if isinstance(text_str, str):
            # text_str = re.sub('[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘！[\\]^_`{|}~\s]+', "", text_str)
            # 去除不可见字符
            text_str = re.sub(
                '[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+',
                '', text_str)
            text_str = re.sub('👆', "", text_str)
            text_str = re.sub('🤙', "", text_str)
            text_str = re.sub('🤩', "", text_str)
            text_str = re.sub('\xF0\x9F\xA4\xA9', "", text_str)
            print(text_str)
            text_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", text_str)
            return text_str
        else:
            return ''