from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):

    JANTINA = (
        ('Lelaki','Lelaki'),
        ('Perempuan', 'Perempuan')
    )

    CAWANGAN = (
        ('SHAH ALAM', 'SHAH ALAM'),
        ('PUNCAK ALAM', 'PUNCAK ALAM'),
        ('PUNCAK PERDANA', 'PUNCAK PERDANA'),
        ('SUNGAI BULOH', 'SUNGAI BULOH'),
        ('DENGKIL', 'DENGKIL'),
        ('SERI ISKANDAR', 'SERI ISKANDAR'),
        ('TAPAH', 'TAPAH'),
        ('SEGAMAT', 'SEGAMAT'),
        ('PASIR GUDANG', 'PASIR GUDANG'),
        ('SUNGAI PETANI', 'SUNGAI PETANI'),
        ('MACHANG', 'MACHANG'),
        ('KOTA BHARU', 'KOTA BHARU'),
        ('ALOR GAJAH', 'ALOR GAJAH'),
        ('BANDARAYA MELAKA', 'BANDARAYA MELAKA'),
        ('JASIN', 'JASIN'),
        ('KUALA PILAH', 'KUALA PILAH'),
        ('SEREMBAN', 'SEREMBAN'),
        ('REMBAU', 'REMBAU'),
        ('JENGKA', 'JENGKA'),
        ('RAUB', 'RAUB'),
        ('KUANTAN', 'KUANTAN'),
        ('PERMATANG PAUH', 'PERMATANG PAUH'),
        ('BERTAM', 'BERTAM'),
        ('ARAU', 'ARAU'),
        ('KUALA TERENGGANU', 'KUALA TERENGGANU'),
        ('BUKIT BESI', 'BUKIT BESI'),
        ('DUNGUN', 'DUNGUN'),
        ('KOTA KINABALU', 'KOTA KINABALU'),
        ('TAWAU', 'TAWAU'),
        ('SAMARAHAN 2', 'SAMARAHAN 2'),
        ('MUKAH', 'MUKAH'),
        ('Lain - Lain', 'Lain - Lain'),

    )

    FAKULTI = (
        ('FAKULTI FARMASI', 'FAKULTI FARMASI'),
        ('FAKULTI PERLADANGAN & AGROTEKNOLOGI', 'FAKULTI PERLADANGAN & AGROTEKNOLOGI'),
        ('FAKULTI SAINS KESIHATAN', 'FAKULTI SAINS KESIHATAN'),
        ('KOLEJ PENGAJIAN ALAM BINA', 'KOLEJ PENGAJIAN ALAM BINA'),
        ('KOLEJ PENGAJIAN KEJURUTERAAN', 'KOLEJ PENGAJIAN KEJURUTERAAN'),
        ('FAKULTI PERUBATAN', 'FAKULTI PERUBATAN'),
        ('KOLEJ PENGAJIAN PENGKOMPUTERAN, INFORMATIK & MATEMATIK', 'KOLEJ PENGAJIAN PENGKOMPUTERAN, INFORMATIK & MATEMATIK'),
        ('FAKULTI PERGIGIAN', 'FAKULTI PERGIGIAN'),
        ('FAKULTI SAINS GUNAAN', 'FAKULTI SAINS GUNAAN'),
        ('FAKULTI SAINS SUKAN & REKREASI', 'FAKULTI SAINS SUKAN & REKREASI'),
        ('KOLEJ PENGAJIAN SENI KREATIF', 'KOLEJ PENGAJIAN SENI KREATIF'),
        ('FAKULTI SAINS PENTADBIRAN & PENGAJIAN POLISI', 'FAKULTI SAINS PENTADBIRAN & PENGAJIAN POLISI'),
        ('FAKULTI KOMUNIKASI & PENGAJIAN MEDIA', 'FAKULTI KOMUNIKASI & PENGAJIAN MEDIA'),
        ('FAKULTI UNDANG-UNDANG', 'FAKULTI UNDANG-UNDANG'),
        ('FAKULTI PENDIDIKAN', 'FAKULTI PENDIDIKAN'),
        ('FAKULTI PENGURUSAN & PERNIAGAAN', 'FAKULTI PENGURUSAN & PERNIAGAAN'),
        ('FAKULTI PENGURUSAN HOTEL & PELANCONGAN', 'FAKULTI PENGURUSAN HOTEL & PELANCONGAN'),
        ('FAKULTI PERAKAUNAN', 'FAKULTI PERAKAUNAN'),
        ('Lain - Lain', 'Lain - Lain'),
    )

    BANGSA = (
        ('Melayu','Melayu'),
        ('Cina','Cina'),
        ('India','India'),
        ('Sabah','Sabah'),
        ('Sarawak','Sarawak'),
        ('Lain-Lain','Lain-Lain'),
    )

    # STATUS = (
    #     ('Menunggu Kelulusan','Menunggu Kelulusan'),
    #     ('Ahli MITASA','Ahli MITASA'),
    # )
    STATUS = (
    ('Not a Member', 'Not a Member'),
    ('New Member', 'New Member'),
    ('Member', 'Member'),
    ('Anomaly', 'Anomaly')
)

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)
    nama = models.CharField(max_length=200, null=True)
    noPekerja = models.CharField(max_length=50, null=True)
    fakulti = models.CharField(max_length=200, null=True, choices=FAKULTI)
    email = models.CharField(max_length=200, null=True)
    tarikhLahir = models.DateField(null=True)
    noIC = models.CharField(max_length=200, null=True)
    noTel = models.CharField(max_length=200, null=True)
    cawangan = models.CharField(max_length=200, null=True, choices=CAWANGAN)
    alamat = models.CharField(max_length=200, null=True)
    tarikhPencen = models.DateField(null=True)
    namaPW = models.CharField(max_length=200, null=True)
    noTelPW = models.CharField(max_length=200, null=True)
    emailAlt = models.CharField(max_length=200, null=True)
    jantina = models.CharField(max_length=200, null=True, choices=JANTINA)
    bangsa = models.CharField(max_length=200, null=True, choices=BANGSA)
    jbtnPTJ = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default='Waiting for Approval', blank=True)

    def clean(self):
        if self.nama:
            self.nama = self.nama.upper()
        if self.namaPW:
            self.namaPW = self.namaPW.upper()
        if self.namaPW:
            self.alamat = self.alamat.upper()
        if self.email:
            self.email = self.email.lower()

    def save(self, *args, **kwargs):
        if self.user:
            self.noPekerja = self.user.username
        self.clean()  # Ensure clean is called before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.nama)
    
class MemberFee(models.Model):
    member = models.ForeignKey(Member, null=True, on_delete=models.CASCADE, related_name='fees', blank=True)
    kod = models.CharField(max_length=200, null=True, blank=True)
    jbtn = models.CharField(max_length=200, null=True, blank=True)
    keterangan = models.CharField(max_length=200, null=True, blank=True)
    noPekerja = models.CharField(max_length=200, null=True, blank=True)
    nama = models.CharField(max_length=200, null=True, blank=True)
    noIC = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True )
    date = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.nama} - {self.amount} on {self.date}"

