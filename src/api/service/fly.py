# 本模块负责上传推荐文章到tangwei.cc云端
# from api.model.article import PushWeixinArticles
from api.model.ai import PushWeixinArticlesAi
import csv

class FlyService:
    def __init__(self):
        pass

    def fly_test(self):
        articles = PushWeixinArticlesAi.query.all()
        news_dataset_train_fc_articles = []
        news_dataset_val_fc_articles = []
        news_dataset_test_fc_articles = []

        all_num = len(articles)
        for i in range(all_num):
            y = i % 4
            if y < 2:
                news_dataset_train_fc_articles.append(articles[i])
            elif y < 3:
                news_dataset_val_fc_articles.append(articles[i])
            else:
                news_dataset_test_fc_articles.append(articles[i])

        self.write_csv('news_dataset_train_fc.csv', news_dataset_train_fc_articles)
        self.write_csv('news_dataset_val_fc.csv', news_dataset_val_fc_articles)
        self.write_csv('news_dataset_test_fc.csv', news_dataset_test_fc_articles)
        news_dataset_train_fc_articles
        return {'result': True}

    def write_csv(self, filename, articles):
        header = ['label', 'content']
        data = []
        for article in articles:
            if article.article_sort is not None:
                data.append((article.article_sort, article.article_keywords))
            else:
                data.append((0, article.article_keywords))
        with open(filename, 'w', encoding='utf-8') as file_obj:
            # 1:创建writer对象
            writer = csv.writer(file_obj)
            # 2:写表头
            writer.writerow(header)
            # 3:遍历列表，将每一行的数据写入csv
            for p in data:
                writer.writerow(p)