from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...views import InstaCrawlerView, DownloadCrawledImages
from ...models import CrawlerStats
import time
from uuid import uuid4


class Command(BaseCommand):
    help = 'Crawl an Instagram user'

    def __init__(self):
        BaseCommand.__init__(self)
        self.user_id = None

    def add_arguments(self, parser):
        parser.add_argument('insta_username', type=str,
                            help='Represents instagram username that will be crawled')
        parser.add_argument('username', type=str,
                            help='Represents username for login')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        insta_username = kwargs['insta_username']
        try:
            user = User.objects.get(username=username)
            self.user_id = user.id
            crawler_id = self._crawl_insta_user(insta_username, self.user_id)
            if crawler_id:
                self.stdout.write(self.style.SUCCESS(
                    f"Crawler ctarted with id: {crawler_id}"))
                status = self._check_crawl_status(crawler_id)
                if status == 'Completed':
                    self.stdout.write(self.style.SUCCESS(
                        f"Crawler completed sccessfully"))
                    download_images = DownloadCrawledImages()
                    zip_file_path = download_images.zip_images(
                        crawler_id, insta_username)
                    if zip_file_path:
                        self.stdout.write(self.style.SUCCESS(
                            f"Images zip is downloaded under following path:"))
                        self.stdout.write(self.style.MIGRATE_HEADING(
                            f"digital_benchmark/media/{str(insta_username)}"))
                    else:
                        self.stdout.write(self.style.ERROR(
                            "Error while zipping images"))
                elif status == 'Invalid_Profile':
                    self.stdout.write(self.style.ERROR(
                        "You entered an Invalid Instagram profile"))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f"No Django user exist with {username}"))

    def _crawl_insta_user(self, public_username, app_user_id):
        crawler = InstaCrawlerView()
        unique_id = str(uuid4())
        crawler_triggered = crawler.trigger_crawler(
            public_username, unique_id, app_user_id)
        if crawler_triggered:
            return unique_id
        return False

    def _check_crawl_status(self, crawler_id):
        status = None
        count = 0
        while True:
            count += 1
            self._print_dots(count)
            try:
                crawler_status = CrawlerStats.objects.get(unique_id=crawler_id)
                status = crawler_status.status
                if status == 'Invalid_Profile':
                    break
                elif status == 'Completed':
                    break
            except CrawlerStats.DoesNotExist:
                break
            time.sleep(4)
        return status

    def _print_dots(self, count):
        dots = ''
        for i in range(count):
            dots = f"{dots}."
        self.stdout.write(self.style.SUCCESS(dots))
