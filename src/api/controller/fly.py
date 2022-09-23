# 本模块负责使用人工智能技术，将初步push和分类的推荐文章
# 使用语义分析精分类
# 给予最终评分
# 将
# 便于eggjs_parse最终将文章上传到tangwei.cc云端
from api.service.fly import FlyService

class FlyController:
    def fly_test(self):
        fly = FlyService()
        result = fly.fly_test()
        return result