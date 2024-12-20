from .base_extractor import MetaExtractor
from .models import MetaExtractorConfig, ExtractorMetaTable
from ..metadata.models import TableMetadataInput
from sqlalchemy import create_engine, MetaData, text


class PgMetaExtractor(MetaExtractor):
    def __init__(self, config: MetaExtractorConfig):
        super().__init__(config)
        self.uri = self._get_connection_uri()
        self.engine = create_engine(
            self.uri, echo=True,
            pool_pre_ping=True
        )

        self.meta_data = MetaData(schema=config.schema_name)
        self.meta_data.reflect(bind=self.engine)

    def _get_connection_uri(self) -> str:
        c = self.config
        return "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
                c.user, c.passw,
                c.host, c.port,
                c.db_name
        )

    def execute_custom_sql(self, raw_sql: str) -> dict:
        with self.engine.connect() as connection:
            result = connection.execute(text(raw_sql))
            return result.fetchall()

    def extract_meta(self) -> list[TableMetadataInput]:
        tables = self.meta_data.tables
        lst = []
        for t in tables:
            tables_info: dict = {}
            tables_info["connection_id"] = self.config.connection_id
            tables_info["table_name"] = t
            tables_info["schema_name"] = tables[t].schema
            tables_info["comment"] = tables[t].comment
            cols = []
            all_columns = tables[t].columns
            for col in all_columns:
                name = col.name
                cols.append({
                    "name": name,
                    "type": str(all_columns[name].type),
                    "nullable": all_columns[name].nullable,
                    "comment": all_columns[name].comment
                })
            tables_info["json_props"] = {}
            tables_info["json_props"]["columns"] = cols
            lst.append(
                ExtractorMetaTable(**tables_info).to_table_metadata_input()
            )
        return lst
