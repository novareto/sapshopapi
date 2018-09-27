# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import logging

from zeep import Client
from requests import Session
from collections import namedtuple
from zeep.transports import Transport
from zope.component import getUtility
from requests.auth import HTTPBasicAuth
from .interfaces import ISAPShopConnection


log = logging.getLogger('sapshopapi')


class MyCache(dict):
    pass


class ArticleMixin(object):

    _v_article = None

    def load(self):
        return

    @property
    def article(self):
        if self._v_article is None:
            matnr = self.getArticleNumber()
            self._v_article = getArticle(matnr)
        return self._v_article

    def getArticleNumber():
        raise NotImplementedError

    def getArticle(self, matnr):
        raise NotImplementedError

    @property
    def matnr(self):
        return self.article.matnr

    @property
    def title(self):
        return self.article.title

    @property
    def description(self):
        return self.article.description

    @property
    def preis(self):
        return self.article.preis

    @property
    def preis_mem(self):
        return self.article.preis_mem

    @property
    def bestand(self):
        return self.article.bestand

    @property
    def freimenge(self):
        return self.article.freimenge


class Article(object):

    def __init__(self,
                 matnr, title="",
                 description="",
                 preis=0.0,
                 preis_mem=0.0,
                 medienart="",
                 bestand = 0.0,
                 freimenge = 0.0):
        self.matnr = matnr
        self.title = title
        self.description = description
        self.preis = preis
        self.preis_mem = preis_mem
        self.medienart = medienart
        self.bestand = bestand
        self.freimenge = freimenge


