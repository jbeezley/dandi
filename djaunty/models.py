from django.db import models

MAX_CHAR_LENGTH = 255


class Publication(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    doi = models.CharField(max_length=MAX_CHAR_LENGTH, unique=True)

    def __str__(self):
        return self.doi


class Dataset(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    related_publications = models.ManyToManyField(Publication)

    # replace with a FileField
    path = models.CharField(max_length=MAX_CHAR_LENGTH)
    size = models.BigIntegerField()

    genotype = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    subject_id = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    age_in_days = models.FloatField(null=True)
    number_of_electrodes = models.IntegerField(null=True)
    lab = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    session_start_time = models.DateField(null=True)
    experimenter = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    session_id = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    species = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    identifier = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    session_description = models.CharField(max_length=1023, null=True)
    institution = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
    number_of_units = models.IntegerField(null=True)
    nwb_version = models.CharField(max_length=MAX_CHAR_LENGTH, null=True)
