from django.core.management.base import BaseCommand
from django.utils import timezone
from website.models import Cart

class Command(BaseCommand):
    help = 'Clean up old cart items'

    def handle(self, *args, **options):
        one_month_ago = timezone.now() - timezone.timedelta(days=30)
        Cart.objects.filter(created_at__lt=one_month_ago).delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleaned old cart items.'))
