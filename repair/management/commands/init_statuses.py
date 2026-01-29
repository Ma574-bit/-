from django.core.management.base import BaseCommand
from repair.models import Status

class Command(BaseCommand):
    help = 'Initialize status data'

    def handle(self, *args, **options):
        statuses = ['รอซ่อม', 'กำลังซ่อม', 'ซ่อมเสร็จ', 'ซ่อมเสร็จแล้ว']
        
        for status_name in statuses:
            status, created = Status.objects.get_or_create(name=status_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ สร้าง Status: {status_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ Status มีอยู่แล้ว: {status_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('✅ เสร็จสิ้นการเตรียมข้อมูล')
        )
