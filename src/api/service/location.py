from api.model.push import PushWeixinArticlesPool
import api.utils.constants as cons
import jieba
from jieba import analyse

class LocationService:
    def __init__(self):
        pass

    def parse_article_location(self):
        # 取出所有未分析地名的文章
        articles = PushWeixinArticlesPool.query.filter_by(is_local=0).all()
        print('=======Articles to Location========')
        print(articles)
        for article in articles:
            print('---in location one-------')
            print(article)
            # 直接分析标题
            title_locations = self.get_locations_by_title(article.title)
            # 将正文中的结尾砍断（避免出现非本地新闻因为含有biz_name而被误认为本地新闻）
            text = self.cut_fake_local_name(article.biz_name, article.text)
            text_locations = self.get_locations_by_title(text)
            final_location = self.merge_locations_by_title_and_text(title_locations, text_locations)
            final_location_str = '|'.join(final_location)
            article.update_location(final_location_str)
            if cons.CURRENT_REGION in final_location_str:
                is_local = 1
            else:
                is_local = 2
            article.update_is_local(is_local)
        return None

    # 首先匹配标题
    # 1-有没有省市自治区名字
    # 2-分析地级行政区名字
    # 3-分析县级行政区名字
    def get_locations_by_title(self, title):
        locations = []
        # jieba.load_userdict("/var/www/html/flask_servers/src/api/utils/dict.txt")
        title_cuts = jieba.cut(title)
        toponym = cons.DOMESTIC_LOCATION_3

        for title_cut in title_cuts:
            for r1 in toponym:
                if title_cut in r1["name"]:
                    locations.append(r1["name"][0])
                for r2 in r1["cityList"]:
                    if title_cut in r2["name"]:
                        locations.append(r1["name"][0] + '-' + r2["name"][0])
                        for r3 in r2["areaList"]:
                            if title_cut in r3["name"]:
                                locations.append(r1["name"][0] + '-' + r2["name"][0] + '-' + r3["name"][0])

        if len(locations) > 0:
            # 对地名数据去重
            locations = list(set(locations))
            return locations
        else:
            return None

    def get_locations_by_text(self, text):
        locations = []
        toponym = cons.DOMESTIC_LOCATION_3
        # jieba.load_userdict("/var/www/html/flask_servers/src/api/utils/dict.txt")
        text_cuts = jieba.cut(text)
        for text in text_cuts:
            for r1 in toponym:
                if text in r1["name"]:
                    locations.append(r1["name"][0])
                for r2 in r1["cityList"]:
                    if text in r2["name"]:
                        locations.append(r1["name"][0] + '-' + r2["name"][0])
                    for r3 in r2["areaList"]:
                        if text in r3["name"]:
                            locations.append(r1["name"][0] + '-' + r2["name"][0] + '-' + r3["name"][0])

        if len(locations) > 0:
            # 对地名数据去重
            locations = list(set(locations))
            return locations
        else:
            return None

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


    def merge_locations_by_title_and_text(self, title_location, text_location):
        if title_location is None and text_location is None:
            return []
        elif title_location is None:
            return text_location
        elif text_location is None:
            return title_location
        else:
            final_location = []
            for title in title_location:
                if title not in final_location:
                    final_location.append(title)
                for text in text_location:
                    if text not in final_location:
                        final_location.append(text)
            return final_location


    # 只返回省级地名的函数，暂未使用
    def get_region1_locations_str(self, title_locations, text_locations):
        # 如果在标题中检测出了地名，直接返回标题中的地名
        if title_locations is not None:
            region1 = []
            for title_location in title_locations:
                if '-' in title_location:
                    temp_region = title_location.split('-')
                    region1.append(temp_region[0])
                else:
                    region1.append(title_location)
            region1 = list(set(region1))
            return ','.join(region1)
        # 如果标题中没有检测出地名，则在正文中寻找，只返回省级地名
        elif text_locations is not None:
            region1 = []
            region1_2 = []
            # 先将正文中出现的1级省级区划和2级省级区划分成两个list：
            for text_location in text_locations:
                if '-' not in text_location:
                    region1.append(text_location)
                else:
                    region1_2.append(text_location)
                    temp_region = text_location.split('-')
                    region1.append(temp_region[0])
            print("region1", region1)
            print("region1_2", region1_2)
            # 暂时只返回省级区域地名
            region1 = list(set(region1))
            return ','.join(region1)
        else:
            return None