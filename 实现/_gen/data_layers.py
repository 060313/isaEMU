# -*- coding: utf-8 -*-
"""各子系统的契约接口与实现类（SS-1 ~ SS-8）。"""
import re
from render import emit, hpp, cpp, st, en

V = '"isa/values.hpp"'


# ------------------------------------------------------------------ 渲染器

def _decl(ret, sig, static=False):
    return "    static %s %s;" % (ret, sig) if static else "    %s %s;" % (ret, sig)


def _path(f, key="file"):
    """公共共享类型放 include/，其余子系统文件放 src/。"""
    return ("include/" if f.get("public") else "src/") + f[key]


def iface_hpp(f):
    name = f["name"]
    body = ["class %s {" % name, "public:", "    virtual ~%s() = default;" % name, ""]
    for m in f["pub"]:
        static = len(m) > 3 and m[3] == "static"
        doc = m[2] if len(m) > 2 else ""
        body.append("    " + ("static " if static else "virtual ") + "%s %s%s;" %
                    (m[0], m[1], "" if static else " = 0"))
        if doc:
            body.append("    // " + doc)
    body.append("};")
    hpp(_path(f), f["title"], f["ref"], f["includes"], "\n".join(body))


def cls_hpp(f):
    name = f["name"]
    bases = (" : " + ", ".join(f["bases"])) if f.get("bases") else ""
    body = ["class %s%s {" % (name, bases), "public:"]
    if f.get("ctor"):
        body.append("    " + f["ctor"])
        body.append("")
    for m in f["pub"]:
        body.append(_decl(m[0], m[1], len(m) > 3 and m[3] == "static"))
        if len(m) > 2 and m[2]:
            body.append("    // " + m[2])
    priv = []
    if f.get("ctor_priv"):
        priv.append("    " + f["ctor_priv"])
    for m in f.get("priv", []):
        priv.append(_decl(m[0], m[1], len(m) > 3 and m[3] == "static"))
        if len(m) > 2 and m[2]:
            priv.append("    // " + m[2])
    for a in f.get("attrs", []):
        line = "    %s %s;" % (a[1], a[0])
        if len(a) > 2 and a[2]:
            line += "  // " + a[2]
        priv.append(line)
    if priv:
        body.append("")
        body.append("private:")
        body += priv
    body.append("};")
    hpp(_path(f), f["title"], f["ref"], f["includes"], "\n".join(body), extra=f.get("extra", ()))


def _stub(cls, ret, sig, hint=None, over=None, static=False):
    name, _, rest = sig.partition("(")
    name = name.strip()
    close = rest.rfind(")")
    if close >= 0:
        params, tail = rest[:close], rest[close + 1:].strip()
    else:
        params, tail = rest, ""
    params = re.sub(r"\s*=\s*[^,)]+", "", params.strip())   # 定义处去掉默认值
    suffix = (" " + tail) if tail else ""
    head = "%s %s::%s(%s)%s" % (ret, cls, name, params, suffix)
    if over is not None:
        return head + " {\n" + over.rstrip() + "\n}"
    body = ["// TODO: 实现 —— %s" % (hint or name)]
    if ret == "void":
        if not static:
            body.append("(void)this;")
    elif ret.startswith("Result<") and ret.endswith(">"):
        body.append('return %s::err(ErrCode::NotImplemented, "%s::%s");' % (ret, cls, name))
    elif ret == "bool":
        body.append("return false;")
    elif ret.rstrip().endswith("&"):
        base = ret.rstrip().rstrip("&").strip().replace("const ", "")
        body.append("static %s kFallback{};" % base)
        body.append("return kFallback;")
    else:
        body.append("return {};")
    return head + " {\n    " + "\n    ".join(body) + "\n}"


def cls_cpp(f):
    src = ['"%s"' % f["file"]]
    src += f.get("use", [])
    body = []
    if f.get("ctor"):
        sig = f["ctor"].replace("explicit ", "").rstrip(";").strip()
        cname, _, rest = sig.partition("(")
        params = rest.rstrip(")")
        body.append("%s::%s(%s) {\n    // TODO: 构造（注入依赖 / 建立组合成员）\n}"
                    % (f["name"], cname.strip(), params))
    over = f.get("over", {})
    for m in f["pub"] + f.get("priv", []):
        mname = m[1].partition("(")[0].strip()
        body.append(_stub(f["name"], m[0], m[1],
                          m[2] if len(m) > 2 else None,
                          over.get(mname),
                          len(m) > 3 and m[3] == "static"))
    if f.get("extra_impl"):
        body.append(f["extra_impl"])
    cpp(_path(f, "impl"), f["title"], f["ref"], src, "\n\n".join(body))


def gen(f):
    if f.get("body") is not None:
        hpp(_path(f), f["title"], f["ref"], f["includes"], f["body"], extra=f.get("extra", ()))
        return
    if f.get("iface"):
        iface_hpp(f)
    else:
        cls_hpp(f)
    if f.get("impl"):
        cls_cpp(f)


# ================================================================== SS-1 模拟执行内核

