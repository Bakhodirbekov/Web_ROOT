# models.py
from autoslug import AutoSlugField
from django.db import models
from django.utils.text import slugify




class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='static/main/img/cotigory-foto')

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)



class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='')
    text = models.TextField(max_length=255)  # Set the maximum length for the text field
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)




class Work(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/main/img/work-foto')
    title = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    vaqti = models.DateTimeField()
    text = models.TextField(max_length=255)
    desc = models.TextField(max_length=255)
    status = models.BooleanField(default=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    # Add an AutoSlugField for automatic slug creation
    slug = AutoSlugField(unique=True, populate_from='title')


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Work, self).save(*args, **kwargs)

class JobApplication(models.Model):
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    resume = models.FileField(upload_to='static/main/resum ')
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, blank=True, null=True )

class User(models.Model):
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class admin_log(models.Model):
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)