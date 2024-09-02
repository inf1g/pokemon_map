from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(
        max_length=200,
        default='покемон',
        verbose_name='Название покемона на русском.'
    )
    title_en = models.CharField(
        max_length=200,
        default='покемон',
        verbose_name='Название покемона на английском.',
        null=True,
        blank=True
    )
    title_jp = models.CharField(
        max_length=200,
        default='покемон',
        verbose_name='Название покемона на японском.',
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='Pokemon',
        verbose_name='Картинка покемона',
        null=True,
        blank=True
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='эволюции для покемона',
        related_name='next_evolutions'
    )
    description = models.TextField(
        blank=True,
        verbose_name='описание покемона'
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='Название покемона.'
    )
    lat = models.FloatField(verbose_name='Широта местоположения покемона.')
    lon = models.FloatField(verbose_name='Долгота местоположения покемона.')
    appeared_at = models.DateTimeField(verbose_name='Появится в.', null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет в.', null=True, blank=True)
    level = models.IntegerField(verbose_name='Уровень.', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    attack = models.IntegerField(verbose_name='Атака', null=True, blank=True)
    defense = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon} на ({self.lat}, {self.lon})'
