from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    # الحقول القديمة من اللابات السابقة
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    edition = models.SmallIntegerField(default=1)
    
    # الحقول الجديدة من Lab 9
    quantity = models.IntegerField(default=1)
    pubdate = models.DateTimeField()
    rating = models.SmallIntegerField(default=1)
    
    publisher = models.ForeignKey(
        Publisher,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='books'
    )
    
    authors = models.ManyToManyField(Author, blank=True)
    
    def __str__(self):
        return self.title