SS1 = [
    dict(iface=True,
         file="core/idecode_table.hpp",
         title="IDecodeTable —— 译码表契约（SA-01 依赖倒置：由内核侧定义、ISA 抽象层实现）",
         ref="6.4.2；5.4 表",
         includes=[V, "<cstdint>"],
         name="IDecodeTable",
         pub=[("const Instruction&", "lookup(Enc enc)", "O(1) 下标访问"),
              ("unsigned", "width()", "一条指令的字节宽度")]),

    dict(iface=True,
         file="core/icore_service.hpp",
         title="ICoreService —— 模拟执行内核的对外契约",
         ref="6.4.2；5.4「定义方 SS-1、实现方 EmulatorCore、调用方 SS-5/SS-6」",
         includes=['"core/idecode_table.hpp"', V, "<cstdint>"],
         name="ICoreService",
         pub=[("void", "load(const Image& img, Addr base, const InitState& init)",
               "整体替换式装载"),
              ("void", "attachDecodeTable(const IDecodeTable& dt)", "绑定译码表（可重复调用以切换 ISA）"),
              ("StepDelta", "step(std::uint32_t n)", "执行 n 步；接口不带默认参数，默认值在 EmulatorCore 的声明里"),
              ("RunResult", "run(RunMode m, Addr param, std::uint64_t limit, const CancelToken& tk)",
               "主循环（活动图①）"),
              ("void", "pause()", "置 Paused；在下一次循环判定时生效"),
              ("void", "reset()", "恢复装载初态；保留映像与译码表"),
              ("RunState", "state()", "只读查询；不产生状态转移"),
              ("StateSnapshot", "reads(ReadScope scope)", "取架构状态只读快照（R2：查询路径与执行路径分离）"),
              ("void", "restore(const StateSnapshot& s)", "用快照覆盖 ArchState（R2 新增，UC-07 的回退落点）")]),

    dict(file="core/mem_types.hpp",
         title="内核内部内存与 CSR 类型（档 3）",
         ref="6.3.3 ArchState 的属性类型；不被跨子系统引用",
         includes=[V, "<cstdint>", "<map>", "<vector>"],
         name="", extra=["骨架：CsrFile / MemImage 为 ArchState 的内部结构，不参与跨子系统传递"],
         body=r'''// Page —— 一页内存（稀疏分配，不预分配整段地址空间）
struct Page {
    static constexpr std::size_t kSize = 4096;
    std::vector<std::uint8_t> bytes;  // 长度为 kSize
};

// MemImage —— 稀疏页内存（NFR-Q5 内存用量受控的落点）
class MemImage {
public:
    std::uint8_t readByte(Addr a) const;              // 未写过处读 0
    void writeByte(Addr a, std::uint8_t v);
    MemView view() const;                             // 快照用只读视图
private:
    std::map<PageNo, Page> pages_;  // 按需分配
};

// CsrFile —— CSR 稀疏封装（4096 项）
class CsrFile {
public:
    Word read(CsrId id) const;
    void write(CsrId id, Word v);
    std::vector<std::pair<CsrId, Word>> touched() const;  // 已写过的项（快照用）
private:
    std::map<CsrId, Word> regs_;
};

// WriteOpList —— 一步产生的全部写操作（EmulatorCore::cycle 的产出类型）
using WriteOpList = std::vector<WriteOp>;'''),

    dict(file="core/arch_state.hpp",
         title="ArchState —— 架构状态（SS-1 构件 2）",
         ref="6.4.1 / 6.3.3；档 2（装配可见）",
         includes=['"core/mem_types.hpp"', V, "<array>", "<cstdint>"],
         name="ArchState",
         pub=[("void", "apply(span<const WriteOp> writes)", "差分写回；写 x0 被丢弃（M-03）"),
              ("StateSnapshot", "snapshot(ReadScope scope)", "取只读快照"),
              ("void", "restore(const StateSnapshot& s)", "仅 EmulatorCore 调用"),
              ("Bytes", "read(Addr a, std::size_t n)", "内存读"),
              ("void", "write(Addr a, span<const std::uint8_t> bytes)", "内存写"),
              ("void", "reset(const InitState& init)", "恢复初态")],
         attrs=[("pc_", "Addr", "程序计数器"),
                ("gpr_", "std::array<Word, 32>", "32 个通用寄存器（含 x0）"),
                ("csr_", "CsrFile", "CSR 稀疏封装"),
                ("mem_", "MemImage", "稀疏页内存；空表示未写过处读 0")],
         impl="core/arch_state.cpp",
         use=['"core/mem_types.hpp"']),

    dict(file="core/trace.hpp",
         title="Trace —— 执行轨迹（SS-1 构件 3）",
         ref="6.4.1 / 6.3.3；档 2。轨迹可裁剪为 SA-13 的「可回退」提供落点",
         includes=[V, "<cstdint>", "<deque>"],
         name="Trace",
         ctor="explicit Trace(std::size_t cap);",
         pub=[("void", "enable(bool on)", "关闭时不追加；rewindTo 返回 Err(TraceDisabled)"),
              ("void", "append(const StepRecord& rec)", "追加一条记录"),
              ("span<const StepRecord>", "query(StepNo from, StepNo to)", "按步号区间查询"),
              ("Result<StateSnapshot>", "rewindTo(StepNo target)", "逆序撤销写操作（M-04）"),
              ("void", "trim()", "裁剪至不超限（M-05）"),
              ("StepNo", "base()", "已被裁剪掉的最早步号")],
         attrs=[("rec_", "std::deque<StepRecord>", "尾部追加、头部弹出"),
                ("cap_", "std::size_t", "IConfig.traceCapacity（落地值 1048576）"),
                ("base_", "StepNo", "已被裁剪掉的最早步号"),
                ("on_", "bool", "轨迹开关（与 EmulatorCore.traceOn_ 同步）")],
         impl="core/trace.cpp"),

    dict(file="core/termination_guard.hpp",
         title="TerminationGuard —— 终止与异常判定（SS-1 构件 4）",
         ref="6.4.1 / 6.3.3；档 2",
         includes=[V, "<array>", "<optional>"],
         name="TerminationGuard",
         pub=[("GuardVerdict", "check(const ArchState& st, Enc enc)", "先查终止序列，再查停机条件（M-06）"),
              ("void", "captureFault(const FaultRecord& f)", "写入异常现场"),
              ("void", "reset()", "清除终止与异常标志")],
         attrs=[("last_", "std::array<Enc, 3>", "最近三条指令编码"),
                ("halted_", "bool", "已判定的终止标志"),
                ("fault_", "std::optional<FaultRecord>", "异常现场")],
         impl="core/termination_guard.cpp"),

    dict(file="core/emulator_core.hpp",
         title="EmulatorCore —— 执行内核（SS-1 构件 1）",
         ref="6.4.1 / 6.3.3；档 2。实现 ICoreService",
         includes=['"core/icore_service.hpp"', '"core/arch_state.hpp"',
                   '"core/trace.hpp"', '"core/termination_guard.hpp"', V],
         name="EmulatorCore",
         bases=["public ICoreService"],
         ctor="explicit EmulatorCore(std::size_t traceCapacity);",
         pub=[("void", "load(const Image& img, Addr base, const InitState& init)", "整体替换式装载"),
              ("void", "attachDecodeTable(const IDecodeTable& dt)", "绑定译码表"),
              ("StepDelta", "step(std::uint32_t n = 1)", "执行 n 步（默认 1）"),
              ("RunResult", "run(RunMode m, Addr param, std::uint64_t limit, const CancelToken& tk)", "主循环（M-01）"),
              ("void", "pause()", "请求暂停"),
              ("void", "reset()", "恢复初态"),
              ("RunState", "state()", "只读查询"),
              ("StateSnapshot", "reads(ReadScope scope)", "只读快照"),
              ("void", "restore(const StateSnapshot& s)", "用快照覆盖状态（R2）")],
         priv=[("WriteOpList", "cycle()", "管道四段：取指 → 译码 → 执行 → 写回（M-02）"),
               ("bool", "atBoundary()", "pc 不在映像区间内（FR-4.3 的边界判定）"),
               ("void", "deliver(const StepDelta& d)", "组装增量")],
         attrs=[("arch_", "std::unique_ptr<ArchState>", "组合 R-01"),
                ("trace_", "std::unique_ptr<Trace>", "组合 R-02"),
                ("guard_", "std::unique_ptr<TerminationGuard>", "组合 R-03"),
                ("decode_", "const IDecodeTable*", "非拥有关联；未装载译码表时为空"),
                ("image_", "ImageDesc", "映像摘要；atBoundary() 读它"),
                ("st_", "RunState", "状态图② 的六取值之一"),
                ("steps_", "std::uint64_t", "本次装载后的累计步数"),
                ("limit_", "std::uint64_t", "本次运行的条数上限（参数快照，非会话配置）"),
                ("tk_", "const CancelToken*", "本次运行的取消令牌"),
                ("traceOn_", "bool", "轨迹开关")],
         impl="core/emulator_core.cpp"),
]

# WriteOpList 是内核内部别名（cycle 的产出）
CORE_EXTRA = r'''
// WriteOpList —— 一步产生的全部写操作（内核内部别名；骨架补充为 vector 的具名封装）
using WriteOpList = std::vector<WriteOp>;
'''

# ================================================================== SS-2 ISA 抽象

