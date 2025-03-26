from .models import (
    DbConnectionResponse,
    ConnectionsOptionValues,
    DbConnectionPartialResponse
)


def wrap_values(lst: list, flag_value: ConnectionsOptionValues):
    match flag_value:
        case ConnectionsOptionValues.all:
            return [DbConnectionResponse.from_orm(x) for x in lst]
        case ConnectionsOptionValues.partly:
            return [DbConnectionPartialResponse.from_orm(x) for x in lst]
    return None
