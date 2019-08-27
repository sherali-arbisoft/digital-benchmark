from __future__ import absolute_import, unicode_literals
from celery import Task

import pickle

from digital_benchmark.celery import app

class FetchCommentReactionsTask(Task):
    def run(self, page_data_provider, comment, *args, **kwargs):
        self.page_data_provider = page_data_provider
        self.comment = comment
        return self.page_data_provider.get_post_reactions(self.comment.get('id'))
    
    def on_success(self, retval, task_id, args, kwargs):
        if 'error' in retval:
            print(retval.get('error').get('message'))
        else:
            reactions = retval
            self.comment['reactions'] = reactions
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('Error in fetching post comment reactions')

FetchCommentReactionsTask = app.register_task(FetchCommentReactionsTask())

class FetchPostCommentsTask(Task):
    def run(self, page_data_provider, post, *args, **kwargs):
        self.page_data_provider = page_data_provider
        self.post = post
        return self.page_data_provider.get_post_comments(self.post.get('id'))
    
    def on_success(self, retval, task_id, args, kwargs):
        if 'error' in retval:
            print(retval.get('error').get('message'))
        else:
            comments = retval
            self.post['comments'] = comments
            for comment in comments:
                fetch_comment_reactions_task = FetchCommentReactionsTask
                fetch_comment_reactions_task.delay(self.page_data_provider, comment)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('Error in fetching post comments')

FetchPostCommentsTask = app.register_task(FetchPostCommentsTask())

class FetchPostReactionsTask(Task):
    def run(self, page_data_provider, post, *args, **kwargs):
        self.page_data_provider = page_data_provider
        self.post = post
        return self.page_data_provider.get_post_reactions(self.post.get('id'))
    
    def on_success(self, retval, task_id, args, kwargs):
        if 'error' in retval:
            print(retval.get('error').get('message'))
        else:
            reactions = retval
            self.post['reactions'] = reactions

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('Error in fetching post reactions')

FetchPostReactionsTask = app.register_task(FetchPostReactionsTask())

class FetchPostsTask(Task):
    def run(self, page_data_provider, *args, **kwargs):
        self.page_data_provider = pickle.loads(page_data_provider)
        return self.page_data_provider.get_posts()
    
    def on_success(self, retval, task_id, args, kwargs):
        if 'error' in retval:
            print(retval.get('error').get('message'))
        else:
            posts = retval
            for post in posts:
                fetch_post_reaction_task = FetchPostReactionsTask
                fetch_post_reaction_task.delay(self.page_data_provider, post)
                fetch_post_comments_task = FetchPostCommentsTask
                fetch_post_comments_task.delay(self.page_data_provider, post)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('Error in fetching posts')

FetchPostsTask = app.register_task(FetchPostsTask())