SS2 = [
    dict(iface=True,
         file="isa/iisa_provider.hpp",
         title="IIsaProvider —— ISA 描述的装载与校验契约",
         ref="6.4.2；5.4「定义方 SS-2、实现方 IsaLoader」",
         includes=[V, "<vector>"],
         name="IIsaProvider",
         pub=[("Result<IsaSpec>", "load(const SourceRef& src)", "解析描述"),
              ("std::vector<Issue>", "validate(const IsaSpec& spec)", "三段校验（M-07）"),
              ("const IDecodeTable&", "buildDecodeTable(const IsaSpec& spec)", "构建译码表"),
              ("std::vector<IsaSpec>", "available()", "内置描述列表")]),

    dict(file="isa/isa_loader.hpp",
         title="IsaLoader —— 描述装载与校验（SS-2 构件 1）",
         ref="6.4.3；档 2",
         includes=['"isa/iisa_provider.hpp"', '"isa/decode_table.hpp"', '"core/idecode_table.hpp"', V, "<vector>"],
         name="IsaLoader",
         bases=["public IIsaProvider"],
         pub=[("Result<IsaSpec>", "load(const SourceRef& src)", "解析"),
              ("std::vector<Issue>", "validate(const IsaSpec& spec)", "三段校验"),
              ("const IDecodeTable&", "buildDecodeTable(const IsaSpec& spec)", "构建并缓存译码表"),
              ("std::vector<IsaSpec>", "available()", "内置描述")],
         priv=[("std::vector<Issue>", "threeStage(const IsaSpec& spec)",
                "三段：完备性 / 寄存器定义 / 编码域自洽（M-07）")],
         attrs=[("active_", "std::optional<IsaSpec>", "最近一次装载（仅作提示，不是「当前 ISA」的权威）"),
                ("table_", "std::unique_ptr<DecodeTable>", "已构建的译码表（组合）")],
         impl="isa/isa_loader.cpp",
         over={"buildDecodeTable": "    // TODO: 构建并缓存译码表\n    return *table_;"}),

    dict(file="isa/decode_table.hpp",
         title="DecodeTable —— 译码表（SS-2 构件 2，不可变）",
         ref="6.4.3 / 6.3.3；档 2。实现 SS-1 定义的 IDecodeTable（SA-01）",
         includes=['"core/idecode_table.hpp"', V, "<cstdint>", "<vector>"],
         name="DecodeTable",
         bases=["public IDecodeTable"],
         ctor_priv="DecodeTable(const IsaSpec& spec, BitMask wide, std::vector<Instruction> rows);",
         pub=[("const Instruction&", "lookup(Enc enc)", "O(1) 下标访问（M-08）"),
              ("unsigned", "width()", "指令宽度"),
              ("DecodeTable", "build(const IsaSpec& spec)", "静态工厂", "static")],
         attrs=[("spec_", "const IsaSpec", "构建它的描述（保留供 width() 与审计）"),
                ("wide_", "const BitMask", "编码宽度位图"),
                ("rows_", "const std::vector<Instruction>", "直表；长度 1 << kMaxEncBits")],
         impl="isa/decode_table.cpp",
         over={"lookup": "    // TODO: 返回 rows_[enc & kMask]；骨架返回静态占位\n"
                         "    static const Instruction kEmpty{};\n    return kEmpty;",
               "build": "    // TODO: 构建直表\n"
                        "    return DecodeTable(spec, BitMask{}, std::vector<Instruction>{});"},
         extra_impl="DecodeTable::DecodeTable(const IsaSpec& spec, BitMask wide, std::vector<Instruction> rows)\n"
                    "    : spec_(spec), wide_(wide), rows_(std::move(rows)) {}"),
]

# ================================================================== SS-3 比对

SS3 = [
    dict(public=True,
         file="isa/compare_types.hpp",
         title="比对共享类型：DiffScope / Divergence（档 1）",
         ref="6.4.4 / 6.3.3；档 1（公开契约）。因被 ICompareService 与 IStore 共同引用，"
             "置于公共头以避免 SS-3 与 SS-5 之间的头文件循环",
         includes=[V, "<optional>", "<string>", "<vector>"],
         name="",
         body=r'''// DiffScope —— 比对子集（不可变）
class DiffScope {
public:
    static DiffScope preset();                              // 默认子集（PC + GPR + 内存写 + 被改 CSR）
    DiffScope configure(FieldMask fields, DiffMode mode) const;  // 内部整体重建
    bool includes(Field f) const;                           // 位掩码判定

    FieldMask fields_{0};   // FR-7.2 的字段子集
    std::uint32_t gprMask_{0xFFFFFFFFu};  // 32 个 GPR 的逐位开关
    DiffMode mode_{DiffMode::Stepwise};
};

// Divergence —— 分歧记录（档 1 数据对象；唯一带可变方法的共享类型）
class Divergence {
public:
    static Divergence make(DivergenceId id, StepNo step, const StateSnapshot& a,
                           const StateSnapshot& b);
    span<const FieldDiff> diffFields() const;
    void update(const Attribution& attr);                   // 唯一可变方法（UC-11）

    // public 只读：读得到，构造后不变
    DivergenceId divId{};
    StepNo stepNo{};
    StateSnapshot sideA;
    StateSnapshot sideB;

private:
    std::vector<FieldDiff> diffs_;          // 差异字段清单
    std::optional<Attribution> attr_{};     // 归因标注
    std::string note_;
};''',),

    dict(iface=True,
         file="compare/icompare_service.hpp",
         title="ICompareService —— 比对契约（SS-3，SA-04 使比对独立成子系统）",
         ref="6.4.2；5.4「定义方 SS-3、实现方 CompareEngine、调用方 SS-5 两个服务」",
         includes=['"isa/compare_types.hpp"', V, "<optional>"],
         name="ICompareService",
         pub=[("std::optional<Divergence>",
               "compare(span<const StepRecord> a, span<const StepRecord> b, const DiffScope& sc, DivergenceId id)",
               "逐条比对；nullopt 表示一致（M-09）"),
              ("std::optional<Divergence>",
               "compareFinal(const StateSnapshot& a, const StateSnapshot& b, const DiffScope& sc, DivergenceId id)",
               "终态比对")]),

    dict(file="compare/compare_engine.hpp",
         title="CompareEngine —— 比对引擎（SS-3 构件 1，零属性）",
         ref="6.4.4 / 6.3.3；类设计总则 G-4「函数式核心」",
         includes=['"compare/icompare_service.hpp"', '"isa/compare_types.hpp"', V, "<optional>"],
         name="CompareEngine",
         bases=["public ICompareService"],
         pub=[("std::optional<Divergence>",
               "compare(span<const StepRecord> a, span<const StepRecord> b, const DiffScope& sc, DivergenceId id)",
               "按步号同步推进，命中首个差异即返回"),
              ("std::optional<Divergence>",
               "compareFinal(const StateSnapshot& a, const StateSnapshot& b, const DiffScope& sc, DivergenceId id)",
               "终态比对"),
              ("std::optional<Divergence>",
               "firstDiff(span<const StepRecord> a, span<const StepRecord> b, const DiffScope& sc, DivergenceId id)",
               "只定位首个分歧（复用同一引擎）")],
         attrs=[],
         impl="compare/compare_engine.cpp"),
]

# ================================================================== 领域数据对象（SS-5 的值对象）

