from django.db import models
from django.contrib.auth.models import User


# Create your models here.

CAMBODIAN_PROVINCES = [
    ('Banteay Meanchey', 'Banteay Meanchey'),
    ('Battambang', 'Battambang'),
    ('Kampong Cham', 'Kampong Cham'),
    ('Kampong Chhnang', 'Kampong Chhnang'),
    ('Kampong Speu', 'Kampong Speu'),
    ('Kampong Thom', 'Kampong Thom'),
    ('Kampot', 'Kampot'),
    ('Kandal', 'Kandal'),
    ('Koh Kong', 'Koh Kong'),
    ('Kratie', 'Kratie'),
    ('Mondulkiri', 'Mondulkiri'),
    ('Phnom Penh', 'Phnom Penh'),
    ('Preah Vihear', 'Preah Vihear'),
    ('Prey Veng', 'Prey Veng'),
    ('Pursat', 'Pursat'),
    ('Ratanakiri', 'Ratanakiri'),
    ('Siem Reap', 'Siem Reap'),
    ('Preah Sihanouk', 'Preah Sihanouk'),
    ('Stung Treng', 'Stung Treng'),
    ('Svay Rieng', 'Svay Rieng'),
    ('Takeo', 'Takeo'),
    ('Oddar Meanchey', 'Oddar Meanchey'),
    ('Kep', 'Kep'),
    ('Pailin', 'Pailin'),
    ('Tboung Khmum', 'Tboung Khmum'),
]

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=50, choices=CAMBODIAN_PROVINCES, null=True)
    phone = models.CharField(max_length=20, null=True)
    address_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address1}, {self.city}, {self.province}"

    class Meta:
        verbose_name_plural = "Addresses"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    pfp = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username


