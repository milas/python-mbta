import enum
import typing

Page = typing.NamedTuple('Page', [('offset', int), ('limit', int)])
Point = typing.NamedTuple('Point', [('latitude', float), ('longitude', float)])


class SortOrder(enum.Enum):
    asc = 'asc'
    desc = 'desc'


Sort = typing.NamedTuple('Sort', [('field', str), ('order', SortOrder)])
Filter = typing.NamedTuple('Filter', [('field', str), ('value', typing.Any)])
MultiFilter = typing.NamedTuple('MultiFilter', [('field', str), ('values', typing.Iterable[str])])


def make_multifilter(key: str, value):
    if value is None:
        return None

    to_filter = [value]
    if not isinstance(value, str):
        try:
            to_filter = list(x for x in value if x is not None)
        except TypeError:
            pass

    if len(to_filter) == 0:
        return None

    return MultiFilter(field=key, values=to_filter)


class WheelchairAccess(enum.Enum):
    Unknown = 0
    Accessible = 1
    Inaccessible = 2


class MbtaModel(object):
    @staticmethod
    def make_multifilter(key: str, value):
        return make_multifilter(key, value)

    @staticmethod
    def build_params(
            *args,
            include: typing.Iterable[str]=None,
            location: Point=None,
            page: Page=None,
            sort: Sort=None
    ) -> typing.Dict[str, str]:
        params = {}

        for arg in args:
            if arg is None:
                continue
            if isinstance(arg, Filter):
                params[f'filter[{arg.field}]'] = arg.value
            elif isinstance(arg, MultiFilter):
                params[f'filter[{arg.field}]'] = ','.join(str(x) for x in arg.values)
            elif isinstance(arg, tuple):
                params[arg[0]] = arg[1]

        if location:
            params['filter[latitude]'] = location.latitude
            params['filter[longitude]'] = location.longitude

        if page:
            params['page[offset]'] = page.offset
            params['page[limit]'] = page.limit

        if sort:
            params['sort'] = f'{sort.field}' if sort.order.asc else f'-{sort.field}'

        if include:
            params['include'] = ','.join(include)

        return params
