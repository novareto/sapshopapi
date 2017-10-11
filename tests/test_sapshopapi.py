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
        BASE_URL="http://SVASAPXQAS.BG10.BGFE.LOCAL:8000/sap/bc/srt/wsdl/flv_10002A111AD1/bndg_url/sap/bc/srt/rfc/sap/",
        SEARCH_URL="zws_etemweb_suche/050/zws_etemweb_suche/zws_etemweb_suche?sap-client=050",
        ITEM_URL="zws_etemweb_artikel/050/zws_etemweb_artikel/zws_etemweb_artikel?sap-client=050",
        ALL_ITEMS_URL="zws_etemweb_all_items/050/zws_etemweb_all_items/zws_etemweb_all_items?sap-client=050"
    )
    component.provideUtility(connection, interfaces.ISAPShopConnection, '')


class TestAPI(object):

    def test_direct(self):
        api = component.getUtility(interfaces.ISAPShopConnection)
        article = api.getArticle('000000000000120171')
        assert isinstance(article, sapshopapi.Article) is True
        assert article.matnr == '000000000000120171'

        article = api.getArticle('003 DP')
        assert isinstance(article, sapshopapi.Article) is True
        assert article.matnr == '003 DP'

        article = api.getArticle('CD006')
        assert isinstance(article, sapshopapi.Article) is True
        assert article.matnr == 'CD006'


def test_all_items():
    all_items = sapshopapi.getAllItems()
    assert isinstance(all_items, list) is True
    assert len(all_items) == 1742
    all_items = sapshopapi.getAllItems()


class MyArticle(sapshopapi.ArticleMixin):
    matnr = '000000000000120171'

    def getArticleNumber(self):
        return self.matnr

    def getArticle(self, matnr):
        return sapshopapi.getArticle(matnr)


def test_article():
    myarticle = MyArticle()
    assert isinstance(myarticle._article, sapshopapi.Article)
    assert myarticle.title == '000000000000120171'
    assert myarticle.description == 'Vereinbarkeit Beruf und Familie'