DOMAIN_TYPES = dict(
    public=True,
    file="isa/domain_types.hpp",
    title="领域数据对象（SS-5 的值对象）",
    ref="6.4.5「数据对象的方法」；类设计 6.2 值类型清单",
    includes=[V, '"isa/compare_types.hpp"', "<optional>", "<string>", "<vector>"],
    name="",
    extra=["置于公共头而非 SS-5 目录：Program 被 SS-4 的 IRefSim 与 SS-3 的 DiffRequest 引用，",
           "若放 src/domain/ 会造成头文件层的反向依赖。",
           "注：这些是值对象（6.2 有权威清单），与「设计类」是两个口径（评审 ①-3 / ⑥-3）。"],
    body=r'''// Program —— 已装载的程序（组合进 Workspace，可由选择性保存单独缺席）
struct Program {
    Image image;
    Addr base{0};
    Addr entryPc{0};
    Addr stackPtr{0};
    SourceRef sourceRef{};

    std::string toJson() const;                  // 骨架：以 JSON 文本承载
    static Program fromJson(const std::string& text);
};

// CaseResult —— 单个用例的执行结果（报告明细）
struct CaseResult {
    CaseId caseId{};
    bool passed{false};
    std::optional<StepNo> firstDiffAt{};
    std::vector<FieldDiff> diffFields{};
    std::optional<StateSnapshot> snapshot_{};    // 重字段，列表页不取（DD-3）
};

// TestCase —— 用例
struct TestCase {
    CaseId caseId{};
    std::string name;
    ProgramRef program{};
    std::uint64_t timeoutSteps{0};
    ExpectedSpec expect_{};                      // finalAssert 或 sequence（7.2.3）
};

// TestSuite —— 用例集（1:n 落子表，DD-2 / DD-8）
struct TestSuite {
    SuiteId suiteId{};
    std::string name;
    std::string group;                           // SQL 保留字，列名为 grp
    std::vector<std::string> tags;
    std::vector<TestCase> cases;

    static Result<TestSuite> load(SuiteId id);
    Hash checksum() const;                       // 完整性校验（C-12）
};

// TestReport —— 测试报告汇总
struct TestReport {
    ReportId reportId{};
    SuiteId suiteId{};
    UserId owner{};
    Timestamp startedAt{};
    Timestamp finishedAt{};
    std::vector<CaseResult> results;

    static TestReport summarize(span<const CaseResult> results);
    double passRate() const;                     // 由 passed / total 现算，不存冗余百分比
    int total() const;
    int passed() const;
};

// Workspace —— 工作区（程序 + 用例集 + 配置，均可选择性缺席）
struct Workspace {
    WorkspaceId wsId{};
    UserId owner{};
    Version version{1};
    std::string name;                            // 新增（DD-7）：UC-12 E1 同名冲突判定

    std::optional<Program> program_{};
    std::vector<TestSuite> suite_{};             // DD-8：n:1，由 optional 改为 vector
    SessionConfig config_{};

    std::string toJson() const;
    static Workspace fromJson(const std::string& text);
};

// ReportRow —— 报告列表项（UI-06；不取 snapshot_blob）
struct ReportRow {
    ReportId reportId{};
    UserId owner{};
    SuiteId suiteId{};
    std::string summary;
    std::vector<CaseResult> results;
};

// LoadResult —— 装载结果
struct LoadResult {
    Program program;
    Disasm disasm;
    std::vector<Issue> issues;
};

// DiffRequest —— 对拍请求
struct DiffRequest {
    Program program;
    DiffScope scope;
    JobId jobId;
};''',
)

# ================================================================== SS-4 适配

SS4 = [
    dict(iface=True,
         file="adapt/iassembler.hpp",
         title="IAssembler —— 工具链适配契约（SS-4，SA-06 使外部工具经子进程隔离）",
         ref="6.4.2；5.4「定义方 SS-4、实现方 ToolchainAdapter」",
         includes=[V],
         name="IAssembler",
         pub=[("Result<Image>", "assemble(const SourceRef& src, const CancelToken& tk)",
               "汇编；D-7：不再提供 assembleOnly，「仅汇编不装载」是调用方不调 loadProgram")]),

    dict(iface=True,
         file="adapt/iref_sim.hpp",
         title="IRefSim —— 参考模拟器适配契约（SS-4）",
         ref="6.4.2；5.4「定义方 SS-4、实现方 RefSimAdapter」",
         includes=[V, '"isa/domain_types.hpp"', "<vector>"],
         name="IRefSim",
         pub=[("Result<std::vector<StepRecord>>",
               "run(const Program& p, const DiffScope& sc, const CancelToken& tk)",
               "驱动参考方并解析提交日志"),
              ("bool", "available()", "参考方是否可用")]),

    dict(file="adapt/toolchain_adapter.hpp",
         title="ToolchainAdapter —— 工具链适配器（SS-4 构件 1）",
         ref="6.4.5；档 2。隔离外部工具链",
         includes=['"adapt/iassembler.hpp"', '"isa/domain_types.hpp"', V, "<string>"],
         name="ToolchainAdapter",
         bases=["public IAssembler"],
         ctor="explicit ToolchainAdapter(const IProcessRunner& runner, const IConfig& cfg);",
         pub=[("Result<Image>", "assemble(const SourceRef& src, const CancelToken& tk)", "汇编")],
         priv=[("Result<Image>", "assembleWith(std::string_view args)", "带参数调用子进程"),
               ("std::vector<Issue>", "parseDiagnostics(std::string_view text)", "解析工具链诊断")],
         attrs=[("runner_", "const IProcessRunner*", "关联"),
                ("cfg_", "const IConfig*", "关联；取 toolchainPath()")],
         impl="adapt/toolchain_adapter.cpp"),

    dict(file="adapt/ref_sim_adapter.hpp",
         title="RefSimAdapter —— 参考模拟器适配（SS-4 构件 2）",
         ref="6.4.5；档 2",
         includes=['"adapt/iref_sim.hpp"', V, "<vector>"],
         name="RefSimAdapter",
         bases=["public IRefSim"],
         ctor="explicit RefSimAdapter(const IProcessRunner& runner, const IConfig& cfg);",
         pub=[("Result<std::vector<StepRecord>>",
               "run(const Program& p, const DiffScope& sc, const CancelToken& tk)", "驱动参考方"),
              ("bool", "available()", "可用性探测")],
         priv=[("void", "degrade()", "标记降级（参考方不可用时）")],
         attrs=[("runner_", "const IProcessRunner*", "关联"),
                ("cfg_", "const IConfig*", "关联；取 spikePath()"),
                ("degraded_", "bool", "降级标志")],
         impl="adapt/ref_sim_adapter.cpp"),
]

# ================================================================== SS-5 领域服务

