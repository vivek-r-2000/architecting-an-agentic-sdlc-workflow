import pytest
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

def test_query_between_inclusive_bounds():
    db = TinyDB(storage=MemoryStorage)
    db.insert({'val': 5})
    db.insert({'val': 10})
    db.insert({'val': 15})
    db.insert({'val': 20})
    
    Q = Query()
    res = db.search(Q.val.between(10, 15))
    assert {r['val'] for r in res} == {10, 15}

def test_query_between_incomparable_types_and_missing_field():
    db = TinyDB(storage=MemoryStorage)
    db.insert({'val': 12})
    db.insert({'val': 'not-a-number'})
    db.insert({'val': None})
    db.insert({'other': 12}) # val is missing
    
    Q = Query()
    # Must evaluate to False without raising TypeError
    res = db.search(Q.val.between(10, 20))
    assert len(res) == 1
    assert res[0]['val'] == 12

def test_query_between_inverted_bounds_and_caching():
    db = TinyDB(storage=MemoryStorage)
    db.insert({'val': 10})
    
    Q = Query()
    # Inverted bounds (low > high) must evaluate to False
    res = db.search(Q.val.between(20, 10))
    assert len(res) == 0
    
    # Query instance must be hashable and cacheable
    q_inst = Q.val.between(10, 20)
    assert hash(q_inst) is not None
