from random import randint, sample

from django.core.management import BaseCommand

from tqdm import tqdm

from ...fakes import DatasetFactory, KeywordFactory, PublicationFactory
from ...models import Dataset, Keyword, Publication


def batch_create(factory, model, batch, count, desc):
    iterations = count // batch
    with tqdm(total=count, desc=desc) as bar:
        for _ in range(iterations):
            rows = factory.build_batch(batch)
            yield model.objects.bulk_create(rows)
            bar.update(batch)

        remain = count % batch
        if remain:
            rows = factory.build_batch(remain)
            yield model.objects.bulk_create(rows)
            bar.update(remain)


class Command(BaseCommand):
    help = 'Seed the database with random data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            default=1024,
            type=int,
            help='The number of rows to create in a batch'
        )
        parser.add_argument(
            '--null-ratio',
            default=0.1,
            type=float,
            help='The proportion of optional columns to set as null.'
        )
        parser.add_argument(
            '--dataset-count',
            default=10000,
            type=int,
            help='The number of datasets to generate'
        )
        parser.add_argument(
            '--publication-count',
            default=1000,
            type=int,
            help='The number of publications to generate'
        )
        parser.add_argument(
            '--keyword-count',
            default=1000,
            type=int,
            help='The number of keywords to generate'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']

        publications = []
        for batch in batch_create(
                PublicationFactory, Publication, batch_size,
                options['publication_count'], 'Generating publications'):
            publications.extend([p.pk for p in batch])

        keywords = []
        for batch in batch_create(
                KeywordFactory, Keyword, batch_size,
                options['keyword_count'], 'Generating keywords'):
            keywords.extend([k.pk for k in batch])

        for batch in batch_create(
                DatasetFactory, Dataset, batch_size,
                options['dataset_count'], 'Generating datasets'):
            publication_links = []
            keyword_links = []
            for dataset in batch:
                for p in sample(publications, k=randint(0, 5)):
                    publication_links.append(Dataset.related_publications.through(
                        dataset_id=dataset.pk, publication_id=p
                    ))

                for k in sample(keywords, k=randint(0, 7)):
                    keyword_links.append(Dataset.keywords.through(
                        dataset_id=dataset.pk, keyword_id=k
                    ))

            Dataset.related_publications.through.objects.bulk_create(publication_links)
            Dataset.keywords.through.objects.bulk_create(keyword_links)
