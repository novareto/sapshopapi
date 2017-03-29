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
class Connection(sapshopapi.SAPAPI):
    """ Example Connection """


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    connection = Connection()
    component.provideUtility(connection, interfaces.ISAPShopConnection, '')


class TestAPI(object):

    def test_thing(self):
        api = component.getUtility(interfaces.ISAPShopConnection)
        article = api.getArticle('000000000000120171')
        assert isinstance(article, sapshopapi.Article) is True
        assert article.matnr == '000000000000120171'


def test_all_items():
    all_items = sapshopapi.getAllItems()
    assert isinstance(all_items, list) is True
