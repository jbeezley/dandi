from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

MAX_CHAR_LENGTH = 255


class Publication(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    doi = models.CharField(max_length=MAX_CHAR_LENGTH, unique=True)

    def __str__(self):
        return self.doi


class Keyword(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    keyword = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.keyword


class Dataset(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    related_publications = models.ManyToManyField(Publication, related_name='datasets')
    keywords = models.ManyToManyField(Keyword, related_name='datasets')

    # replace with a FileField
    path = models.CharField(max_length=MAX_CHAR_LENGTH)
    size = models.BigIntegerField()

    genotype = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    subject_id = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    age = models.DurationField(null=True)
    date_of_birth = models.DateTimeField(null=True)
    number_of_electrodes = models.IntegerField(null=True)
    lab = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    session_start_time = models.DateField(null=True)
    experimenter = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    session_id = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    species = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    identifier = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    session_description = models.CharField(max_length=1023, null=True)
    experiment_description = models.CharField(max_length=1023, null=True)
    institution = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    number_of_units = models.IntegerField(null=True)
    nwb_version = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)

    search_vector = SearchVectorField(null=True, editable=False)

    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]


class DataTag(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=MAX_CHAR_LENGTH, unique=True)
    datasets = models.ManyToManyField(Dataset, related_name='tags')

    def __str__(self):
        return self.name
