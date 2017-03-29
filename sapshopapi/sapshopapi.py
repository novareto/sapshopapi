# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

from cached_property import timed_cached_property
from zope.component import getUtility
from .interfaces import ISAPShopConnection
from collections import namedtuple

AI = namedtuple('AllItems', ('matnr'))


BASE_URL = "http://SVASAPXQAS.BG10.BGFE.LOCAL:8000/sap/bc/srt/wsdl/flv_10002A111AD1/bndg_url/sap/bc/srt/rfc/sap/"
SEARCH_URL = "zws_etemweb_suche/050/zws_etemweb_suche/zws_etemweb_suche?sap-client=050"
ITEM_URL = "zws_etemweb_artikel/050/zws_etemweb_artikel/zws_etemweb_artikel?sap-client=050"
ALL_ITEMS_URL = "zws_etemweb_all_items/050/zws_etemweb_all_items/zws_etemweb_all_items?sap-client=050"


class Article(object):

    def __init__(self, matnr, title, description, preis, preis_mem):
        self.matnr = matnr
        self.title = title
        self.description = description
        self.preis = preis
        self.preis_mem = preis_mem


class SAPAPI(object):
    """ Example Connection """

    def client(self, MET_URL):
        from suds.client import Client
        client = Client(
            BASE_URL + MET_URL,
            username="xxwsn",
            password="novareto"
        )
        return client

    def getArticle(self, matnr):
        client = self.client(ITEM_URL)
        article = client.service.Z_ETEM_WS_ARTIKEL(matnr)
        return Article(
            matnr=matnr,
            title=article.EX_TITLE,
            description=article.EX_DESCR,
            preis=article.EX_PRICEEXT,
            preis_mem=article.EX_PRICEMEM
        )

    def getAllItems(self):
        client = self.client(ALL_ITEMS_URL)
        results = [y for x, y in client.service.Z_ETEM_WS_ALL_ITEMS()['ET_MATLIST']][0]
        rc = []
        for x in results:
            rc.append(AI(x.MATNR))
        return rc



def getAllItems():
    client = getUtility(ISAPShopConnection)
    return client.getAllItems()
