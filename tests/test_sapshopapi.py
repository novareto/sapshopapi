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
    connection = Connection(
        BASE_URL="http://SVASAPXQAS.BG10.BGFE.LOCAL:8000/sap/bc/srt/wsdl/flv_10002A111AD1/srvc_url/sap/bc/srt/rfc/sap/",
        ITEM_URL="zws_etem_imp_artikel/050/zws_etem_imp_artikel/zws_etem_imp_artikel?sap-client=050",
        ALL_ITEMS_URL="zws_etem_imp_all_items/050/zws_etem_imp_all_items/zws_etem_imp_all_items?sap-client=050"
    )
    component.provideUtility(connection, interfaces.ISAPShopConnection, '')


class TestAPI(object):

    def test_direct(self):
        api = component.getUtility(interfaces.ISAPShopConnection)
        article = api.getArticle('A001/07P')
        assert isinstance(article, sapshopapi.Article) is True
        assert article.matnr == 'A001/07P'

        article = api.getArticle('AB012')
        assert isinstance(article, sapshopapi.Article) is True
        assert article.matnr == 'AB012'

        article = api.getArticle('AB010')
        assert isinstance(article, sapshopapi.Article) is True
        assert article.matnr == 'AB010'


def test_all_items():
    all_items = sapshopapi.getAllItems()
    assert isinstance(all_items, list) is True
    assert len(all_items) == 310
    all_items = sapshopapi.getAllItems()


class MyArticle(sapshopapi.ArticleMixin):
    matnr = 'AB010'

    def getArticleNumber(self):
        return self.matnr

    def getArticle(self, matnr):
        return sapshopapi.getArticle(matnr)


def test_article():
    myarticle = MyArticle()
    myarticle.load()
    assert isinstance(myarticle._article, sapshopapi.Article)
    assert myarticle.matnr == 'AB010'
    assert myarticle.title == 'Textil'
