from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from member.models import Member

class Command(BaseCommand):
    help = 'Create user accounts for members without a user and assign them to the "member" group'

    def handle(self, *args, **kwargs):
        members = Member.objects.filter(user__isnull=True)
        for member in members:
            self.create_user_for_member(member)
        self.stdout.write(self.style.SUCCESS('Successfully created user accounts for members and assigned them to the "member" group'))

    def create_user_for_member(self, member):
        user = User.objects.create_user(
            username=member.noPekerja,
            password= member.noPekerja  # Set a secure password or handle password setting separately
        )
        
        # Assign the user to the 'member' group
        member_group = Group.objects.get(name='member')
        user.groups.add(member_group)
        
        member.user = user
        member.save()