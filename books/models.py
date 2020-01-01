from django.db import models


# Create your models here.
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
        ordering = ['name']


# blank = True, null = True, verbose_name
# --> Changes for Actual Physical Model
class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    # Make Email field as option not required.
    # blank = True --> Make some field as Option not required.
    # blank = False --> Make some field as Required.
    # verbose_name --> Label that Define by user.
    #              --> Do not use Capital Letter when use title case.
    #              --> Because Django shows Capital when it needs.
    email = models.EmailField(blank=True, verbose_name='e-mail')

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    # Make Date and Number Fields as option not required
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
