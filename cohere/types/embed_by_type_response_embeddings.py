# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from ..core.unchecked_base_model import UncheckedBaseModel


class EmbedByTypeResponseEmbeddings(UncheckedBaseModel):
    """
    An object with different embedding types. The length of each embedding type array will be the same as the length of the original `texts` array.
    """

    float_: typing.Optional[typing.List[typing.List[float]]] = pydantic_v1.Field(alias="float", default=None)
    """
    An array of float embeddings.
    """

    int8: typing.Optional[typing.List[typing.List[int]]] = pydantic_v1.Field(default=None)
    """
    An array of signed int8 embeddings. Each value is between -128 and 127.
    """

    uint8: typing.Optional[typing.List[typing.List[int]]] = pydantic_v1.Field(default=None)
    """
    An array of unsigned int8 embeddings. Each value is between 0 and 255.
    """

    binary: typing.Optional[typing.List[typing.List[int]]] = pydantic_v1.Field(default=None)
    """
    An array of packed signed binary embeddings. The length of each binary embedding is 1/8 the length of the float embeddings of the provided model. Each value is between -128 and 127.
    """

    ubinary: typing.Optional[typing.List[typing.List[int]]] = pydantic_v1.Field(default=None)
    """
    An array of packed unsigned binary embeddings. The length of each binary embedding is 1/8 the length of the float embeddings of the provided model. Each value is between 0 and 255.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}