SS5_IFACE = [
    ("i_session_service.hpp", "ISessionService", "会话服务契约", "UC-01 / UC-14",
     [("Result<LoginResult>", "login(const Credential& c)", "取凭据行 → 哑元 KDF → 建会话 + 建工作区（M-10）"),
      ("void", "logout(Token t)", "结束会话"),
      ("Result<SessionContext&>", "contextOf(Token t)", "解析会话上下文（D-3：服务不持有内核引用）"),
      ("std::size_t", "reap(const Clock& now)", "回收超时会话（M-11）"),
      ("std::vector<User>", "listUsers()", "管理员视角的用户列表"),
      ("Result<void>", "updateUser(UserId u, const UserPatch& p)", "配额与状态的局部更新"),
      ("Usage", "queryUsage(UserId u)", "窗口用量")]),

    ("i_isa_service.hpp", "IIsaService", "ISA 管理契约", "UC-02",
     [("Result<IsaSpec>", "loadSpec(const SourceRef& src)", "装载描述"),
      ("std::vector<Issue>", "validate(const IsaSpec& spec)", "校验"),
      ("SpecId", "current()", "当前 ISA 标识"),
      ("Result<void>", "switchTo(SpecId id)", "切换 ISA")]),

    ("i_load_service.hpp", "ILoadService", "装载服务契约", "UC-03 / UC-12",
     [("Result<Image>", "assemble(const SourceRef& src)", "仅汇编（D-7：不接着调 loadProgram 即为「仅汇编不装载」）"),
      ("Result<LoadResult>", "loadProgram(const LoadSpec& s)", "汇编 + 装载（整体替换式）"),
      ("std::vector<ExampleId>", "examples()", "内置示例列表")]),

    ("i_debug_service.hpp", "IDebugService", "调试服务契约", "UC-04 ~ UC-07",
     [("Result<RunResult>", "execute(RunMode m, Addr param, std::uint64_t limit)", "按模式分派（M-12）"),
      ("StateSnapshot", "readState(ReadScope scope)", "读架构状态"),
      ("Result<void>", "rollback(StepNo target)", "回退到指定步"),
      ("std::vector<Breakpoint>", "registerBreakpoint(Addr a, BpOp op)", "断点增删改"),
      ("bool", "checkHit(Addr a)", "断点命中判定")]),

    ("i_test_service.hpp", "ITestService", "测试服务契约", "UC-08 / UC-09",
     [("Result<TestReport>", "runSuite(SuiteId s, DiffMode m, const CancelToken& tk)", "批量执行（M-13）"),
      ("std::vector<ReportRow>", "queryReports(UserId u, std::optional<SuiteId> s)", "报告列表（DD-5）"),
      ("Result<TestReport>", "getReport(UserId u, ReportId id)", "取报告（不含 snapshot_blob）"),
      ("Result<CaseSnapshot>", "snapshotOf(ReportId r, CaseId c)", "取用例复现快照")]),

    ("i_diff_service.hpp", "IDiffService", "对拍服务契约", "UC-10 / UC-11",
     [("Result<JobHandle>", "start(const DiffRequest& req, const CancelToken& tk)", "发起对拍（M-14）"),
      ("Result<Divergence>", "diffDetail(DivergenceId id)", "分歧详情"),
      ("Result<void>", "annotate(span<const DivergenceId> ids, AttributionCategory cat, std::string note)",
       "批量归因（C-14）"),
      ("bool", "degrade()", "参考方降级状态")]),

    ("i_workspace_service.hpp", "IWorkspaceService", "工作区服务契约", "UC-12",
     [("Result<Version>", "save(SaveSelection sel)", "选择性保存"),
      ("Result<Workspace>", "load(WorkspaceId id)", "加载工作区"),
      ("std::vector<WorkspaceBrief>", "list(UserId u)", "工作区列表（UI-09）")]),
]

SS5 = [
    dict(file="domain/session_context.hpp",
         title="SessionContext —— 会话上下文（SS-5 的内部结构，档 3）",
         ref="6.3.3；R3 / SA-03：内核生命周期由会话上下文唯一负责",
         includes=['"core/icore_service.hpp"', '"domain/breakpoint_table.hpp"', V, "<memory>"],
         name="SessionContext",
         ctor="SessionContext(Token t, UserId u, WorkspaceId w, SpecId isa, class IStore& store);",
         pub=[("const Token&", "token() const", "会话令牌"),
              ("UserId", "uid() const", "所有者（隔离谓词来源）"),
              ("WorkspaceId", "ws() const", "默认工作区"),
              ("SpecId", "isa() const", "当前 ISA（会话级；多会话可各用不同 ISA）"),
              ("void", "touch(const Clock& now)", "推进 lastSeen（落库有 tHeartbeat 节流）"),
              ("bool", "expired(const Clock& now, Duration timeout) const", "空闲超时判定"),
              ("ICoreService&", "core()", "D-3：服务经此取内核引用，而不是自行持有"),
              ("BreakpointTable&", "breakpoints()", "断点表")],
         attrs=[("token_", "Token", "构造注入"),
                ("uid_", "UserId", "构造注入"),
                ("ws_", "WorkspaceId", "构造注入"),
                ("isa_", "SpecId", "构造注入"),
                ("lastSeen_", "Timestamp", "构造时 = clock.now()"),
                ("core_", "std::unique_ptr<ICoreService>", "组合 R-05 / SA-03"),
                ("bps_", "std::unique_ptr<BreakpointTable>", "组合 R-06")],
         impl="domain/session_context.cpp",
         over={"core": "    // TODO: 返回内核引用（D-3）\n    return *core_;"}),

    dict(file="domain/breakpoint_table.hpp",
         title="BreakpointTable —— 断点表（SS-5 的内部结构，档 3）",
         ref="6.4.1 / 6.3.3；随工作区持久化（T-10）",
         includes=[V, "<map>", "<vector>"],
         name="BreakpointTable",
         pub=[("std::vector<Breakpoint>", "apply(Addr a, BpOp op)", "增删改（E-09 的八种操作）"),
              ("bool", "hits(Addr a) const", "命中判定"),
              ("const std::vector<Breakpoint>&", "items() const", "全部断点"),
              ("void", "loadFrom(const BreakpointRow& row)", "从持久化行恢复"),
              ("BreakpointRow", "toRow(UserId u, WorkspaceId w) const", "导出为持久化行")],
         attrs=[("on_", "std::map<Addr, Breakpoint>", "按地址索引")],
         impl="domain/breakpoint_table.cpp"),
]

_IFACE_INC = ['"domain/session_context.hpp"', '"isa/domain_types.hpp"', V,
              '"core/idecode_table.hpp"', '"core/icore_service.hpp"', "<optional>", "<vector>"]

