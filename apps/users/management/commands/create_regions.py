from django.core.management.base import BaseCommand
from apps.users.models import Region


class Command(BaseCommand):
    help = 'Создает тестовые регионы'

    def handle(self, *args, **options):
        regions_data = [
            {'name': 'Алматы', 'code': 'ALM'},
            {'name': 'Астана', 'code': 'AST'},
            {'name': 'Шымкент', 'code': 'SHM'},
            {'name': 'Актобе', 'code': 'AKT'},
            {'name': 'Тараз', 'code': 'TAR'},
            {'name': 'Павлодар', 'code': 'PAV'},
            {'name': 'Усть-Каменогорск', 'code': 'UKG'},
            {'name': 'Семей', 'code': 'SEM'},
            {'name': 'Костанай', 'code': 'KOS'},
            {'name': 'Кызылорда', 'code': 'KYZ'},
        ]
        
        created_count = 0
        for region_data in regions_data:
            region, created = Region.objects.get_or_create(
                code=region_data['code'],
                defaults={'name': region_data['name']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Создан регион: {region.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Создано регионов: {created_count}')
        )
