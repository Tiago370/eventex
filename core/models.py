from django.db import models
from django.shortcuts import resolve_url as r

class Speaker(models.Model):
    name = models.CharField('nome', max_length=225)
    slug = models.SlugField('slug')
    photo = models.URLField('foto')
    website = models.URLField('website', blank=True)
    description = models.TextField('descricao', blank=True)

    class Meta:
        verbose_name = 'palestrante'
        verbose_name_plural = 'palestrantes'
    
    def __str__(self):
        return self.name
    
    def get_aboslute_url(self):
        print(r('speaker_detail', slug=self.slug))
        return r('speaker_detail', slug=self.slug)


class Contact(models.Model):
    EMAIL = 'E'
    PHONE = 'P'
    
    KINDS = (
        (EMAIL, 'Email'),
        (PHONE, 'Telefone'),
    )
    speaker = models.ForeignKey('Speaker', on_delete=models.CASCADE, verbose_name='palestrante')
    kind = models.CharField('tipo', max_length=1, choices=KINDS)
    value = models.CharField('valor', max_length=255)

    class Meta:
        verbose_name = 'contato'
        verbose_name_plural = 'contatos'

    def __str__(self):
        return self.value
    
class Talk(models.Model):
    title = models.CharField(max_length=200)
    start = models.TimeField()
    description = models.TextField()
    speakers = models.ManyToManyField('Speaker')


    def __str__(self):
        return str(self.start)