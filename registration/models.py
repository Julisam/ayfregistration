from django.db import models

class Participant(models.Model):
    ARCHDEACONRY_CHOICES = [
        ('Ago-Iwoye', 'Ago-Iwoye'),
        ('Ago-South', 'Ago-South'),
        ('Oru', 'Oru'),
        ('Awa', 'Awa'),
        ('Ifelodun', 'Ifelodun'),
        ('Cathedral', 'Cathedral'),
        ('Ojowo', 'Ojowo'),
        ('Oke-Sopin', 'Oke-Sopin'),
        ('Oke-Agbo', 'Oke-Agbo'),
        ('Atikori', 'Atikori'),
        ('Japara', 'Japara'),
    ]
    
    ROLE_CHOICES = [
        ('Director', 'Director'),
        ('DeputyDirector', 'Deputy Director'),
        ('Chaplain', 'Chaplain'),
        ('Special Guest', 'Special Guest'),
        ('Vendor', 'Vendor'),
        ('Delegate', 'Delegate'),
        ('Leader', 'Leader'),
        ('Executive', 'Executive'),
    ]

    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=False, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    parish = models.CharField(max_length=100)
    archdeaconry = models.CharField(max_length=100, choices=ARCHDEACONRY_CHOICES)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    photo = models.ImageField(upload_to='photos/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    room_no = models.PositiveBigIntegerField(blank=True, null=True)
    camp_id = models.PositiveBigIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name.strip()} {self.last_name.upper()}"
    
    @property
    def room_label(self):
        if self.room_no:
            prefix = 'MH' if self.gender == 'Male' else 'FH'
            return f"{prefix}{self.room_no:02d}"
        return None
    
    @property
    def camp_label(self):
        if self.camp_id:
            CAMPERS = ['Executive', 'Leader', 'Delegate']
            prefix = 'C' if self.role in CAMPERS else 'G'
            return f"{prefix}{self.camp_id:03d}"
        return None
    
    def save(self, *args, **kwargs):
        CAMPERS = ['Executive', 'Leader', 'Delegate']
        
        if not self.camp_id:
            if self.role in CAMPERS:
                # Get next C serial number
                last_camper = Participant.objects.filter(role__in=CAMPERS).order_by('camp_id').last()
                self.camp_id = (last_camper.camp_id if last_camper else 0) + 1
            else:
                # Get next G serial number
                last_guest = Participant.objects.exclude(role__in=CAMPERS).order_by('camp_id').last()
                self.camp_id = (last_guest.camp_id if last_guest else 0) + 1
        
        if not self.room_no and self.role in CAMPERS:
            same_gender_count = Participant.objects.filter(gender=self.gender, role__in=CAMPERS).count()
            self.room_no = (same_gender_count % 10) + 1
        
        super().save(*args, **kwargs)