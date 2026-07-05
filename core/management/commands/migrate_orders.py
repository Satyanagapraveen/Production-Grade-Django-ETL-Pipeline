import time
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import LegacyOrder, Order, OrderLine

class Command(BaseCommand):
    help = 'Migrates legacy orders to the new normalized schema using batched iterators.'

    def add_arguments(self, parser):
        parser.add_argument('--batch-size', type=int, default=1000)
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--start-from', type=str)

    def handle(self, *args, **options):
        start_time = time.perf_counter()
        
        batch_size = options['batch_size']
        dry_run = options['dry_run']
        start_from = options['start_from']

        self.stdout.write(f"Starting optimized migration... Batch size: {batch_size}")

        queryset = LegacyOrder.objects.filter(migrated=False).order_by('external_id')
        if start_from:
            queryset = queryset.filter(external_id__gte=start_from)

        orders_to_create = []
        lines_to_create = []
        processed_ids = []
        
        records_processed = 0

        for legacy_order in queryset.iterator(chunk_size=batch_size):
            raw = legacy_order.raw_data
            
            new_order = Order(
                external_id=legacy_order.external_id,
                customer_email=raw['customer_email'],
                total=Decimal(raw['total'])
            )
            orders_to_create.append(new_order)
            processed_ids.append(legacy_order.id)

            for item in raw['items']:
                new_line = OrderLine(
                    order=new_order, 
                    sku=item['sku'],
                    quantity=item['quantity'],
                    unit_price=Decimal(item['unit_price'])
                )
                lines_to_create.append(new_line)
                
            records_processed += 1
            
            if len(orders_to_create) >= batch_size:
                self.stdout.write(f"Buffer full. Ready to process batch of {len(orders_to_create)}...")
                # self.process_batch(...) will go here
                orders_to_create = []
                lines_to_create = []
                processed_ids = []

        self.stdout.write(self.style.SUCCESS(f"Extraction tested. Total records iterated: {records_processed}"))