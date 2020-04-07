"""
Maps of builtin types and names

You can update this file by executing it, using the PG* env var to connect
to a Postgres server.
"""

# Copyright (C) 2020 The Psycopg Team

import re
from typing import Dict, Generator, Optional, NamedTuple, Union

INVALID_OID = 0


class TypeInfo(NamedTuple):
    name: str
    oid: int
    array_oid: int
    alt_name: str
    delimiter: str


class TypesRegistry:
    """
    Container for the information about types in a database.
    """

    def __init__(self) -> None:
        self._by_oid: Dict[int, TypeInfo] = {}
        self._by_name: Dict[str, TypeInfo] = {}

    def add(self, info: TypeInfo) -> None:
        self._by_oid[info.oid] = info
        if info.array_oid:
            self._by_oid[info.array_oid] = info
        self._by_name[info.name] = info
        if info.alt_name not in self._by_name:
            self._by_name[info.alt_name] = info

    def __iter__(self) -> Generator[TypeInfo, None, None]:
        seen = set()
        for t in self._by_oid.values():
            if t.oid not in seen:
                seen.add(t.oid)
                yield t

    def __getitem__(self, key: Union[str, int]) -> TypeInfo:
        if isinstance(key, str):
            return self._by_name[key]
        elif isinstance(key, int):
            return self._by_oid[key]
        else:
            raise TypeError(
                f"the key must be an oid or a name, got {type(key)}"
            )

    def get(self, key: Union[str, int]) -> Optional[TypeInfo]:
        try:
            return self[key]
        except KeyError:
            return None


builtins = TypesRegistry()

for r in [
    # fmt: off
    # autogenerated: start

    # Generated from PostgreSQL 12.2

    ('aclitem', 1033, 1034, 'aclitem', ','),
    ('any', 2276, 0, '"any"', ','),
    ('anyarray', 2277, 0, 'anyarray', ','),
    ('anyelement', 2283, 0, 'anyelement', ','),
    ('anyenum', 3500, 0, 'anyenum', ','),
    ('anynonarray', 2776, 0, 'anynonarray', ','),
    ('anyrange', 3831, 0, 'anyrange', ','),
    ('bit', 1560, 1561, 'bit', ','),
    ('bool', 16, 1000, 'boolean', ','),
    ('box', 603, 1020, 'box', ';'),
    ('bpchar', 1042, 1014, 'character', ','),
    ('bytea', 17, 1001, 'bytea', ','),
    ('char', 18, 1002, '"char"', ','),
    ('cid', 29, 1012, 'cid', ','),
    ('cidr', 650, 651, 'cidr', ','),
    ('circle', 718, 719, 'circle', ','),
    ('cstring', 2275, 1263, 'cstring', ','),
    ('date', 1082, 1182, 'date', ','),
    ('daterange', 3912, 3913, 'daterange', ','),
    ('event_trigger', 3838, 0, 'event_trigger', ','),
    ('float4', 700, 1021, 'real', ','),
    ('float8', 701, 1022, 'double precision', ','),
    ('gtsvector', 3642, 3644, 'gtsvector', ','),
    ('inet', 869, 1041, 'inet', ','),
    ('int2', 21, 1005, 'smallint', ','),
    ('int2vector', 22, 1006, 'int2vector', ','),
    ('int4', 23, 1007, 'integer', ','),
    ('int4range', 3904, 3905, 'int4range', ','),
    ('int8', 20, 1016, 'bigint', ','),
    ('int8range', 3926, 3927, 'int8range', ','),
    ('internal', 2281, 0, 'internal', ','),
    ('interval', 1186, 1187, 'interval', ','),
    ('json', 114, 199, 'json', ','),
    ('jsonb', 3802, 3807, 'jsonb', ','),
    ('jsonpath', 4072, 4073, 'jsonpath', ','),
    ('line', 628, 629, 'line', ','),
    ('lseg', 601, 1018, 'lseg', ','),
    ('macaddr', 829, 1040, 'macaddr', ','),
    ('macaddr8', 774, 775, 'macaddr8', ','),
    ('money', 790, 791, 'money', ','),
    ('name', 19, 1003, 'name', ','),
    ('numeric', 1700, 1231, 'numeric', ','),
    ('numrange', 3906, 3907, 'numrange', ','),
    ('oid', 26, 1028, 'oid', ','),
    ('oidvector', 30, 1013, 'oidvector', ','),
    ('opaque', 2282, 0, 'opaque', ','),
    ('path', 602, 1019, 'path', ','),
    ('point', 600, 1017, 'point', ','),
    ('polygon', 604, 1027, 'polygon', ','),
    ('record', 2249, 2287, 'record', ','),
    ('refcursor', 1790, 2201, 'refcursor', ','),
    ('text', 25, 1009, 'text', ','),
    ('tid', 27, 1010, 'tid', ','),
    ('time', 1083, 1183, 'time without time zone', ','),
    ('timestamp', 1114, 1115, 'timestamp without time zone', ','),
    ('timestamptz', 1184, 1185, 'timestamp with time zone', ','),
    ('timetz', 1266, 1270, 'time with time zone', ','),
    ('trigger', 2279, 0, 'trigger', ','),
    ('tsquery', 3615, 3645, 'tsquery', ','),
    ('tsrange', 3908, 3909, 'tsrange', ','),
    ('tstzrange', 3910, 3911, 'tstzrange', ','),
    ('tsvector', 3614, 3643, 'tsvector', ','),
    ('txid_snapshot', 2970, 2949, 'txid_snapshot', ','),
    ('unknown', 705, 0, 'unknown', ','),
    ('uuid', 2950, 2951, 'uuid', ','),
    ('varbit', 1562, 1563, 'bit varying', ','),
    ('varchar', 1043, 1015, 'character varying', ','),
    ('void', 2278, 0, 'void', ','),
    ('xid', 28, 1011, 'xid', ','),
    ('xml', 142, 143, 'xml', ','),
    # autogenerated: end
    # fmt: on
]:
    builtins.add(TypeInfo(*r))


def self_update() -> None:
    import subprocess as sp

    queries = [
        """
select format($$
# Generated from PostgreSQL %s.%s
$$,
        setting::int / 10000, setting::int % 100)   -- assume PG >= 10
    from pg_settings
    where name = 'server_version_num'
""",
        r"""
select format(
        '(%L, %s, %s, %L, %L),',
        typname, oid, typarray, oid::regtype, typdelim)
    from pg_type
    where oid < 10000
    and typname !~ all('{^(_|pg_|reg),_handler$}')
    order by typname
""",
    ]

    with open(__file__, "rb") as f:
        lines = f.read().splitlines()

    new = []
    for query in queries:
        out = sp.run(
            ["psql", "-AXqt", "-c", query], stdout=sp.PIPE, check=True
        )
        new.extend(out.stdout.splitlines())

    new = [b" " * 4 + l if l else b"" for l in new]  # indent
    istart, iend = [
        i
        for i, l in enumerate(lines)
        if re.match(br"\s*#\s*autogenerated:\s+(start|end)", l)
    ]
    lines[istart + 1 : iend] = new

    with open(__file__, "wb") as f:
        f.write(b"\n".join(lines))
        f.write(b"\n")


if __name__ == "__main__":
    self_update()
