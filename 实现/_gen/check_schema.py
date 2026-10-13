# -*- coding: utf-8 -*-
"""校验两份 DDL 的结构计数是否与数据设计基线一致。

基线（详细设计 7.3 / 类设计说明 4.6）：11 张业务表、83 列、13 个外键、9 个索引。
schema_version 是构建期元数据表，不计入上述计数。
"""
import pathlib
import re
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema"

EXPECT_TABLES = 11
EXPECT_COLUMNS = 83
EXPECT_FKS = 13
EXPECT_IX = 9
EXPECT_FK_RANGE = 13

META_TABLE = "schema_version"


def sqlite_counts():
    text = (SCHEMA / "sqlite_schema.sql").read_text(encoding="utf-8")
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(text)
    q = con.execute
    tabs = [r[0] for r in q(
        "select name from sqlite_master where type='table' "
        "and name not like 'sqlite_%' and name <> ?", (META_TABLE,))]
    cols = sum(len(list(q("pragma table_info(%s)" % t))) for t in tabs)
    fks = sum(len(list(q("pragma foreign_key_list(%s)" % t))) for t in tabs)
    return sorted(tabs), cols, fks


def main():
    tabs, cols, fks = sqlite_counts()
    ok = True

    rows = (
        ("业务表", len(tabs), EXPECT_TABLES, str(len(tabs))),
        ("列", cols, EXPECT_COLUMNS, ""),
        ("外键", fks, EXPECT_FKS, ""),
    )
    for name, got, want, _ in rows:
        flag = "OK" if got == want else "**不一致**"
        ok = ok and got == want
        print("%-6s %3d / 期望 %3d  %s" % (name, got, want, flag))

    print("表清单：%s" % " ".join(tabs))

    # 两份 DDL 的编号覆盖：IX-01 ~ IX-09、FK-01 ~ FK-13
    for fname in ("sqlite_schema.sql", "postgres_schema.sql"):
        text = (SCHEMA / fname).read_text(encoding="utf-8")
        ix = sorted(set(re.findall(r"IX-0\d", text)))
        fk = ["FK-%02d" % i for i in range(1, EXPECT_FK_RANGE + 1)]
        missing_fk = [x for x in fk if x not in text]
        flag_ix = "OK" if len(ix) == EXPECT_IX else "**不一致**"
        flag_fk = "OK" if not missing_fk else "**缺 %s**" % ",".join(missing_fk)
        ok = ok and len(ix) == EXPECT_IX and not missing_fk
        print("%-20s IX %d/%d %s   FK %d/%d %s"
              % (fname, len(ix), EXPECT_IX, flag_ix,
                 EXPECT_FK_RANGE - len(missing_fk), EXPECT_FK_RANGE, flag_fk))

    print("== DDL 自检%s ==" % ("通过" if ok else "未通过"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
