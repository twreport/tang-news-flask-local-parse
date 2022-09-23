from api.service.location import LocationService

class LocationController:
    def parse_article_location(self):
        los = LocationService()
        result = los.parse_article_location()
        return result