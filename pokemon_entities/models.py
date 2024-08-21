from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, default='покемон', help_text='Название покемона.')
    photo = models.ImageField(upload_to='Pokemon', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    lat = models.FloatField(max_length=200)
    lon = models.FloatField(max_length=200)

    def __str__(self):
        return f'{self.lat} {self.lon}'
