from django.conf import settings
from django.utils import timezone

from . import models

class FacebookDataParser:

    def parse_page_details_and_insights(self, page_response, page_insights_response):
        page = models.Page()
        page.created_at = timezone.now()
        page.updated_at = timezone.now()
        for key in settings.FACEBOOK_DEFAULT_FIELDS_FOR_PAGE:
            setattr(page, key, page_response.get(key, ''))
        page.engagement = page_response['engagement']['count']
        for key in settings.FACEBOOK_DEFAULT_METRICES_FOR_PAGE_INSIGHTS:
            items = [item for item in page_insights_response if item.get('name', '') == key]
            if len(items) > 0:
                setattr(page, key, items[0]['values'][0]['value'])
        return page