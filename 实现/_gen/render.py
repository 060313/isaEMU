# 实现框架生成器 —— 渲染工具
# 由 _gen/gen.py 调用；输出根目录 = 实现/
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def emit(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.rstrip() + "\n", encoding="utf-8")
    return p


def origin(title, ref, extra=()):
    lines = ["/**", " * " + title, " *", " * 设计依据：" + ref]
    for e in extra:
        lines.append(" * " + e)
    lines.append(" */")
    return "\n".join(lines)


def inc(s):
    if s.startswith("<") or s.startswith('"'):
        return s
    return '"%s"' % s


def hpp(rel, title, ref, includes=(), body="", extra=()):
    out = ["#pragma once", "", origin(title, ref, extra), ""]
    if includes:
        out += ["#include %s" % inc(i) for i in includes]
        out.append("")
    out += ["namespace isa {", "", body.strip(), "", "}  // namespace isa"]
    emit(rel, "\n".join(out))


def cpp(rel, title, ref, includes=(), body="", extra=()):
    out = [origin(title, ref, extra), ""]
    out += ["#include %s" % inc(i) for i in includes]
    out += ["", "namespace isa {", "", body.strip(), "", "}  // namespace isa"]
    emit(rel, "\n".join(out))


def st(name, fields=(), doc="", eq=False, note=""):
    """渲染一个 struct 定义。fields 元素为 (名字, 类型) 或 (名字, 类型, 注释)。"""
    out = []
    if doc:
        out.append("// " + doc)
    out.append("struct %s {" % name)
    if note:
        out.append("    // " + note)
    for f in fields:
        fn, ft = f[0], f[1]
        fc = f[2] if len(f) > 2 else ""
        line = "    %s %s;" % (ft, fn)
        if fc:
            line += "  // " + fc
        out.append(line)
    if not fields and not note:
        out.append("    // （骨架：暂无字段）")
    if eq:
        cond = " && ".join("%s == o.%s" % (f[0], f[0]) for f in fields)
        out.append("")
        out.append("    bool operator==(const %s& o) const { return %s; }" % (name, cond))
    out.append("};")
    return "\n".join(out)


def en(name, vals, doc="", bit=""):
    """渲染一个枚举。bit 非空时生成位掩码运算符，值为该枚举的底层类型。"""
    out = []
    if doc:
        out.append("// " + doc)
    out.append("enum class %s {" % name)
    for v in vals:
        out.append("    %s," % v)
    out.append("};")
    if bit:
        b = bit
        out.append("")
        out.append("inline %s operator|(%s a, %s b) {" % (name, name, name))
        out.append("    return static_cast<%s>(static_cast<%s>(a) | static_cast<%s>(b));"
                   % (name, b, b))
        out.append("}")
        out.append("inline %s operator&(%s a, %s b) {" % (name, name, name))
        out.append("    return static_cast<%s>(static_cast<%s>(a) & static_cast<%s>(b));"
                   % (name, b, b))
        out.append("}")
        out.append("inline bool has(%s set, %s f) {" % (name, name))
        out.append("    return (static_cast<%s>(set) & static_cast<%s>(f)) != 0;" % (b, b))
        out.append("}")
    return "\n".join(out)


def stub_void(what):
    return "    (void)this;\n    // TODO: 实现 —— %s" % what


def err_line(ctype, what):
    return ('    return Result<%s>::err(ErrCode::NotImplemented, "%s");' % (ctype, what))
