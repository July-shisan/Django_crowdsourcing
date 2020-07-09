#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from haystack import indexes
from home.models import Challenge

class ChallengeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Challenge

    def index_queryset(self, using=None):
        return self.get_model().objects.all()