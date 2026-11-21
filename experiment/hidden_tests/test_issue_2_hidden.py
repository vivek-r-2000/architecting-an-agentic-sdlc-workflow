import pytest
from tinydb import TinyDB, Query
from tinydb.table import Document
from tinydb.storages import MemoryStorage

def test_upsert_condition_takes_precedence_for_existing_match():
    db = TinyDB(storage=MemoryStorage)
    # Alice is doc_id 1
    id1 = db.insert({'name': 'alice', 'role': 'user', 'karma': 10})
    
    # Upsert with a Document instance that has a provisional/dummy doc_id=99,
    # but a query condition targeting alice.
    Q = Query()
    updated_doc = Document({'role': 'admin', 'karma': 20}, doc_id=99)
    affected = db.upsert(updated_doc, Q.name == 'alice')
    
    # Must update doc 1, NOT insert a brand new doc 99
    assert affected == [id1]
    assert len(db.all()) == 1
    record = db.get(doc_id=id1)
    assert record['role'] == 'admin'
    assert record['karma'] == 20

def test_upsert_inserts_new_record_preserving_doc_id_when_no_match():
    db = TinyDB(storage=MemoryStorage)
    Q = Query()
    new_doc = Document({'user': 'bob', 'role': 'admin'}, doc_id=50)
    affected = db.upsert(new_doc, Q.user == 'bob')
    
    assert affected == [50]
    assert db.get(doc_id=50)['user'] == 'bob'

def test_upsert_multiple_matches_updates_all():
    db = TinyDB(storage=MemoryStorage)
    id1 = db.insert({'category': 'books', 'discount': 0})
    id2 = db.insert({'category': 'books', 'discount': 0})
    
    Q = Query()
    affected = db.upsert({'discount': 10}, Q.category == 'books')
    assert set(affected) == {id1, id2}
    assert db.get(doc_id=id1)['discount'] == 10
    assert db.get(doc_id=id2)['discount'] == 10
