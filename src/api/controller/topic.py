from api.service.topic import TopicService

class TopicController:
    def make_cluster(self):
        topic = TopicService()
        result = topic.make_cluster()
        return result
