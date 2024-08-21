from django.db import models  # noqa F401


class Pokemon(models.Model):
    description = models.TextField(max_length=200, help_text='Описание покемона.')
    title = models.CharField(max_length=200, help_text='Название покемона.')
    created_date = models.DateTimeField()

    def __str__(self):
        return f'{self.description} {self.title} {self.created_date}'
