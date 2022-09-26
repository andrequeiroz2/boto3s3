from fastapi.responses import ORJSONResponse as BaseORJSONResponse
from sqlalchemy.engine import RowMapping
from decimal import Decimal
from typing import Any
import numpy as np

try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


def json_serializer(obj):
    """
    Serialize formatos nao serializaveis por padrao no JSON
    Deve retornar o formato novo ou TypeError, caso contrario o valor ficara null, passando a false impressao
        de que foi serializado com sucesso.
    :param obj: dicionario para serializar
    :return: objeto serializado em Json
    """
    if isinstance(obj, Decimal):
        return float(obj)

    if isinstance(obj, RowMapping):
        return dict(obj)

    if isinstance(obj, np.float):
        return float(obj)

    raise TypeError


class ORJSONResponse(BaseORJSONResponse):
    def render(self, content: Any) -> bytes:  # skipcq: PYL-R0201
        if not orjson:
            raise ImportError("orjson must be installed to use ORJSONResponse")

        return orjson.dumps(content, default=json_serializer)
