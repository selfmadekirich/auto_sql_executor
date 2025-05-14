import re
from .base_extractor import MetaExtractor
from .models import MetaExtractorConfig, ExtractorMetaTable
from ..metadata.models import TableMetadataInput
from sqlalchemy import create_engine, MetaData, text


class PgMetaExtractor(MetaExtractor):
    def __init__(self, config: MetaExtractorConfig, reflect=True):
        super().__init__(config)
        self.uri = self._get_connection_uri()
        self.engine = create_engine(
            self.uri, echo=True,
            pool_pre_ping=True
        )

        self.meta_data = MetaData(schema=config.schema_name)
        if reflect:
            self.meta_data.reflect(bind=self.engine)

    def _get_connection_uri(self) -> str:
        c = self.config
        return "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
                c.user, c.passw,
                c.host, c.port,
                c.db_name
        )

    def execute_custom_sql(
        self,
        raw_sql: str,
        page: int = 1,
        size: int = 15
    ) -> list[dict]:
        # @TODO: wrap in decorator
        existing_limit = size
        offset = (page - 1) * size

        limit_match = re.search(r'\sLIMIT\s+(\d+)', raw_sql, re.IGNORECASE)

        if limit_match:
            existing_limit = int(limit_match.group(1))

        limit = existing_limit
        offset_str = f"OFFSET {offset}"

        if existing_limit >= size:
            limit = size
            raw_sql = re.sub(
                r'\sLIMIT\s+\d+', '', raw_sql, flags=re.IGNORECASE
            )

        raw_sql = re.sub(
                r'\sOFFSET\s+\d+', '', raw_sql, flags=re.IGNORECASE
            )
        raw_sql = raw_sql.replace(';', '')

        paginated_sql = f"{raw_sql} LIMIT {limit} {offset_str}"

        with self.engine.connect() as connection:
            result = connection.execute(text(paginated_sql))
            return [x._asdict() for x in result]

    def _row2dict(self, row):
        dict((col, getattr(row, col)) for col in row.__table__.columns.keys())

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
