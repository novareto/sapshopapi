# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

from cached_property import timed_cached_property
from zope.component import getUtility
from .interfaces import ISAPShopConnection


class ArticleItem(object):
    """ Article Item"""

    _client = None

    @property
    def client(self):
        """ Return the Client"""
        return getUtility(ISAPShopConnection)

    @timed_cached_property(ttl=5)
    def price(self):
        """ Return Price Information"""
        return self.client.price()
