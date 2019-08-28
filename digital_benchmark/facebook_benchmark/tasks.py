from __future__ import absolute_import, unicode_literals
from celery import Task
import logging

from digital_benchmark.celery import app
from .data_provider import FacebookPageDataProvider
from .data_parser import FacebookPageDataParser
from .models import Post

class FetchPostCommentsTask(Task):
    def run(self, page_access_token, facebook_profile_id, page_id, post_id):
        self.facebook_profile_id = facebook_profile_id
        self.page_id = page_id
        self.page_access_token = page_access_token
        self.post_id = post_id

        facebook_page_data_provider = FacebookPageDataProvider(page_access_token=self.page_access_token)
        post = Post.objects.get(pk=self.post_id)
        return facebook_page_data_provider.get_post_comments(post.post_id)
    
    def on_success(self, retval, task_id, args, kwargs):
        if 'error' in retval:
            logger = logging.getLogger(__name__)
            logger.error(retval.get('error').get('message'))
        else:
            comments_response = retval
            facebook_page_data_parser = FacebookPageDataParser(self.facebook_profile_id, self.page_id)
            for comment_response in comments_response:
                facebook_page_data_parser.parse_comment(self.post_id, comment_response)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = logging.getLogger(__name__)
        logger.error('Error in fetching post comments')

FetchPostCommentsTask = app.register_task(FetchPostCommentsTask())

class FetchPostsTask(Task):
    def run(self, page_access_token, facebook_profile_id, page_id):
        self.page_access_token = page_access_token
        self.facebook_profile_id = facebook_profile_id
        self.page_id = page_id

        facebook_page_data_provider = FacebookPageDataProvider(page_access_token=self.page_access_token)
        return facebook_page_data_provider.get_posts()
    
    def on_success(self, retval, task_id, args, kwargs):
        if 'error' in retval:
            logger = logging.getLogger(__name__)
            logger.error(retval.get('error').get('message'))
        else:
            posts_response = retval
            facebook_page_data_parser = FacebookPageDataParser(self.facebook_profile_id, self.page_id)
            for post_response in posts_response:
                post = facebook_page_data_parser.parse_post(post_response)
                fetch_post_comments_task = FetchPostCommentsTask
                fetch_post_comments_task.delay(self.page_access_token, self.facebook_profile_id, self.page_id, post.id)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = logging.getLogger(__name__)
        logger.error('Error in fetching posts')

FetchPostsTask = app.register_task(FetchPostsTask())