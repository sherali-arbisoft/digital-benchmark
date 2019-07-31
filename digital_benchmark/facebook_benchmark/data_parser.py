from django.conf import settings

from .models import Page

class FacebookDataParser:

    def parse_page_details_and_insights(self, page_response, page_insights_response):
        page = Page()
        page.displayed_message_response_time = page_response.get('displayed_message_response_time', '')
        page.num_engagements = page_response.get('engagement', {}).get('count', 0)
        page.fan_count = page_response.get('fan_count', 0)
        page.name = page_response.get('name', '')
        page.overall_start_rating = page_response.get('overall_start_rating', 0)
        page.page_id = page_response.get('id', '')
        page.rating_count = page_response.get('rating_count', 0)
        page.talking_about_count = page_response.get('talking_about_count', 0)
        page.unread_message_count = page_response.get('unread_message_count', 0)
        page.unread_notif_count = page_response.get('unread_notif_count', 0)
        page.unseen_message_count = page_response.get('unseen_message_count', 0)
        page.verification_status = page_response.get('verification_status', 'not_verified')
        for item in page_insights_response['data']:
            setattr(page, item['name'], item['values'][0]['value'])
        return page