class SAPAPI(object):
    """ Example Connection """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            log.debug("Setting the following API-URL-Endpoints %s %s" % (k, v))
            setattr(self, k, v)

    def client(self, MET_URL):
        """
        This method retuns an ZEEP Client you have to Provide the SOAP URL 
        """
        session = Session()
        session.auth = HTTPBasicAuth("xxwsn", "novareto")
        client = Client(
            self.BASE_URL + MET_URL,
            transport=Transport(session=session)
        )
        return client

    def getArticle(self, matnr):
        log.info('Fetching Article %s' % matnr)
        client = self.client(self.ITEM_URL)
        article = client.service.Z_ETEM_IMP_ARTIKEL(matnr)
        return Article(
            matnr=matnr,
            title=article.EX_DESCR,
            preis=article.EX_PRICEEXT,
            preis_mem=article.EX_PRICEMEM,
            medienart=article.EX_WARENGRUPPE,
            bestand = article.EX_AMOUNT,
            freimenge = article.EX_AMOUNT_FREE
        )

    def getAllItems(self):
        client = self.client(self.ALL_ITEMS_URL)
        results = client.service.Z_ETEM_IMP_ALL_ITEMS().ET_MATLIST.item
        rc = []
        for x in results:
            rc.append(Article(x.MATNR))
        return rc

    def getUser(self, email, art="R"):
        client = self.client(self.GET_USER_URL)
        user = client.service.Z_ETEM_IMP_GET_USER(IP_USER=email)
        if user.ET_ADRESSLIST:
            return user.ET_ADRESSLIST
            #if art == "R":
            #    return user.ET_ADRESSLIST.item[0]
            #return user.ET_ADRESSLIST.item[1]
        return []

    def deleteUserVerify(self, **kwargs):
        client = self.client(self.DELETE_USER_URLV)
        res = client.service.Z_ETEM_IMP_DELETE_USER_VERIFY(IP_DELCODE=kwargs.get('delcode'), IP_USER=kwargs.get('email'))
        log.info('Entfernter User %s' % kwargs.get('email'))
        return res

    def deleteUser(self, email):
        client = self.client(self.DELETE_USER_URL)
        res = client.service.Z_ETEM_IMP_DELETE_USER_REQUEST(IP_USER=email)
        log.info('Zum Loeschen vorgemerkter Benutzer %s' % email)
        return res

    def addUser(self, **kwargs):
        client = self.client(self.ADD_USER_URL)
        # Types
        factory = client.type_factory('ns0')
        user = factory.ZIMP_S_CREATE_USER(
            ANRED=kwargs.get('anrede', ''), 
            NAME1=kwargs.get('name1', ''), 
            NAME2=kwargs.get('name2', ''), 
            NAME3=kwargs.get('name3', ''), 
            NAME4=kwargs.get('name4', ''), 
            ORT01=kwargs.get('ort', ''), 
            STRAS=kwargs.get('strasse', ''),
            PSTLZ=kwargs.get('plz', ''),
            LAND1=kwargs.get('land', ''),
            TELF1=kwargs.get('telefon', ''),
            MITNR=kwargs.get('mitnr', ''),
            ART=u'R', 
            SMTP_ADDR=kwargs.get('email', '')
        )
        v_factory = client.type_factory('ns0')
        versand = v_factory.ZIMP_S_CREATE_USER(
            ANRED=kwargs.get('anrede_v', ''),
            NAME1=kwargs.get('name1_v', ''),
            NAME2=kwargs.get('name2_v', ''),
            NAME3=kwargs.get('name3_v', ''),
            NAME4=kwargs.get('name4_v', ''),
            ORT01=kwargs.get('ort_v', ''),
            STRAS=kwargs.get('strasse_v', ''),
            PSTLZ=kwargs.get('plz_v', ''),
            LAND1=kwargs.get('land_v', ''),
            TELF1=kwargs.get('telefon', ''),
            MITNR=kwargs.get('mitnr', ''),
            ART=u'V',
            SMTP_ADDR=kwargs.get('email', '')
        )
        ul = factory.ZIMP_T_CREATE_USER(item=[user])
        if kwargs.get('versand'):
            ul = factory.ZIMP_T_CREATE_USER(item=[user, versand]) 
        result = client.service.Z_ETEM_IMP_CREATE_USER(IP_PASSWORD=kwargs.get('passwort'), IT_USER=ul)
        log.info('Added User %s' % kwargs.get('email'))
        return result

    def updateUser(self, **kwargs):
        client = self.client(self.UPDATE_USER_URL)
        factory = client.type_factory('ns0')
        user = factory.ZIMP_S_UPDATE_USER(
            ANRED=kwargs.get('anrede', ''), 
            NAME1=kwargs.get('name1', ''), 
            NAME2=kwargs.get('name2', ''), 
            NAME3=kwargs.get('name3', ''), 
            NAME4=kwargs.get('name4', ''), 
            ORT01=kwargs.get('ort', ''), 
            STRAS=kwargs.get('strasse', ''),
            PSTLZ=kwargs.get('plz', ''),
            LAND1=kwargs.get('land', ''),
            TELF1=kwargs.get('telefon', ''),
            MITNR=kwargs.get('mitnr', ''),
            ART=u'R', 
        )
        v_factory = client.type_factory('ns0')
        versand = v_factory.ZIMP_S_UPDATE_USER(
            ANRED=kwargs.get('anrede_v', ''),
            NAME1=kwargs.get('name1_v', ''),
            NAME2=kwargs.get('name2_v', ''),
            NAME3=kwargs.get('name3_v', ''),
            NAME4=kwargs.get('name4_v', ''),
            ORT01=kwargs.get('ort_v', ''),
            STRAS=kwargs.get('strasse_v', ''),
            PSTLZ=kwargs.get('plz_v', ''),
            LAND1=kwargs.get('land_v', ''),
            TELF1=kwargs.get('telefon', ''),
            MITNR=kwargs.get('mitnr', ''),
            ART=u'V',
        )
        ul = factory.ZIMP_T_UPDATE_USER(item=[user, versand])
        result = client.service.Z_ETEM_IMP_UPDATE_USER(IP_USER=kwargs.get('email'), IT_ADRESS=ul)
        return result

    def resetPassword(self, email):
        client = self.client(self.RESET_PASSWORD_URL)
        result = client.service.Z_ETEM_IMP_RESET_PASSWORD(IP_USER=email)
        return result

    def updatePassword(self, email, old_password, new_password):
        client = self.client(self.UPDATE_PASSWORD_URL)
        result = client.service.Z_ETEM_IMP_UPDATE_PASSWORD(IP_USER=email, IP_PASSWORD=old_password, IP_NEWPASSWORD=new_password)
        return result

    def getPassword(self, email, password):
        client = self.client(self.GET_PASSWORD_URL)
        result = client.service.Z_ETEM_IMP_GET_PASSWORD(IP_USER=email, IP_PASSWORD=password)
        if result.EX_MESSAGE == u'Login g\xfcltig':
            return True
        return False

    def createOrder(self, email, artikel):
        client = self.client(self.CREATE_ORDER_URL)
        factory = client.type_factory('ns0')
        s_artikel = []
        for art in artikel:
            s_artikel.append(
                factory.ZIMP_S_ORDER(
                    MATNR=art.get('matnr'),
                    MENGE=art.get('menge')
                )
            )
        order = factory.ZIMP_T_ORDER(item=s_artikel)
        result = client.service.Z_ETEM_IMP_CREATE_ORDER(IP_USER=email, IT_ORDER=order)
        return result

def getAllItems():
    client = getUtility(ISAPShopConnection)
    return client.getAllItems()


def getArticle(matnr):
    client = getUtility(ISAPShopConnection)
    return client.getArticle(matnr)


def getAPI():
    return getUtility(ISAPShopConnection)
