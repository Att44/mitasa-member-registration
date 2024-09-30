from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Member, MemberFee
import uuid


class MemberResource(resources.ModelResource):
    class Meta:
        model = Member
        fields = ['nama', 'noPekerja','fakulti','email','tarikhLahir','noIC','noTel','cawangan','alamat','tarikhPencen','namaPW','noTelPW','emailAlt','jantina','bangsa','jbtnPTJ','status',]


class MemberFeeResource(resources.ModelResource):
    processed_noPekerja = set()
    member = fields.Field(
        column_name='noPekerja',
        attribute='member',
        widget=ForeignKeyWidget(Member, 'noPekerja')
    )

    class Meta:
        model = MemberFee
        fields = ('id', 'member', 'kod', 'jbtn', 'keterangan', 'noPekerja', 'nama', 'noIC', 'amount', 'date')
        import_id_fields = ('id',)

    def before_import_row(self, row, **kwargs):
        noPekerja = row.get('noPekerja')
        amount = row.get('amount')
        self.processed_noPekerja.add(noPekerja)
        try:
            member = Member.objects.get(noPekerja=noPekerja)
            if amount in [5, 6]:
                member.status = 'Member'
            elif amount == 16:
                member.status = 'New Member'
            member.save()
        except Member.DoesNotExist:
            pass