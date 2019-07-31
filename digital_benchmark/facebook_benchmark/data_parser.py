from django.conf import settings
from django.utils import timezone

from .models import Page

class FacebookDataParser:

    def parse_page_details_and_insights(self, page_response, page_insights_response):
        page = Page()
        for key in settings.FACEBOOK_DEFAULT_FIELDS_FOR_PAGE:
            setattr(page, key, page_response.get(key, ''))
        page.id = ''
        page.page_id = page_response['id']
        page.engagement = page_response['engagement']['count']
        for key in settings.FACEBOOK_DEFAULT_METRICES_FOR_PAGE_INSIGHTS:
            items = [item for item in page_insights_response if item.get('name', '') == key]
            if len(items) > 0:
                setattr(page, key, items[0]['values'][0]['value'])
        return page