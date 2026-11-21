# Issue 2: [Bug] Table.upsert() with Document instance raises KeyError or fails to preserve doc_id

## Problem Description
When calling `table.upsert(doc, query)` where `doc` is an existing `Document` instance (which carries `doc.doc_id`), `upsert` crashes with a `KeyError` or improperly re-inserts a duplicate document when the query condition does not match but the `doc.doc_id` already exists in another record, or fails when updating with a Document that has missing table keys.

## Steps to Reproduce
```python
from tinydb import TinyDB, Query
from tinydb.table import Document
from tinydb.storages import MemoryStorage

db = TinyDB(storage=MemoryStorage)
table = db.table('t1')

d1 = Document({'key': 'val1', 'count': 1}, doc_id=10)
table.insert(d1)

# Calling upsert with a Document instance should update existing record if query matches,
# or insert preserving doc_id if provided without crashing on key lookup
Q = Query()
table.upsert(Document({'key': 'val1', 'count': 2}, doc_id=10), Q.key == 'val1')
assert table.get(doc_id=10)['count'] == 2
```

## Expected Behavior
`Table.upsert` should seamlessly accept either a plain `dict` or a `Document` instance. When updating or inserting:
1. It must correctly update all matching documents without raising `KeyError`.
2. When inserting a new document via `upsert`, if a `Document` instance with `doc_id` is supplied, it must respect that `doc_id` or safely assign the next sequence ID without corrupting `table._next_id`.
3. It must return the list of affected `doc_id` integers.
