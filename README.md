# bug-free-funicular

[![Build Status](https://travis-ci.org/andela-lkabui/bug-free-funicular.svg?branch=develop)](https://travis-ci.org/andela-lkabui/bug-free-funicular)
[![Coverage Status](https://coveralls.io/repos/github/andela-lkabui/bug-free-funicular/badge.svg?branch=develop)](https://coveralls.io/github/andela-lkabui/bug-free-funicular?branch=develop)

## API Routes

### User Resource

URL | Method | Description | Parameters | Public
--- | ------ | ----------- | ---------- | ------
`/auth/new/`| POST | Creates a new User | `username` and `password` | **Yes**
`/auth/login/`| POST | Logs in an existing User | `username` and `password` | **Yes**
`/auth/logout/`| GET | Logs out a logged in User | `N/A` | **No**

### Account Resource

URL | Method | Description | Parameters | Public
--- | ------ | ----------- | ---------- | ------
`/accounts/`| POST | Creates a new Account | `account_name`, `account_number`, `account_owner` and `account_provider`| **No**
`/accounts/`| GET | Retrieves all accounts belonging to currently logged in user | `N/A`| **No**
`/accounts/:account_id`| GET | Retrieves Account of id: `account_id` belonging to currently logged in user | `account_id` | **No**
`/accounts/:account_id`| PUT | Edits details of Account of id: `account_id` belonging to currently logged in user | `account_id` | **No**
`/accounts/:account_id`| DELETE | Deletes Account of id: `account_id` belonging to currently logged in user | `account_id` | **No**

### Service Resource

* Services are a **WIP**. Not entirely clear on who should own these. Will be fixed in due time!

URL | Method | Description | Parameters | Public
--- | ------ | ----------- | ---------- | ------
`/services/`| POST | Creates a new Service | `service_name`, `price`, `service_provider` and `service_description (optional)`| **No**
`/services/`| GET | Retrieves all Services | `N/A`| **No**
`/services/:service_id`| GET | Retrieves Service of id: `service_id` | `service_id` | **No**
`/services/:service_id`| PUT | Edits details of Service of id: `service_id` | `service_id` | **No**
`/services/:service_id`| DELETE | Deletes Service of id: `service_id` | `account_id` | **No**

### Goods Resource

* Goods are a **WIP**. Not entirely clear on who should own these. Will be fixed in due time!

URL | Method | Description | Parameters | Public
--- | ------ | ----------- | ---------- | ------
`/goods/`| POST | Creates a new Good | `good_name`, `price` and `good_provider` | **No**
`/goods/`| GET | Retrieves all Goods | `N/A`| **No**
`/goods/:goods_id`| GET | Retrieves Good of id: `goods_id` | `goods_id` | **No**
`/goods/:goods_id`| PUT | Edits details of Good of id: `goods_id` | `goods_id` | **No**
`/goods/:goods_id`| DELETE | Deletes Good of id: `goods_id` | `goods_id` | **No**

### Provider Resource

URL | Method | Description | Parameters | Public
--- | ------ | ----------- | ---------- | ------
`/provider/`| POST | Creates a new Provider | `provider_name`, `po_box` and `location` | **No**
`/provider/`| GET | Retrieves all Providers | `N/A`| **No**
`/provider/:provider_id`| GET | Retrieves Provider of id: `provider_id` | `provider_id` | **No**
`/provider/:provider_id`| PUT | Edits details of Provider of id: `provider_id` | `provider_id` | **No**
`/provider/:provider_id`| DELETE | Deletes Provider of id: `provider_id` | `provider_id` | **No**