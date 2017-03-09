#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_sapshopapi
----------------------------------

Tests for `sapshopapi` module.
"""

from sapshopapi import sapshopapi
from sapshopapi import interfaces
from zope import component, interface


@interface.implementer(interfaces.ISAPShopConnection)
class Connection(object):
    """ Example Connection """

    def price(self):
        """i  """
        return 1.0


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    connection = Connection()
    component.provideUtility(connection, interfaces.ISAPShopConnection, '')


class TestSAPShop(object):

    def test_article(self):
        """Sample pytest test function with the pytest fixture as an argument.
        """
        article = sapshopapi.ArticleItem()
        assert article.price == 1.0
