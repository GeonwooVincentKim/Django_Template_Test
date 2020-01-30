import datetime

from django.db import models


# Create your models here.
from django.utils import timezone


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    # Output Data Lists that
    # Human being can recognize as Words
    # not Models type.
    def __str__(self):
        return self.name

    # Can designate various model-specific options
    # For Example, Publisher object should sort
    # as name Field.
    class Meta:
        ordering = ['-name']


# blank = True, null = True, verbose_name
# --> Changes for Actual Physical Model
class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    # Make Email field as option not required.
    # blank = True --> Make some field as Option not required.
    # blank = False --> Make some field as Required.
    # verbose_name --> Label that Define by user.
    #              --> Do not use Capital Letter when use title case.
    #              --> Because Django shows Capital when it needs.
    # email = models.EmailField(blank=True, verbose_name='e-mail')

    def __str__(self):
        return self.name


# class MaleManager(models.Manager):
#     def get_queryset(self):
#         return super(MaleManager, self).get_queryset(
#         ).filter(sex='M')
#
#
# class FemaleManager(models.Manager):
#     def get_queryset(self):
#         return super(FemaleManager, self).get_queryset(
#         ).filter(sex='F')
#
#
# class Person(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     # sex = models.CharField(max_length=1,
#     #                        choices=(
#     #                            ('M', 'Male'),
#     #                            ('F', 'Female'),
#     #                        ))
#     birth_date = models.DateField()
#
#     def baby_boomer_status(self):
#         # Return Specific Baby-Boom condition.
#         import datetime
#         if self.birth_date < datetime.date(1945, 8, 1):
#             return "Pre-boomer"
#         elif self.birth_date < datetime.date(1965, 1, 1):
#             return "Baby-boomer"
#         else:
#             return "Post-boomer"
#
#     def _get_full_name(self):
#         # Return full name of specific person
#         return "%s %s" % (self.first_name, self.last_name)
#     full_name = property(_get_full_name)
#
#     # people = models.Manager()
#     # men = MaleManager()
#     # women = FemaleManager()
#
#
# class Blog(models.Model):
#     name = models.CharField(max_length=100)
#     tagline = models.TextField()
#
#     def save(self, *args, **kwargs):
#         if self.name == "Yoko Ono's blog":
#             return  # Yoko will not have own Blog
#
#         else:
#             super(Blog, self).save(*args, **kwargs)
#             # Call "Real" Save() Method
#
#
# # Define Lower Class Manager first.
# class DahlBookManager(models.Manager):
#     def get_queryset(self):
#         return super(DahlBookManager, self).get_queryset().\
#             filter(author='Roald Dahl')
#
#
# class BookManager(models.Manager):
#     def title_count(self, keyword):
#         return self.filter(title__icontains=keyword).count()


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey(Publisher)
    # Make Date and Number Fields as option not required
    publication_date = models.DateField()
    # publication_date = models.DateField(blank=True, null=True)
    # num_pages = models.IntegerField(blank=True, null=True)
    # objects = models.Manager()
    # dahl_objects = DahlBookManager()  # Dahl Particular Manager.

    # def __str__(self):
    #     return self.title

    def recent_publication(self):
        return self.publication_date >= timezone.now().date()


datetime.timedelta(weeks=8)
