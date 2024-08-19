import pytest
import tempfile
from pathlib import Path 

from fastlite import database
from timekeeper import migrations as m

@pytest.fixture
def migration():
    return m.Migration(
        version=1,
        up="create table if not exists test(id integer primary key autoincrement, version int)",
        down="drop table test"
    )

@pytest.fixture
def db_path():
    tmp_db_path = tempfile.mktemp()
    yield tmp_db_path
    Path(tmp_db_path).unlink()


@pytest.fixture
def db(db_path):
    setup = m.Migrations(db_path)
    return setup.m_db
    
def test_upgrade(migration, db):
    v = migration.upgrade(db)
    assert v == 1

def test_downgrade(migration, db):
    v = migration.upgrade(db)
    assert v == 1
    v = migration.downgrade(db)
    assert v == 0

def test_ensure_latest(db_path):
    migrations = [
        m.Migration(
            version=1,
            up="create table if not exists test(id integer primary key autoincrement, version int)",
            down="drop table test"
        ),
        m.Migration(
            version=2,
            up="alter table test add column name varchar",
            down='alter table test drop column name'
        )
    ]
    setup = m.Migrations(db_path)
    db = database(db_path)
    with pytest.raises(Exception):
        db.execute("insert into test(version, name) values (1, 'test')")
    
    setup.ensure_version(migrations)
    db.execute("insert into test(version, name) values (1, 'test')")
    result = db.execute_returning_dicts("select * from test")
    assert len(result) == 1
    assert result[0]['name'] == 'test'
    db.close()
    
    setup.ensure_version(migrations, version=1)
    db = database(db_path)
    with pytest.raises(Exception):
        db.execute("insert into test(version, name) values (1, 'test')")
    



