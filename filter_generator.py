from __future__ import annotations
from typing import Any, List, Dict, Protocol
import json


class SetOpProtocol(Protocol):
    def _set_op(self, op: str, value: Any) -> BasicFilter:
        raise NotImplementedError


class FilterBase:
    def __init__(self):
        self.filter = {}

    def _set_op(self, op: str, value: Any):
        self.filter[op] = value
        return self


class BasicFilter(FilterBase):
    def __init__(self, property_name: str):
        super().__init__()
        self.filter["property"] = property_name

    def to_dict(self) -> Dict[str, Any]:
        return self.filter

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.filter, **kwargs)


# Mixins
class EqualsMixin(SetOpProtocol):
    def equals(self, value: Any) -> BasicFilter:
        return self._set_op("equals", value)


class DoesNotEqualMixin(SetOpProtocol):
    def does_not_equal(self, value: Any):
        return self._set_op("does_not_equal", value)


class IsEmptyMixin(SetOpProtocol):
    def is_empty(self) -> BasicFilter:
        return self._set_op("is_empty", True)


class IsNotEmptyMixin(SetOpProtocol):
    def is_not_empty(self) -> BasicFilter:
        return self._set_op("is_not_empty", True)


class GreaterThanMixin(SetOpProtocol):
    def greater_than(self, value: Any) -> BasicFilter:
        return self._set_op("greater_than", value)


class GreaterThanOrEqualMixin(SetOpProtocol):
    def greater_than_or_equal_to(self, value: Any) -> BasicFilter:
        return self._set_op("greater_than_or_equal_to", value)


class LessThanMixin(SetOpProtocol):
    def less_than(self, value: Any) -> BasicFilter:
        return self._set_op("less_than", value)


class LessThanOrEqualMixin(SetOpProtocol):
    def less_than_or_equal_to(self, value: Any) -> BasicFilter:
        return self._set_op("less_than_or_equal_to", value)


class ContainsMixin(SetOpProtocol):
    def contains(self, value: Any):
        return self._set_op("contains", value)


class DoesNotContainMixin(SetOpProtocol):
    def does_not_contain(self, value: Any):
        return self._set_op("does_not_contain", value)


class EndsWithMixin(SetOpProtocol):
    def ends_with(self, value: Any) -> BasicFilter:
        return self._set_op("ends_with", value)


class StartsWithMixin(SetOpProtocol):
    def starts_with(self, value: Any) -> BasicFilter:
        return self._set_op("starts_with", value)


# Typed filters
class CheckboxFilter(BasicFilter, EqualsMixin, DoesNotEqualMixin):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "checkbox"


class DateFilter(BasicFilter, EqualsMixin, IsEmptyMixin, IsNotEmptyMixin):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "date"

    def after(self, value: str):
        return self._set_op("after", value)

    def before(self, value: str):
        return self._set_op("before", value)


# More Typed filters
class FilesFilter(BasicFilter, IsEmptyMixin, IsNotEmptyMixin):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "files"


class MultiSelectFilter(
    BasicFilter, EqualsMixin, DoesNotEqualMixin, IsEmptyMixin, IsNotEmptyMixin
):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "multi_select"

    def contains(self, value: str):
        return self._set_op("contains", value)

    def does_not_contain(self, value: str):
        return self._set_op("does_not_contain", value)


class NumberFilter(
    BasicFilter,
    GreaterThanMixin,
    GreaterThanOrEqualMixin,
    LessThanMixin,
    LessThanOrEqualMixin,
    EqualsMixin,
    DoesNotEqualMixin,
    IsEmptyMixin,
    IsNotEmptyMixin,
):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "number"


class PeopleFilter(
    BasicFilter, ContainsMixin, DoesNotContainMixin, IsEmptyMixin, IsNotEmptyMixin
):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "people"


class RelationFilter(
    BasicFilter, ContainsMixin, DoesNotContainMixin, IsEmptyMixin, IsNotEmptyMixin
):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "relation"


class RichTextFilter(
    BasicFilter,
    ContainsMixin,
    DoesNotContainMixin,
    DoesNotEqualMixin,
    EndsWithMixin,
    EqualsMixin,
    StartsWithMixin,
    IsEmptyMixin,
    IsNotEmptyMixin,
):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "rich_text"


class SelectFilter(
    BasicFilter, EqualsMixin, DoesNotEqualMixin, IsEmptyMixin, IsNotEmptyMixin
):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "select"


class StatusFilter(
    BasicFilter, EqualsMixin, DoesNotEqualMixin, IsEmptyMixin, IsNotEmptyMixin
):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "status"


class UniqueIdFilter(
    BasicFilter,
    GreaterThanMixin,
    GreaterThanOrEqualMixin,
    LessThanMixin,
    LessThanOrEqualMixin,
    EqualsMixin,
    DoesNotEqualMixin,
):
    def __init__(self, property_name: str):
        super().__init__(property_name)
        self.filter["type"] = "unique_id"


# Special Cases
class FormulaFilter(BasicFilter):
    def __init__(self, property_name: str, type_name: str, inner_filter: BasicFilter):
        super().__init__(property_name)
        self.filter["type"] = "formula"
        self.filter[type_name] = inner_filter.to_dict()


class RollupFilter(BasicFilter):
    def __init__(
        self,
        property_name: str,
        operator: str,
        type_name: str,
        inner_filter: BasicFilter,
    ):
        super().__init__(property_name)
        self.filter["type"] = "rollup"
        self.filter[operator] = {type_name: inner_filter.to_dict()}


class TimestampFilter(FilterBase, EqualsMixin, IsEmptyMixin, IsNotEmptyMixin):
    def __init__(self, timestamp: str):
        super().__init__()
        self.filter["timestamp"] = timestamp


# Compound filters
class CompoundFilter:
    def __init__(self, operator: str, filters: List[BasicFilter]):
        self.filter = {operator: [f.to_dict() for f in filters]}

    def to_json(self):
        return json.dumps(self.filter)
