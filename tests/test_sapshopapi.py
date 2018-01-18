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
        ALL_ITEMS_URL="zws_etem_imp_all_items/050/zws_etem_imp_all_items/zws_etem_imp_all_items?sap-client=050",
        ADD_USER_URL="zws_etem_imp_create_user/050/zws_etem_imp_create_user/zws_etem_imp_create_user?sap-client=050",
        UPDATE_USER_URL="zws_etem_imp_update_user/050/zws_etem_imp_update_user/zws_etem_imp_update_user?sap-client=050",
        GET_USER_URL="zws_etem_imp_get_user/050/zws_etem_imp_get_user/zws_etem_imp_get_user?sap-client=050",
        DELETE_USER_URL="zws_etem_imp_delete_user_req/050/zws_etem_imp_delete_user_req/zws_etem_imp_delete_user_req?sap-client=050",
        DELETE_USER_URLV="zws_etem_imp_delete_user_ver/050/zws_etem_imp_delete_user_ver/zws_etem_imp_delete_user_ver?sap-client=050",
        UPDATE_PASSWORD_URL="zws_etem_imp_update_password/050/zws_etem_imp_update_password/zws_etem_imp_update_password?sap-client=050",
        RESET_PASSWORD_URL="zws_etem_imp_reset_password/050/zws_etem_imp_reset_password/zws_etem_imp_reset_password?sap-client=050",
        GET_PASSWORD_URL="zws_etem_imp_get_password/050/zws_etem_imp_get_password/zws_etem_imp_get_password?sap-client=050",
        CREATE_ORDER_URL="zws_etem_imp_create_order/050/zws_etem_imp_create_order/zws_etem_imp_create_order?sap-client=050"
    )
    component.provideUtility(connection, interfaces.ISAPShopConnection, '')



def addUser():
    api = component.getUtility(interfaces.ISAPShopConnection)
    result = api.addUser(
        anrede="Herr",
        name1="Klinger",
        name2="Christian",
        name3="Novareto",
        name4="GmbH",
        plz="90619",
        ort="Fuerth",
        strasse="Karonlinenstr. 17",
        land="DE",
        email="ck@novareto.de",
        art="R",
        mitnr="12345678",
        passwort="K1e2test"
    )


def deleteAll(email):
    api = component.getUtility(interfaces.ISAPShopConnection)
    URL = "http://SVASAPXQAS.BG10.BGFE.LOCAL:8000/sap/bc/srt/wsdl/flv_10002A111AD1/srvc_url/sap/bc/srt/rfc/sap/zws_etem_imp_masterdelete/050/zws_etem_imp_masterdelete/zws_etem_imp_masterdelete?sap-client=050"
    client = api.client(URL)
    result = client.service.Z_ETEM_IMP_MASTERDELETE(IP_USER=email)
    return result


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


class TestUser(object):

    def test_add(self):
        api = component.getUtility(interfaces.ISAPShopConnection)
        result = api.addUser(
            anrede="Herr",
            name1="Klinger",
            name2="Christian",
            name3="Novareto",
            name4="GmbH",
            plz="90619",
            ort="Fuerth",
            strasse="Karonlinenstr. 17",
            land="DE",
            email="ck@novareto.de",
            art="R",
            mitnr="12345678",
            passwort="K1e2test"
        )
        user = api.getUser(email="ck@novareto.de")
        assert user.ANRED == "Herr"
        assert user.NAME1 == "Klinger"
        assert user.NAME3 == "Novareto"
        #delm = api.deleteUser(email="ck@novareto.de")

    def test_reset_password(self):
        api = component.getUtility(interfaces.ISAPShopConnection)
        result = api.resetPassword('ck@novareto.de')
        assert result.EX_MESSAGE == 'Reset erfolgreich'

    def test_update_password(self):
        api = component.getUtility(interfaces.ISAPShopConnection)
        result = api.updatePassword('ck@novareto.de', 'K1e2test', 'B1e2test')
        assert result.EX_MESSAGE == 'Update erfolgreich'
        result = api.updatePassword('ck@novareto.de', 'B1e2test', 'K1e2test')

    def test_get_password(self):
        api = component.getUtility(interfaces.ISAPShopConnection)
        result = api.getPassword('ck@novareto.de', 'K1e2test')
        assert result is True
        result = api.getPassword('ck@novareto.de', 'WrongPW')
        assert result is False

    def test_update_user(self):
        api = component.getUtility(interfaces.ISAPShopConnection)
        result = api.updateUser(
            anrede="Herr",
            name1="Klinger1",
            name2="Christian1",
            name3="Novareto1",
            name4="GmbH",
            plz="90619",
            ort="Fuerth",
            strasse="Karonlinenstr. 17",
            land="DE",
            email="ck@novareto.de",
            art="R",
            mitnr="12345678",
            passwort="K1e2test"
        )
        assert result.EX_MESSAGE == 'Update erfolgreich'
        user = api.getUser(email="ck@novareto.de")
        assert user.ANRED == "Herr"
        assert user.NAME1 == "Klinger1"
        assert user.NAME3 == "Novareto1"
        result = api.updateUser(
            anrede="Herr",
            name1="Klinger",
            name2="Christian",
            name3="Novareto",
            name4="GmbH",
            plz="90619",
            ort="Fuerth",
            strasse="Karonlinenstr. 17",
            land="DE",
            email="ck@novareto.de",
            art="R",
            mitnr="12345678",
            passwort="K1e2test"
        )

    @classmethod 
    def teardown_class(cls):
        deleteAll('ck@novareto.de')


class TestOrder():

    @classmethod 
    def setup_class(cls):
        addUser()

    @classmethod 
    def teardown_class(cls):
        deleteAll('ck@novareto.de')

    def test_order(self):
        api = component.getUtility(interfaces.ISAPShopConnection)
        result = api.createOrder(email="ck@novareto.de", password="K1e2test", artikel=[{'matnr':'AB010', 'menge':"1"}])
        assert result.EX_VBELN is not None