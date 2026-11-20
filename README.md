# sapshopapi

`sapshopapi` is a Python client for the SAP Shop SOAP services. It handles article lookup, customer accounts, passwords, and order submission.

## Setup

Run `pip install .` from the package root. Pass `BASE_URL` and the WSDL path for each operation you use. The client concatenates the base URL and path, so include the separator where needed.

```python
from sapshopapi.sapshopapi import SAPAPI

api = SAPAPI(
    BASE_URL="https://sap.example.com/",
    ITEM_URL="path/to/article-wsdl",
)
article = api.getArticle("12345")
print(article.title, article.preis, article.bestand)
```

## Operations

| Task | Methods | Endpoint settings |
| --- | --- | --- |
| Fetch an article or list material numbers | `getArticle(matnr)`, `getAllItems()` | `ITEM_URL`, `ALL_ITEMS_URL` |
| Look up, add, or update a customer | `getUser(email)`, `addUser(**kwargs)`, `updateUser(**kwargs)` | `GET_USER_URL`, `ADD_USER_URL`, `UPDATE_USER_URL` |
| Request and confirm account deletion | `deleteUser(email)`, `deleteUserVerify(email=..., delcode=...)` | `DELETE_USER_URL`, `DELETE_USER_URLV` |
| Validate, reset, or change a password | `getPassword(email, password)`, `resetPassword(email)`, `updatePassword(email, old_password, new_password)` | `GET_PASSWORD_URL`, `RESET_PASSWORD_URL`, `UPDATE_PASSWORD_URL` |
| Submit an order | `createOrder(email, artikel)` with a list of dictionaries containing `matnr` and `menge` | `CREATE_ORDER_URL` |

`getAllItems()` returns `Article` objects populated with material numbers only. Use `getArticle(matnr)` for titles, prices, and stock.

For Zope integration, register the configured client as the unnamed `ISAPShopConnection` utility. The module-level `getAPI()`, `getArticle()`, and `getAllItems()` helpers resolve that utility.
