import re
import pytest
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

def test_matches_missing_field_evaluates_false():
    db = TinyDB(storage=MemoryStorage)
    db.insert({'name': 'alice', 'bio': 'expert software engineer'})
    db.insert({'name': 'bob'}) # bio missing
    
    Q = Query()
    results = db.search(Q.bio.matches(r'engineer'))
    assert len(results) == 1
    assert results[0]['name'] == 'alice'

def test_matches_none_value_evaluates_false():
    db = TinyDB(storage=MemoryStorage)
    db.insert({'name': 'alice', 'bio': 'expert software engineer'})
    db.insert({'name': 'charlie', 'bio': None})
    
    Q = Query()
    results = db.search(Q.bio.matches(r'engineer'))
    assert len(results) == 1
    assert results[0]['name'] == 'alice'

def test_matches_incomparable_type_evaluates_false():
    db = TinyDB(storage=MemoryStorage)
    db.insert({'name': 'alice', 'code': 'ABC-123'})
    db.insert({'name': 'david', 'code': 12345})
    db.insert({'name': 'elena', 'code': ['ABC', 'DEF']})
    
    Q = Query()
    results = db.search(Q.code.matches(r'^ABC'))
    assert len(results) == 1
    assert results[0]['name'] == 'alice'
