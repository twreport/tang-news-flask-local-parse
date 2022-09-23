from api.service.parse import ParseService

class ParseController:
    def parse_article(self):
        parse = ParseService()
        result = parse.parse_article()
        return result

    def count_avg_of_bizs(self):
        parse = ParseService()
        result = parse.count_avg_of_bizs()
        return result

    def scan_articles(self):
        parse = ParseService()
        result = parse.scan_articles()
        return result