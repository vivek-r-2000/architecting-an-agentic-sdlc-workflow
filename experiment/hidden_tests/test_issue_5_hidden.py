import pytest
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

def test_indexed_field_lookup_accelerates_query():
    db = TinyDB(storage=MemoryStorage)
    table = db.table('users')
    
    # Insert documents
    for i in range(50):
        table.insert({'username': f'user_{i}', 'email': f'user_{i}@example.com'})
        
    # Requirements specify adding create_index(field) to Table for O(1) attribute lookup
    table.create_index('username')
    
    Q = Query()
    res = table.search(Q.username == 'user_25')
    assert len(res) == 1
    assert res[0]['username'] == 'user_25'

def test_indexed_field_invalidates_on_document_mutation():
    db = TinyDB(storage=MemoryStorage)
    table = db.table('users')
    doc_id = table.insert({'username': 'alice', 'status': 'active'})
    
    table.create_index('username')
    Q = Query()
    assert len(table.search(Q.username == 'alice')) == 1
    
    # Mutation should update the index
    table.update({'username': 'alice_renamed'}, doc_ids=[doc_id])
    assert len(table.search(Q.username == 'alice')) == 0
    assert len(table.search(Q.username == 'alice_renamed')) == 1

def test_indexed_field_cleans_up_on_document_removal():
    db = TinyDB(storage=MemoryStorage)
    table = db.table('users')
    doc_id = table.insert({'username': 'bob', 'status': 'inactive'})
    
    table.create_index('username')
    Q = Query()
    table.remove(doc_ids=[doc_id])
    
    assert len(table.search(Q.username == 'bob')) == 0
