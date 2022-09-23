from api.service.classify import ClassifyService

class ClassifyController:
    def classify_article_by_keywords(self):
        classify = ClassifyService()
        result = classify.classify_article_by_keywords()
        return result

    def make_sci_db(self):
        classify = ClassifyService()
        result = classify.make_sci_db()
        return result

    def make_sci_text(self):
        classify = ClassifyService()
        result = classify.make_sci_text()
        return result