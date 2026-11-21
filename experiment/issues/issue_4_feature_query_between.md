# Issue 4: [Feature] Add Query.between(low, high) boundary predicate method

## Feature Description
Add a new query method `Query.between(low, high)` to `tinydb.queries.Query`.

## Requirements
1. `Query.between(low, high)` must return a `QueryInstance` checking whether a document's field value satisfies inclusive bounds: `low <= value <= high`.
2. Defensive Type Handling: If the document's field is absent, `None`, or contains an incomparable type (e.g., comparing an integer bound against a string document value), the query must evaluate to `False` gracefully without raising `TypeError` or unhandled exceptions.
3. Logical Composition: The returned `QueryInstance` must seamlessly support logical bitwise operators (`&`, `|`, `~`).
4. Query Caching & Hashing: Must generate a deterministic, frozen hash tuple so that `Table._query_cache` can cache the query result safely.
5. Inverted bounds: If `low > high`, the query evaluates to `False` for all values.