SS5 += [
    dict(file="domain/session_service.hpp",
         title="SessionService —— 会话服务（SS-5 构件 1）",
         ref="6.4.5；档 2。实现 ISessionService",
         includes=['"domain/i_session_service.hpp"', '"domain/session_context.hpp"', V, "<map>", "<memory>"],
         name="SessionService",
         bases=["public ISessionService"],
         ctor="SessionService(IStore& store, IIdGen& ids, const IConfig& cfg, ILogger& log);",
         pub=[("Result<LoginResult>", "login(const Credential& c)", "取凭据行 → 哑元 KDF → 建会话（M-10）"),
              ("void", "logout(Token t)", "结束会话"),
              ("Result<SessionContext&>", "contextOf(Token t)", "解析上下文（D-3）"),
              ("std::size_t", "reap(const Clock& now)", "回收超时会话（M-11）"),
              ("std::vector<User>", "listUsers()", "用户列表"),
              ("Result<void>", "updateUser(UserId u, const UserPatch& p)", "更新用户"),
              ("Usage", "queryUsage(UserId u)", "窗口用量")],
         priv=[("Result<LoginResult>", "createSession(const Credential& c)", "建会话 + 建工作区"),
               ("bool", "expired(const SessionContext& ctx, const Clock& now) const", "超时判定")],
         attrs=[("store_", "IStore*", "关联"),
                ("ids_", "IIdGen*", "关联"),
                ("cfg_", "const IConfig*", "关联"),
                ("log_", "ILogger*", "关联"),
                ("live_", "std::map<Token, std::unique_ptr<SessionContext>>", "活跃会话；移出即触发内核析构")],
         impl="domain/session_service.cpp"),

    dict(file="domain/isa_service.hpp",
         title="IsaService —— ISA 管理服务（SS-5 构件 2）",
         ref="6.4.5；档 2。实现 IIsaService",
         includes=['"domain/i_isa_service.hpp"', '"isa/iisa_provider.hpp"', V, "<vector>"],
         name="IsaService",
         bases=["public IIsaService"],
         ctor="IsaService(IIsaProvider& prov, IStore& store, ILogger& log);",
         pub=[("Result<IsaSpec>", "loadSpec(const SourceRef& src)", "装载描述"),
              ("std::vector<Issue>", "validate(const IsaSpec& spec)", "校验"),
              ("SpecId", "current()", "当前 ISA"),
              ("Result<void>", "switchTo(SpecId id)", "切换 ISA")],
         priv=[("Result<void>", "saveActive(const IsaSpec& spec)", "记录最近一次装载（仅作提示）")],
         attrs=[("prov_", "IIsaProvider*", "关联"),
                ("store_", "IStore*", "关联"),
                ("log_", "ILogger*", "关联")],
         impl="domain/isa_service.cpp"),

    dict(file="domain/load_service.hpp",
         title="LoadService —— 装载服务（SS-5 构件 3）",
         ref="6.4.5；档 2。实现 ILoadService；D-7 的决策点在这里",
         includes=['"domain/i_load_service.hpp"', '"domain/session_service.hpp"',
                   '"adapt/iassembler.hpp"', V, "<vector>"],
         name="LoadService",
         bases=["public ILoadService"],
         ctor="LoadService(IAssembler& asm_, IStore& store, SessionService& sess);",
         pub=[("Result<Image>", "assemble(const SourceRef& src)", "仅汇编（D-7）"),
              ("Result<LoadResult>", "loadProgram(const LoadSpec& s)", "汇编 + 装载"),
              ("std::vector<ExampleId>", "examples()", "内置示例")],
         priv=[("ICoreService*", "coreOf(Token t)", "经会话上下文取内核（D-3）")],
         attrs=[("asm_", "IAssembler*", "关联"),
                ("store_", "IStore*", "关联"),
                ("sess_", "SessionService*", "关联")],
         impl="domain/load_service.cpp"),

    dict(file="domain/debug_service.hpp",
         title="DebugService —— 调试服务（SS-5 构件 4）",
         ref="6.4.5；档 2。实现 IDebugService；断点展开在服务层（M-12）",
         includes=['"domain/i_debug_service.hpp"', '"domain/session_service.hpp"', V],
         name="DebugService",
         bases=["public IDebugService"],
         ctor="DebugService(SessionService& sess, ILogger& log);",
         pub=[("Result<RunResult>", "execute(RunMode m, Addr param, std::uint64_t limit)", "按模式分派"),
              ("StateSnapshot", "readState(ReadScope scope)", "读状态"),
              ("Result<void>", "rollback(StepNo target)", "回退"),
              ("std::vector<Breakpoint>", "registerBreakpoint(Addr a, BpOp op)", "断点操作"),
              ("bool", "checkHit(Addr a)", "断点命中")],
         priv=[("Result<WorkspaceId>", "effectiveWs(Token t)", "从会话上下文取工作区（供断点读写）")],
         attrs=[("sess_", "SessionService*", "关联"),
                ("log_", "ILogger*", "关联")],
         impl="domain/debug_service.cpp"),

    dict(file="domain/test_service.hpp",
         title="TestService —— 测试服务（SS-5 构件 5）",
         ref="6.4.5；档 2。实现 ITestService",
         includes=['"domain/i_test_service.hpp"', '"domain/session_service.hpp"',
                   '"compare/icompare_service.hpp"', V, "<map>"],
         name="TestService",
         bases=["public ITestService"],
         ctor="TestService(SessionService& sess, ICompareService& cmp, IStore& store);",
         pub=[("Result<TestReport>", "runSuite(SuiteId s, DiffMode m, const CancelToken& tk)", "批量执行（M-13）"),
              ("std::vector<ReportRow>", "queryReports(UserId u, std::optional<SuiteId> s)", "报告列表"),
              ("Result<TestReport>", "getReport(UserId u, ReportId id)", "取报告"),
              ("Result<CaseSnapshot>", "snapshotOf(ReportId r, CaseId c)", "用例快照")],
         priv=[("TestReport", "summarize(span<const CaseResult> rs)", "汇总"),
               ("CaseResult", "runOne(const TestCase& c, DiffMode m, const CancelToken& tk)", "单用例执行")],
         attrs=[("sess_", "SessionService*", "关联"),
                ("cmp_", "ICompareService*", "关联"),
                ("store_", "IStore*", "关联"),
                ("jobs_", "std::map<JobId, JobEntry>", "在跑的任务")],
         impl="domain/test_service.cpp"),

    dict(file="domain/diff_service.hpp",
         title="DiffService —— 对拍服务（SS-5 构件 6）",
         ref="6.4.5；档 2。实现 IDiffService；任务在批次边界退出（M-14）",
         includes=['"domain/i_diff_service.hpp"', '"domain/session_service.hpp"',
                   '"compare/icompare_service.hpp"', '"adapt/iref_sim.hpp"', V, "<map>"],
         name="DiffService",
         bases=["public IDiffService"],
         ctor="DiffService(SessionService& sess, IRefSim& ref, ICompareService& cmp, IStore& store);",
         pub=[("Result<JobHandle>", "start(const DiffRequest& req, const CancelToken& tk)", "发起对拍"),
              ("Result<Divergence>", "diffDetail(DivergenceId id)", "分歧详情"),
              ("Result<void>", "annotate(span<const DivergenceId> ids, AttributionCategory cat, std::string note)",
               "批量归因"),
              ("bool", "degrade()", "参考方降级")],
         priv=[("std::vector<StepRecord>", "driveCore(const Program& p, const CancelToken& tk)", "驱动内核侧"),
               ("std::vector<StepRecord>", "driveRef(const Program& p, const CancelToken& tk)", "驱动参考方"),
               ("Result<JobEntry&>", "jobOf(JobId j)", "取任务条目")],
         attrs=[("sess_", "SessionService*", "关联"),
                ("ref_", "IRefSim*", "关联"),
                ("cmp_", "ICompareService*", "关联"),
                ("store_", "IStore*", "关联"),
                ("jobs_", "std::map<JobId, JobEntry>", "在跑的任务")],
         impl="domain/diff_service.cpp"),

    dict(file="domain/workspace_service.hpp",
         title="WorkspaceService —— 工作区服务（SS-5 构件 7）",
         ref="6.4.5；档 2。实现 IWorkspaceService",
         includes=['"domain/i_workspace_service.hpp"', '"domain/session_service.hpp"', V, "<vector>"],
         name="WorkspaceService",
         bases=["public IWorkspaceService"],
         ctor="WorkspaceService(IStore& store, SessionService& sess);",
         pub=[("Result<Version>", "save(SaveSelection sel)", "选择性保存（事务 T-1）"),
              ("Result<Workspace>", "load(WorkspaceId id)", "加载工作区"),
              ("std::vector<WorkspaceBrief>", "list(UserId u)", "工作区列表")],
         priv=[("Workspace", "pack(SaveSelection sel)", "把会话现场打包为 Workspace"),
               ("Workspace", "unpack(const WorkspaceRow& row)", "把持久化行还原为 Workspace")],
         attrs=[("store_", "IStore*", "关联"),
                ("sess_", "SessionService*", "关联")],
         impl="domain/workspace_service.cpp"),
]

# ================================================================== SS-6 集成 API

