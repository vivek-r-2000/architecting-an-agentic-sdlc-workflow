# Issue 1: [Bug] Query.matches() crashes with AttributeError when field is None or integer

## Problem Description
When querying documents using `Query.matches(regex)`, if a document is missing the target field or if the field contains `None` or an integer/boolean instead of a string, `tinydb.queries.Query` raises an unhandled `AttributeError` or `TypeError`:

```python
AttributeError: 'NoneType' object has no attribute 'search'
```

## Steps to Reproduce
```python
from tinydb import TinyDB, Query
import re

db = TinyDB(storage=MemoryStorage)
db.insert({'name': 'alice', 'bio': 'Software engineer at IIIT'})
db.insert({'name': 'bob', 'bio': None})
db.insert({'name': 'charlie', 'bio': 12345})
db.insert({'name': 'dave'}) # bio missing

User = Query()
# The following query crashes instead of evaluating to False for non-string / missing fields:
results = db.search(User.bio.matches(r'engineer', flags=re.IGNORECASE))
```

## Expected Behavior
`User.field.matches(pattern)` should gracefully evaluate to `False` whenever:
1. The target field is absent from the document.
2. The target field's value is `None`.
3. The target field's value is a non-string type (such as `int`, `float`, `list`, or `dict`).

It should never raise an unhandled `AttributeError` or crash the search routine.
