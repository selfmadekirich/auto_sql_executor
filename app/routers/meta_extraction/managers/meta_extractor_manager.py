from ..base_extractor import MetaExtractor
from ..pg_extractor import PgMetaExtractor
from models.db_connections import DBConnections
from ...admin.models import SupportedDbTypes
from ..models import MetaExtractorConfig
from ...metadata.models import TableMetadataInput


class MetaExtractorManager:
    def __init__(self, db_conn: DBConnections, reflect=True):
        m = MetaExtractorConfig.from_db_connections(db_conn)
        self.extractor: MetaExtractor = self._get_extractor(db_conn.db_type)(
            m, reflect
        )

    def extract(self) -> list[TableMetadataInput]:
        return self.extractor.extract_meta()

    def execute_sql(self, raw_sql: str) -> dict:
        return self.extractor.execute_custom_sql(raw_sql)

    def _get_extractor(self, db_type: str):
        d = {
            SupportedDbTypes.Postgres: PgMetaExtractor,
            SupportedDbTypes.MySQL: None
        }

        if db_type not in d.keys():
            raise Exception("invalid db type")

        return d.get(db_type)