SS6 = [
    dict(file="api/http_gateway.hpp",
         title="HttpGateway —— HTTP / WebSocket 网关（SS-6 构件 1）",
         ref="6.4.6；档 2。UC-01 ~ UC-14 的统一入口",
         includes=[V, '"api/router.hpp"', '"api/access_guard.hpp"', "<string>"],
         name="HttpGateway",
         ctor="HttpGateway(Router& router, AccessGuard& guard);",
         pub=[("HttpResponse", "handle(const HttpRequest& req)", "入口：拆为 unwrap + wrap 两段"),
              ("void", "push(WsSession& ws, const Event& e)", "WebSocket 主动推送（FR-6.4）")],
         priv=[("Result<Payload>", "unwrap(const HttpRequest& req)", "解析请求体、校验 Schema"),
               ("HttpResponse", "wrap(const Result<Payload>& r)", "结果 / 错误统一封装")],
         attrs=[("router_", "Router*", "关联"),
                ("guard_", "AccessGuard*", "关联")],
         impl="api/http_gateway.cpp"),

    dict(file="api/router.hpp",
         title="Router —— 请求路由分发（SS-6 构件 2）",
         ref="6.4.6；档 2。UC-13",
         includes=[V, "<string>"],
         name="Router",
         pub=[("Result<Payload>", "route(const RouteKey& key, const Params& params)", "查表分发并绑定参数")],
         priv=[("Result<Bound>", "bind(const Schema& schema, const Params& params)", "参数绑定与类型校验")],
         attrs=[("table_", "std::map<RouteKey, std::string>", "路由表（骨架：键 → 处理器标识）")],
         impl="api/router.cpp"),

    dict(file="api/access_guard.hpp",
         title="AccessGuard —— 鉴权与配额检查（SS-6 构件 3）",
         ref="6.4.6；档 2。SA-05 的唯一落点",
         includes=[V, "<mutex>"],
         name="AccessGuard",
         ctor="AccessGuard(const IConfig& cfg, IStore& store, ILogger& log);",
         pub=[("Result<Caller>", "authorize(const Credential& c)", "鉴权（方式一）"),
              ("Result<void>", "checkQuota(UserId u, OpKind op)", "配额检查（方式一）"),
              ("Result<void>", "checkInstrLimit(UserId u, std::uint64_t n)",
               "单次请求指令条数上限（与 IConfig.instrLimit 同源，C-02 的收口）")],
         attrs=[("cfg_", "const IConfig*", "关联"),
                ("store_", "IStore*", "关联"),
                ("log_", "ILogger*", "关联"),
                ("rate_", "std::map<UserId, std::pair<std::uint64_t, Timestamp>>", "窗口限流计数（进程内并发，见 7.4.5.1）")],
         impl="api/access_guard.cpp"),

    dict(file="api/bootstrapper.hpp",
         title="Bootstrapper —— 组合根（SS-6 构件 4）",
         ref="6.4.6；SA-08。全项目唯一出现 new 的地方",
         includes=[V, "<memory>"],
         name="",
         extra=["Container 是组合根的产出物：装配完成的各构件引用。",],
         body=r'''class IStore;
class ILogger;
class IConfig;
class SessionService;
class HttpGateway;

// Container —— 装配结果（骨架：只列关键构件，实现时补齐）
struct Container {
    std::unique_ptr<IStore> store;
    std::unique_ptr<SessionService> sessions;
    std::unique_ptr<HttpGateway> gateway;
};

// Bootstrapper —— 组合根
// 约束：全项目只有此处与 SessionContext 的构造出现 new（可用 grep -n "new " src/ 在 CI 里强制）
class Bootstrapper {
public:
    static Container build(const IConfig& cfg);
};'''),
]

# ================================================================== SS-8 基础服务

