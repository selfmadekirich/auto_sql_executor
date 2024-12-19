from .base_extractor import MetaExtractor
from .models import MetaExtractorConfig
from ..metadata.models import TableMetadataInput
from sqlalchemy import create_engine, MetaData


class PgMetaExtractor(MetaExtractor):
    def __init__(self, config: MetaExtractorConfig):
        super().__init__(config)
        self.uri = self._get_connection_uri()
        self.engine = create_engine(
            self.uri, echo=True,
            pool_pre_ping=True
        )

        self.meta_data = MetaData()
        self.meta_data.reflect(bind=self.engine)

    def _get_connection_uri(self) -> str:
        c = self.config
        return "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
                c.user, c.passw,
                c.host, c.port,
                c.db_name
        )

    def extract_meta(self) -> list[TableMetadataInput]:
        tables = self.meta_data.tables
        lst = []
        for t in tables:
            tables_info: dict = {}
            tables_info["table_name"] = t
            tables_info["schema_name"] = tables[t].schema
            tables_info["comment"] = tables[t].comment
            cols = []
            all_columns = tables[t].columns
            for col in all_columns:
                name = col.name
                cols.append({
                    "name": name,
                    "type": all_columns[name].type,
                    "nullable": all_columns[name].nullable,
                    "comment": all_columns[name].comment
                })
            tables_info["json_props"] = cols
            lst.append(TableMetadataInput(**tables_info))
        return lst
