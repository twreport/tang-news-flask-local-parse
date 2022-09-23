from api.model.test import Test
from api.service.parse import ParseService

class TestController:
    def get_test_list(self):
        query = Test.objects()
        for q in query:
            print(q.test)
        return query

    def test_push_article(self):
        parse = ParseService()
        result = parse.test_push_article()
        return result

    def check_status(self):
        return 'Flask Service local_news_parse is OK!'