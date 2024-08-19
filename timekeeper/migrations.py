from fastlite import database, Database
from dataclasses import dataclass

LATEST_VERSION = """
SELECT COALESCE(MAX(VERSION),0) AS VERSION
FROM MIGRATIONS
"""

DELETE_MIGRATION = """
DELETE FROM MIGRATIONS
WHERE VERSION = ?
RETURNING *
"""

class Migrations:

    def __init__(self, db_path: str):
        self.m_db = database(db_path)
        self.migrations = self.m_db.t.migrations
        if self.migrations not in self.m_db.tables:
            self.migrations.create(id=int, version=int, pk='id')
        result = self.m_db.execute_returning_dicts(LATEST_VERSION)[0]
        print(result)
        self.current_version = result['VERSION']
    
    def ensure_version(self, migrations: list["Migration"], version=None):
        versions = {item.version: item for item in migrations}
        version = max(versions.keys()) if version is None else version
        result = self.m_db.execute_returning_dicts(LATEST_VERSION)
        current_version = result[0]['VERSION']
        while current_version < version:
            current_version = versions[current_version + 1].upgrade(self.m_db)

        while current_version > version:
            current_version = versions[current_version].downgrade(self.m_db)
        


@dataclass
class Migration:
    version: int
    up: str
    down: str

    def upgrade(self, db: Database) -> int:
        db.execute(self.up)
        migrations = db.t.migrations
        result = migrations.insert(version=self.version)
        return result['version']
    
    def downgrade(self, db: Database) -> int:
        print(self.down)
        db.execute(self.down)
        db.execute_returning_dicts(DELETE_MIGRATION, (self.version,))
        result = db.execute_returning_dicts(LATEST_VERSION)[0]
        return result['VERSION']
    
VERSIONS = [
    Migration(
        version=1,
        up="create table if not exists test(id int primary key autoincrement, version int)",
        down="drop table test"
    )
]

    



