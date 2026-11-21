import pytest
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

def test_query_any_matches_if_any_element_satisfies():
    db = TinyDB(storage=MemoryStorage)
    db.insert({'id': 1, 'tags': ['python', 'ml']})
    db.insert({'id': 2, 'tags': ['rust', 'systems']})
    db.insert({'id': 3, 'tags': []})
    db.insert({'id': 4, 'tags': None})
    
    Q = Query()
    # Tag matches if any tag is in ['python', 'c++']
    results = db.search(Q.tags.any(['python', 'c++']))
    assert [r['id'] for r in results] == [1]

def test_query_all_matches_if_all_elements_satisfy():
    db = TinyDB(storage=MemoryStorage)
    db.insert({'id': 1, 'scores': [90, 95, 88]})
    db.insert({'id': 2, 'scores': [90, 45, 88]})
    db.insert({'id': 3, 'scores': []}) # empty list does not satisfy all
    
    Q = Query()
    results = db.search(Q.scores.all(lambda s: s >= 80))
    assert [r['id'] for r in results] == [1]

def test_query_any_and_all_composition():
    db = TinyDB(storage=MemoryStorage)
    db.insert({'id': 1, 'tags': ['a', 'b'], 'active': True})
    db.insert({'id': 2, 'tags': ['a', 'c'], 'active': False})
    
    Q = Query()
    results = db.search((Q.tags.any(['a'])) & (Q.active == True))
    assert [r['id'] for r in results] == [1]
