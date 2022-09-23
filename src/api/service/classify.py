from api.model.push import PushWeixinArticlesPool
from api.model.article import PushWeixinArticles
from api.model.ai import PushWeixinArticlesAi
import api.utils.constants as cons
import jieba
from jieba import analyse

class ClassifyService:
    def __init__(self):
        # 结巴分词关键词提取数量
        self.topk = 20


    def classify_article_by_keywords(self):
        print('in service classify_article_by_keywords')
        articles = PushWeixinArticlesPool.query.filter_by(sort=0).all()
        print(articles)
        for article in articles:
            article_type = self.keywords_filter(article)
            if article_type is not None:
                article.update_sort(article_type)
            else:
                # 无法硬分析的文章，状态更新为100，等待ai
                article.update_sort(100)
        return True

    def cut_fake_local_name(self, biz_name, text):
        # 先删除特定字词
        for del_word in cons.DEL_WORDS:
            text = text.replace(del_word, '')
        # 判断正文中是否包含公众号名称
        stop_words = cons.STOP_WORDS
        stop_words.append(biz_name)
        # 将常用停止词之前的内容砍掉
        text_cut = text
        for word in stop_words:
            text_cut_list = text_cut.split(word)
            text_cut = text_cut_list[0]
        # 如果没有包含公众号名称和停止词，则直接砍断后10%内容，应为新闻中很少在文章结尾才指出地名
        cut_num = int(len(text_cut) * 0.9)
        return text_cut[:cut_num]

    def keywords_filter(self, article):
        article_title = article.title
        # 先分析标题，如果能从标题判断出分类，则直接返回分类值
        # title_keywords = self.parse_article_title(article_title)
        # print("===============title cut words=======================")
        # for title_keyword in title_keywords:
        #     print(title_keyword)
        #     article_sort = self.get_sort_in_matrix(title_keyword)
        #     if article_sort is not None:
        #         return article_sort

        # 更换标题分析算法，只要关键词在标题中，即返回分类，简单粗暴！20220728
        print(article_title)
        print("===============title=======================")
        article_sort = self.get_title_sort_in_matrix(article_title)
        print(article_sort)
        if article_sort is not None:
            return article_sort

        # 如果标题无法判断出分类，则分析正文的关键词
        article_text = self.cut_fake_local_name(article.biz_name, article.text)
        text_keywords = self.parse_article_text(article_text)
        print("===============text key words=======================")
        for text_keyword in text_keywords:
            print(text_keyword)
            article_sort = self.get_sort_in_matrix(text_keyword)
            if article_sort is not None:
                return article_sort

        # 如果标题和正文都无法分析，则返回None，等待使用AI分析
        return None

    def get_key_words_from_title_and_text(self, article_title, article_text):
        title_keywords = self.parse_article_title(article_title)
        text_keywords = self.parse_article_text(article_text)
        for text_keyword in text_keywords:
            title_keywords.append(text_keyword)
        return ','.join(title_keywords)


    def make_sci_text(self):
        articles = PushWeixinArticlesPool.query.filter_by(sci_text='').all()
        for article in articles:
            text_cut = self.cut_fake_local_name(article.biz_name, article.text)
            text = self.get_key_words_from_title_and_text(article.title, text_cut)
            article.update_sci_text(text)
        return None

    def cut_fake_local_name(self, biz_name, text):
        # 判断正文中是否包含公众号名称
        if biz_name in text:
            text_list = text.split(biz_name)
            return text_list[0]
        else:
            # 如果没有包含公众号名称，则直接砍断后10%内容，应为新闻中很少在文章结尾才指出地名
            cut_num = int(len(text) * 0.9)
            return text[:cut_num]

    def parse_article_title(self, article_title):
        jieba.load_userdict("/var/www/html/flask_servers/local_news_parse/src/api/utils/dict.txt")
        title_cuts = jieba.cut(article_title)
        final_cut_words = self.del_stop_words(title_cuts)
        return final_cut_words

    def parse_article_text(self, article_text):
        # 使用停用词表
        jieba.analyse.set_stop_words('/var/www/html/flask_servers/local_news_parse/src/api/utils/stop_words.txt')
        jieba.load_userdict("/var/www/html/flask_servers/local_news_parse/src/api/utils/dict.txt")

        # 引入TF-IDF关键词抽取接口
        tfidf = analyse.extract_tags
        # 基于TF-IDF算法进行关键词抽取
        tfidf_keywords_list = tfidf(article_text, topK=self.topk)

        # 引入TextRank关键词抽取接口
        textrank = analyse.textrank

        # 基于TextRank算法进行关键词抽取
        textrank_keywords_list = textrank(article_text, topK=self.topk)
        # 输出抽取出的关键词
        # textrank_keywords = ','.join(textrank_keywords_list)

        # 将两种关键词提取的结果进行综合
        # 同时去除纯数字
        keywords_final = []
        for tfidf_keyword in tfidf_keywords_list:
            if tfidf_keyword.isdigit():
                pass
            else:
                keywords_final.append(tfidf_keyword)

        for textrank_keyword in textrank_keywords_list:
            if textrank_keyword.isdigit():
                pass
            else:
                keywords_final.append(textrank_keyword)

        # 关键词去重
        keywords_final = list(set(keywords_final))
        if len(keywords_final) > 20:
            return keywords_final[:20]
        else:
            return keywords_final

    def get_sort_in_matrix(self, word):
        # 遍历二维数组matrix，返回分类值
        matrix = cons.KEYWORDS_MATRIX
        matrix_length = len(matrix)
        for i in range(0, matrix_length):
            if word in matrix[i]:
                return i
        return None

    def get_title_sort_in_matrix(self, title):
        matrix = cons.KEYWORDS_MATRIX
        matrix_length = len(matrix)
        for i in range(0, matrix_length):
            for key_word in matrix[i]:
                if key_word in title:
                    return i
        return None

    def del_stop_words(self, cut_words):
        final_words = []
        stop_words_list = self.get_stop_words_list()
        for word in cut_words:
            if word not in stop_words_list:
                final_words.append(word)
        return final_words

    # 创建停用词列表
    def get_stop_words_list(self):
        url = '/var/www/html/flask_servers/local_news_parse/src/api/utils/stop_words.txt'
        stopwords = [line.strip() for line in open(url, encoding='UTF-8').readlines()]
        return stopwords

    def make_sci_db(self):
        # 将刚刚推送的文章(status=2)同步到AI数据库中，以便于后面进行语义分析
        articles = PushWeixinArticles.query.filter_by(status=2).all()
        print(len(articles))
        for article in articles:
            id = article.id
            a = PushWeixinArticlesAi.query.filter_by(article_id=id).all()
            if a is not None:
                article_keywords = self.parse_article_keywords(article)
                ai = PushWeixinArticlesAi(id, article_keywords, article.article_sort, 0, 1)
                ai.create()
                # 将转移至ai数据库之后的文章，状态更新为3
                article.update_status(3)
        return True

    # 根据分析算法，拟将标题与正文合并，返回到ai数据库中，使用m1继续处理
    def parse_article_keywords(self, article):
        article_title = article.title
        article_text = article.text
        text = article_title + article_text
        return text
