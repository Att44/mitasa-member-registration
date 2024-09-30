from django.core.management.base import BaseCommand
from member.models import Member, MemberFee

class Command(BaseCommand):
    help = 'Assign MemberFee instances to the corresponding Member based on noPekerja'

    def handle(self, *args, **kwargs):
        member_fees = MemberFee.objects.filter(member__isnull=True)
        for fee in member_fees:
            try:
                member = Member.objects.get(noPekerja=fee.noPekerja)
                fee.member = member
                fee.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully assigned fee {fee.id} to member {member.nama}'))
            except Member.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'No member found with noPekerja {fee.noPekerja} for fee {fee.id}'))