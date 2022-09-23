from api.model.push import PushWeixinArticlesPool
from api.model.topic import PushWeixinTopics
from api.model.sort import AdminSort
from collections import Counter
from pyhanlp import *
from api.service.classify import ClassifyService
import api.utils.constants as cons
import time

class TopicService:
    def __init__(self):
        # 结巴分词关键词提取数量
        self.topk = 20
        # 48小时限制时间戳
        now_time = int(time.time())
        self.time_limit = now_time - cons.PARSE_TIME

    def make_cluster(self):
        ClusterAnalyzer = SafeJClass('com.hankcs.hanlp.mining.cluster.ClusterAnalyzer')
        analyzer = ClusterAnalyzer()
        classify = ClassifyService()
        # 从数据库中取出数据，(刊播时间少于48小时的文章）
        articles = PushWeixinArticlesPool.query.filter(PushWeixinArticlesPool.push_time > self.time_limit).all()

        for article in articles:
            # 将标题分词和文本关键词组成待分析文本，加入到hanlp分析器
            if article.sci_text == '':
                text_cut = self.cut_fake_local_name(article.biz_name, article.text)
                text = classify.get_key_words_from_title_and_text(article.title, text_cut)
                article.update_sci_text(text)
            else:
                text = article.sci_text
            analyzer.addDocument(article.id, text)
        # 将每48小时的新闻大致分组
        num = int(len(articles) / cons.ARTICLES_NUM_1_CLUSTER)
        print(num)
        clusters = analyzer.kmeans(num)

        # clusters = analyzer.repeatedBisection(1.0)

        # hanlp聚类后形成的数据结构是[[1,2,3],[4,5],[6,7,8,9]]这样的嵌套list
        # 遍历每一个话题
        for cluster in clusters:
            print("============================cluster================================")
            cluster_words_list = []
            cluster_article_list = []
            cluster_read_num = 0
            cluster_articles_num = len(cluster)
            # 根据每一篇文章的id找出文章
            for id in cluster:
                item = PushWeixinArticlesPool.query.get(int(id))
                print(item.title)
                # 复制obj列表，避免多次查询数据库
                cluster_article_list.append(item)
                # 计算话题阅读量总数
                cluster_read_num = cluster_read_num + int(item.read_num)
                # 按照hanlp的要求生成id之后的text
                sci_text_list = item.sci_text.split(',')
                for sci_text in sci_text_list:
                    cluster_words_list.append(sci_text)

            # 计算话题阅读量平均数
            cluster_read_num_avg = int(cluster_read_num / cluster_articles_num)

            # 将话题的关键词按照值的大小排序
            cluster_words_obj = Counter(cluster_words_list)
            cluster_words_obj_ordered = sorted(cluster_words_obj.items(), key=lambda x: x[1], reverse=True)

            # 得出话题中频次最高的关键词和频次前五的关键词字符串
            i = 0
            cluster_title_str = '|'
            for cluster_word in cluster_words_obj_ordered:
                if i == 0:
                    cluster_title_keywords = cluster_word[0]
                if i < 5:
                    cluster_title_str = cluster_title_str + cluster_word[0] + '|'
                    i = i + 1
            cluster_title_to_show = ''
            for article in cluster_article_list:
                if cluster_title_keywords in article.title and article.read_num > cluster_read_num_avg:
                    cluster_title_to_show = article.title
                    break
            if cluster_title_to_show == '':
                cluster_title_to_show = cluster_title_str

            # 分析话题分类
            topic_sort = self.parse_topic_sort(cluster_article_list)
            # 计算话题的score
            topic_score = self.count_score(cluster_read_num, cluster_read_num_avg, topic_sort)

            print(cluster_title_to_show)
            print(cluster_title_str)
            print('read_num:', cluster_read_num)
            print('read_num_avg:', cluster_read_num_avg)
            print('topic_sort:', topic_sort)
            print('topic_score:', topic_score)

            now_time = int(time.time())
            topics = PushWeixinTopics.query.filter_by(topic_title=cluster_title_to_show).all()
            if len(topics) > 0:
                topic = topics[0]
                topic.update_datas(cluster_title_str, cluster_articles_num, cluster_read_num, cluster_read_num_avg, topic_score)
                # 将所有与主题关联的文章更新topic_id
                for article in cluster_article_list:
                    article.update_topic_id(topic.id)
            else:
                px = PushWeixinTopics(cluster_title_to_show, cluster_title_str, cluster_articles_num, cluster_read_num,
                                      cluster_read_num_avg, topic_score, 0, 0, '', now_time, 0, 1)
                px.create()
                # 将所有与主题关联的文章更新topic_id
                for article in cluster_article_list:
                    article.update_topic_id(px.id)

    # 计算话题最终得分
    def count_score(self, cluster_read_num, cluster_read_num_avg, topic_sort):
        # 目前的计算公式为：（总阅读+平均阅读数*平均条数）*种类系数
        # 除以100是担心数目过大超过int，理论上的数字范围为10~1.5万
        print(cluster_read_num)
        print(cluster_read_num_avg)
        print(topic_sort)
        topic_sort_obj = AdminSort.query.filter_by(id=topic_sort).first()
        result = cluster_read_num + cluster_read_num_avg * cons.ARTICLES_NUM_1_CLUSTER * 5
        result_s = result * topic_sort_obj.sort_power
        result_f = result_s / 1000
        return int(result_f)

    # 分析话题分类
    def parse_topic_sort(self, obj_list):
        sort_list = []
        for obj in obj_list:
            sort_list.append(obj.sort)
        sort_obj = Counter(sort_list)
        sort_obj_ordered = sorted(sort_obj.items(), key=lambda x: x[1], reverse=True)
        return sort_obj_ordered[0][0]

    def cut_fake_local_name(self, biz_name, text):
        # 判断正文中是否包含公众号名称
        if biz_name in text:
            text_list = text.split(biz_name)
            return text_list[0]
        else:
            # 如果没有包含公众号名称，则直接砍断后10%内容，应为新闻中很少在文章结尾才指出地名
            cut_num = int(len(text) * 0.9)
            return text[:cut_num]