SS8 = [
    dict(iface=True,
         file="base/i_store.hpp",
         title="IStore —— 持久化服务契约（SS-8；18 个操作）",
         ref="7.4.2 操作清单；6.4.8",
         includes=['"isa/domain_types.hpp"', '"isa/compare_types.hpp"', V,
                   '"isa/span.hpp"', "<optional>", "<string>", "<vector>"],
         name="IStore",
         pub=[("std::optional<User>", "findUser(UserId u)", "O-01；谓词 uid = :u"),
              ("std::optional<User>", "findUserByName(std::string n)", "O-02；免谓词入口（登录前）"),
              ("std::optional<CredentialRow>", "findCredential(std::string n)", "O-03；免谓词入口（DD-1 新增）"),
              ("void", "saveUser(UserId u, const User& x)", "O-04；UPSERT"),
              ("std::vector<User>", "queryUsers()", "O-05；管理员视角"),
              ("Usage", "queryUsage(UserId u)", "O-06；三段组装（DD-4）"),
              ("void", "saveSession(Token t, const SessionRow& r)", "O-07；按 token 定位（免谓词）"),
              ("void", "dropSession(Token t)", "O-08；写 ended_at，不物理删"),
              ("Version", "putWorkspace(UserId u, const Workspace& w)", "O-09；事务 T-1"),
              ("std::optional<Workspace>", "getWorkspace(UserId u, WorkspaceId id)", "O-10；含 optional<Program> / vector<TestSuite>"),
              ("std::vector<WorkspaceBrief>", "queryWorkspaces(UserId u)", "O-11；UI-09 列表（DD-5 新增）"),
              ("void", "saveReport(UserId u, const TestReport& r)", "O-12；事务 T-2"),
              ("std::optional<TestReport>", "getReport(UserId u, ReportId id)", "O-13；不含 snapshot_blob"),
              ("std::vector<ReportRow>", "queryReports(UserId u, std::optional<SuiteId> s)",
               "O-14；UI-06 列表（DD-5 新增）"),
              ("void", "saveBreakpoints(UserId u, const BreakpointRow& b)", "O-15；整表替换"),
              ("BreakpointRow", "loadBreakpoints(UserId u, WorkspaceId w)", "O-16；双参（M-09 签名细化）"),
              ("void", "saveDivergence(UserId u, span<const Divergence> d)", "O-17；批量 INSERT"),
              ("std::vector<Divergence>", "queryDivergence(UserId u, JobId j)",
               "O-18；job_id 为逻辑引用，无外键")]),

    dict(file="base/db_driver.hpp",
         title="DbDriver —— 双形态数据库驱动抽象（SS-8；SA-10 的落点）",
         ref="7.2.2「9 个逻辑类型 / 7 处 DDL 差异由 DbDriver 吸收」",
         includes=[V, "<string>"],
         name="",
         extra=["骨架：只给出接口形状。两个具体驱动（SqliteDriver / PostgresDriver）为后续实现留位。",],
         body=r'''// LogicalType —— 语言的逻辑类型（9 个，7.2.2）；各方言的具体类型由驱动映射
enum class LogicalType {
    U64,        // BIGINT     / INTEGER
    I32,        // INTEGER    / INTEGER
    SmallInt,   // SMALLINT   / INTEGER
    Bool,       // BOOLEAN    / INTEGER
    Text,       // TEXT       / TEXT
    VarChar,    // VARCHAR(n) / TEXT
    Bytes,      // BYTEA      / BLOB
    Json,       // JSONB      / TEXT
    TimePoint,  // TIMESTAMPTZ/ TEXT
};

class DbDriver {
public:
    virtual ~DbDriver() = default;

    virtual DriverKind kind() const = 0;
    virtual std::string dialectFor(LogicalType t) const = 0;  // 9 个逻辑类型 → 方言类型
    virtual std::string nowExpr() const = 0;                  // 时刻表达式
    virtual std::string onConflictClause() const = 0;         // UPSERT 子句
};'''),

    dict(file="base/db_store.hpp",
         title="DbStore —— 持久化服务实现（SS-8）",
         ref="7.4；6.4.8。实现 IStore；D-5 的 scoped 是隔离唯一入口",
         includes=['"base/i_store.hpp"', '"base/db_driver.hpp"', V, "<string>", "<vector>"],
         name="DbStore",
         bases=["public IStore"],
         ctor="explicit DbStore(DbDriver& driver);",
         pub=[("std::optional<User>", "findUser(UserId u)"),
              ("std::optional<User>", "findUserByName(std::string n)"),
              ("std::optional<CredentialRow>", "findCredential(std::string n)"),
              ("void", "saveUser(UserId u, const User& x)"),
              ("std::vector<User>", "queryUsers()"),
              ("Usage", "queryUsage(UserId u)"),
              ("void", "saveSession(Token t, const SessionRow& r)"),
              ("void", "dropSession(Token t)"),
              ("Version", "putWorkspace(UserId u, const Workspace& w)"),
              ("std::optional<Workspace>", "getWorkspace(UserId u, WorkspaceId id)"),
              ("std::vector<WorkspaceBrief>", "queryWorkspaces(UserId u)"),
              ("void", "saveReport(UserId u, const TestReport& r)"),
              ("std::optional<TestReport>", "getReport(UserId u, ReportId id)"),
              ("std::vector<ReportRow>", "queryReports(UserId u, std::optional<SuiteId> s)"),
              ("void", "saveBreakpoints(UserId u, const BreakpointRow& b)"),
              ("BreakpointRow", "loadBreakpoints(UserId u, WorkspaceId w)"),
              ("void", "saveDivergence(UserId u, span<const Divergence> d)"),
              ("std::vector<Divergence>", "queryDivergence(UserId u, JobId j)")],
         priv=[("std::string", "scoped(std::string sql, UserId u)",
                "M-15：唯一拼装入口，追加 AND owner_id = :u；参数经占位符绑定（不拼字符串）")],
         attrs=[("driver_", "DbDriver*", "关联")],
         impl="base/db_store.cpp"),

    dict(iface=True,
         file="base/i_config.hpp",
         title="IConfig —— 配置服务契约（SS-8）",
         ref="6.4.8；双形态同源（SA-09）只靠配置项区分",
         includes=[V, "<cstdint>", "<string>"],
         name="IConfig",
         pub=[("DriverKind", "dbDriver()"),
              ("bool", "authEnabled()"),
              ("std::uint64_t", "instrLimit()", "「上限」的唯一取值点（C-02 的收口）"),
              ("std::size_t", "traceCapacity()"),
              ("Duration", "sessionTimeout()"),
              ("std::uint32_t", "cancelCheckInterval()", "取消检查的批次间隔，默认 4096（⑦-1）"),
              ("std::string", "toolchainPath()"),
              ("std::string", "spikePath()"),
              ("std::uint16_t", "port()")]),

    dict(file="base/file_config.hpp",
         title="FileConfig —— 配置服务实现（SS-8，从文件与环境变量读取）",
         ref="6.4.8；SA-09 双形态同源",
         includes=['"base/i_config.hpp"', V, "<string>"],
         name="FileConfig",
         bases=["public IConfig"],
         pub=[("DriverKind", "dbDriver()"),
              ("bool", "authEnabled()"),
              ("std::uint64_t", "instrLimit()"),
              ("std::size_t", "traceCapacity()"),
              ("Duration", "sessionTimeout()"),
              ("std::uint32_t", "cancelCheckInterval()"),
              ("std::string", "toolchainPath()"),
              ("std::string", "spikePath()"),
              ("std::uint16_t", "port()")],
         attrs=[("path_", "std::string", "配置文件路径")],
         impl="base/file_config.cpp"),

    dict(iface=True,
         file="base/i_logger.hpp",
         title="ILogger —— 日志服务契约（SS-8）",
         ref="6.4.8；异常现场（FR-3.5）落这里",
         includes=[V, "<string_view>"],
         name="ILogger",
         pub=[("void", "log(Level lv, std::string_view msg)"),
              ("void", "logAt(Level lv, std::string_view msg, const FaultRecord& f)",
               "带异常现场的日志")]),

    dict(file="base/std_logger.hpp",
         title="StdLogger —— 日志服务实现（SS-8，写标准错误）",
         ref="6.4.8",
         includes=['"base/i_logger.hpp"', V, "<string_view>"],
         name="StdLogger",
         bases=["public ILogger"],
         pub=[("void", "log(Level lv, std::string_view msg)"),
              ("void", "logAt(Level lv, std::string_view msg, const FaultRecord& f)")],
         attrs=[],
         impl="base/std_logger.cpp"),

    dict(iface=True,
         file="base/i_id_gen.hpp",
         title="IIdGen —— 标识生成契约（SS-8）",
         ref="6.4.8；数据设计总则 G-2：业务标识由 IIdGen 生成，不依赖数据库自增",
         includes=[V],
         name="IIdGen",
         pub=[("Token", "newToken()"),
              ("WorkspaceId", "newWorkspaceId()"),
              ("DivergenceId", "newDivergenceId()"),
              ("JobId", "newJobId()")]),

    dict(file="base/uuid_gen.hpp",
         title="UuidGen —— 标识生成实现（SS-8）",
         ref="6.4.8",
         includes=['"base/i_id_gen.hpp"', V],
         name="UuidGen",
         bases=["public IIdGen"],
         pub=[("Token", "newToken()"),
              ("WorkspaceId", "newWorkspaceId()"),
              ("DivergenceId", "newDivergenceId()"),
              ("JobId", "newJobId()")],
         attrs=[],
         impl="base/uuid_gen.cpp"),

    dict(iface=True,
         file="base/i_process_runner.hpp",
         title="IProcessRunner —— 外部进程调用契约（SS-8）",
         ref="6.4.8；SA-06：外部工具与参考模拟器一律经子进程隔离",
         includes=[V, "<string>"],
         name="IProcessRunner",
         pub=[("Result<RunOutcome>", "run(const RunSpec& spec, const CancelToken& tk)", "即起即收"),
              ("bool", "available(const std::string& path)", "路径可用性探测")]),

    dict(file="base/proc_runner.hpp",
         title="ProcRunner —— 外部进程调用实现（SS-8）",
         ref="6.4.8",
         includes=['"base/i_process_runner.hpp"', V, "<string>"],
         name="ProcRunner",
         bases=["public IProcessRunner"],
         pub=[("Result<RunOutcome>", "run(const RunSpec& spec, const CancelToken& tk)"),
              ("bool", "available(const std::string& path)")],
         attrs=[],
         impl="base/proc_runner.cpp"),
]

# ================================================================== 主程序

MAIN_CPP = r'''/**
 * isa-sim 主程序 —— 骨架空壳
 *
 * 设计依据：《软件详细设计文档》6.4.6（Bootstrapper 为组合根）
 * 装配顺序：读配置 → Bootstrapper::build → 启动网关。
 * 骨架阶段只做装配链路占位，返回 0。
 */

#include "api/bootstrapper.hpp"
#include "base/file_config.hpp"
#include "base/i_config.hpp"

int main(int argc, char** argv) {
    (void)argc;
    (void)argv;

    // TODO: FileConfig 从路径读配置 → Bootstrapper::build(cfg) → gateway->handle(...)
    return 0;
}'''


def gen_all():
    for f in SS1 + SS2 + SS3 + SS4 + SS5 + SS6 + SS8:
        gen(f)
    gen(DOMAIN_TYPES)
    for fn, name, title, uc, methods in SS5_IFACE:
        gen(dict(iface=True,
                 file="domain/" + fn,
                 title="%s —— %s" % (name, title),
                 ref="6.4.2；" + uc,
                 includes=_IFACE_INC,
                 name=name,
                 pub=methods))
    emit("src/main.cpp", MAIN_CPP)
