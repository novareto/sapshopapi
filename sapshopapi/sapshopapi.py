# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import logging

from zope.component import getUtility
from .interfaces import ISAPShopConnection


log = logging.getLogger('sapshopapi')


class ArticleMixin(object):

    def load(self):
        matnr = self.getArticleNumber()
        self._article = getArticle(matnr)

    def getArticleNumber():
        raise NotImplementedError

    def getArticle(self, matnr):
        raise NotImplementedError

    @property
    def matnr(self):
        return self._article.matnr

    @property
    def title(self):
        return self._article.title

    @property
    def description(self):
        return self._article.description

    @property
    def preis(self):
        return self._article.preis

    @property
    def preis_mem(self):
        return self._article.preis_mem


class Article(object):

    def __init__(self,
                 matnr, title="",
                 description="",
                 preis=0.0,
                 preis_mem=0.0,
                 medienart=""):
        self.matnr = matnr
        self.title = title
        self.description = description
        self.preis = preis
        self.preis_mem = preis_mem
        self.medienart = medienart


class SAPAPI(object):
    """ Example Connection """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            log.info("Setting the following API-URL-Endpoints %s %s" % (k, v))
            setattr(self, k, v)

    def client(self, MET_URL):
        from requests import Session
        from requests.auth import HTTPBasicAuth
        from zeep import Client
        from zeep.transports import Transport
        session = Session()
        session.auth = HTTPBasicAuth("xxwsn", "novareto")
        client = Client(
            self.BASE_URL + MET_URL,
            transport=Transport(session=session)
        )
        return client

    def getArticle(self, matnr):
        client = self.client(self.ITEM_URL)
        article = client.service.Z_ETEM_IMP_ARTIKEL(matnr)
        return Article(
            matnr=matnr,
            title=article.EX_DESCR,
            preis=article.EX_PRICEEXT,
            preis_mem=article.EX_PRICEMEM,
            medienart=article.EX_WARENGRUPPE
        )

    def getAllItems(self):
        client = self.client(self.ALL_ITEMS_URL)
        results = client.service.Z_ETEM_IMP_ALL_ITEMS().ET_MATLIST.item
        rc = []
        for x in results:
            rc.append(Article(x.MATNR))
        return rc


def getAllItems():
    client = getUtility(ISAPShopConnection)
    return client.getAllItems()


def getArticle(matnr):
    client = getUtility(ISAPShopConnection)
    return client.getArticle(matnr)
