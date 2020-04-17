from django.db import models

class XRay(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='x_ray_images', null=False, blank=False, default=None)

    def __str__(self):
        return 'X-Ray object (ID {})'.format(self.id)