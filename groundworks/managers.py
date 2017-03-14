# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class TimeStampedQuerySet(models.QuerySet):
    """
    A ``QuerySet`` for ``TimeStamped`` models.
    """

    def newest(self):
        return self.order_by('-date_created')


class TimeStampedManager(models.Manager):
    """
    A ``Manager`` for ``TimeStamped`` models.
    """

    def get_queryset(self):
        return TimeStampedQuerySet(self.model, using=self._db)

    def newest(self):
        return self.get_queryset().newest()


class PublishableQuerySet(models.QuerySet):
    """
    A ``QuerySet`` for ``Publishable`` models.
    """

    def published(self):
        return self.filter(
            is_published=True, date_published__lte=timezone.now()
        )

    def draft(self):
        return self.filter(
            models.Q(is_published=False) |
            models.Q(date_published__gt=timezone.now())
        )


class PublishableManager(models.Manager):
    """
    A ``Manager`` for ``Publishable`` models.
    """

    def get_queryset(self):
        return PublishableQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def draft(self):
        return self.get_queryset().draft()


class UndeletableQuerySet(models.QuerySet):
    """
    A ``QuerySet`` for ``Undeletable`` models.
    """

    def deleted(self):
        return self.exclude(date_deleted__isnull=True)

    def not_deleted(self):
        return self.filter(date_deleted__isnull=True)


class UndeletableManager(models.Manager):
    """
    A ``Manager`` for ``Undeletable`` models.
    """

    # NOTE: Do not filter out the deleted objects in get_queryset. This
    #       manager is set as the base_manager for reverse relations as well,
    #       so filtering should not take place here. See the docs on Managers
    #       and base_managers.
    def get_queryset(self):
        return UndeletableQuerySet(self.model, using=self._db)

    def deleted(self):
        return self.get_queryset().deleted()

    def not_deleted(self):
        return self.get_queryset().not_deleted()