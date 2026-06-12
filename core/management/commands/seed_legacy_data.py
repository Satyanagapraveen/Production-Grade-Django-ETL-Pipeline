import uuid
import random
from django.core.management.base import BaseCommand
from core.models import LegacyOrder
class Command(BaseCommand):
    help='Seeds the database with 500,000 legacy orders'
    def handle(self,*args, **options):
        self.stdout.write("sttarting to seed database")
        batch_size=10000
        total_records=500000
        for i in range(0,total_records,batch_size):
            orders_to_create=[]
            for j in range(batch_size):
                ext_id=f"legacy-{uuid.uuid4()}"
                raw_data={
                    "customer_email":f"user_{i+j}@example.com",
                    "total":str(random.randint(50,100))+".99",
                    "items":[
                    {
                        "sku":f"sku-{random.randint(100,999)}",
                        "quantity":random.randint(1,5),
                        "unit_price":str(random.randint(50,100))+".99"
                    }
                    ]
                }
                new_legacy_order=LegacyOrder(external_id=ext_id,raw_data=raw_data)
                orders_to_create.append(new_legacy_order)
            LegacyOrder.objects.bulk_create(orders_to_create)
            self.stdout.write(f"Inserted {i+batch_size} records ...")
        self.stdout.write(self.style.SUCCESS("successfully seeded 500,000 records!"))


