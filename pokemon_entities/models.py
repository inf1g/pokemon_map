from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        default='покемон',
        help_text='Название покемона.'
    )
    photo = models.ImageField(
        upload_to='Pokemon',
        help_text='Картинка покемона',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        help_text='Название покемона.'
    )
    lat = models.FloatField(help_text='Широта местоположения покемона.')
    lon = models.FloatField(help_text='Долгота местоположения покемона.')
    appeared_at = models.DateTimeField(help_text='Появится в.', null=True, blank=True)
    disappeared_at = models.DateTimeField(help_text='Исчезнет в.', null=True, blank=True)
    level = models.IntegerField(help_text='Уровень.', null=True, blank=True)
    health = models.IntegerField(help_text='Здоровье', null=True, blank=True)
    attack = models.IntegerField(help_text='Атака', null=True, blank=True)
    defense = models.IntegerField(help_text='Защита', null=True, blank=True)
    stamina = models.IntegerField(help_text='Выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title} на ({self.lat}, {self.lon})'
