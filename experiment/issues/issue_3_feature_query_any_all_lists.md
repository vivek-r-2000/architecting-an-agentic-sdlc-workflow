# Issue 3: [Feature] Add Query.any() and Query.all() for nested array/list fields

## Feature Description
Currently, TinyDB queries on list fields only support basic equality or custom lambdas. Users frequently store documents with array fields (e.g., `tags: ['python', 'ai', 'cloud']` or `scores: [85, 92, 78]`). We need first-class query methods `Query.any(cond)` and `Query.all(cond)` on `tinydb.queries.Query` to test conditions against list items.

## Motivation & Use Cases
```python
User = Query()
# Match if ANY item in tags equals 'python':
db.search(User.tags.any(['python', 'cython'])) # or cond callable

# Match if ALL items in permissions are in allowed set:
db.search(User.roles.all(['admin', 'editor']))
```

## Specification
1. `Query.any(cond)`:
   - Evaluates to `True` if the document's field is a list/sequence and at least one element satisfies `cond`.
   - If `cond` is a sequence/list, evaluates whether any element of the document field is contained in `cond`.
   - If `cond` is a callable/QueryInstance, evaluates whether `cond(item)` returns True for any element.
   - If the document field is missing, None, or not iterable, evaluates to `False` without raising an exception.
2. `Query.all(cond)`:
   - Evaluates to `True` if the document's field is a non-empty sequence/list and all elements satisfy `cond`.
   - If the field is missing, None, or empty, evaluates to `False`.
3. Must support standard query composition (`&`, `|`, `~`) and produce deterministic hash values for query caching.
