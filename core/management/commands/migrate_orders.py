import tracemalloc
from django.core.management.base import BaseCommand
from core.models import LegacyOrder, Orders, OrderLine

class Command(BaseCommand):
    help = 'Naive migration script for benchmarking memory failure.'

    def handle(self, *args, **options):
        self.stdout.write("Starting NAIVE migration. Monitoring memory...")

        tracemalloc.start()

        legacy_orders = LegacyOrder.objects.filter(migrated=False)
        
        count = 0
        for legacy_order in legacy_orders:
            count += 1
            if count >= 10000: 
                break 
                
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()

        top_stats = snapshot.statistics('lineno')

        self.stdout.write(self.style.ERROR("--- Top 3 Memory Hogs ---"))
        for stat in top_stats[:3]:
            self.stdout.write(str(stat))