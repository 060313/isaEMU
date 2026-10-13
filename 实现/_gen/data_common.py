# -*- coding: utf-8 -*-
"""共享类型层：span / Result / 别名 / 枚举 / 值类型 / 领域数据对象。"""
from render import emit, hpp, st, en

# ---------------------------------------------------------------- 手写头

SPAN_HPP = r'''#pragma once

/**
 * isa::span —— 最小非拥有只读/可写视图
 *
 * 设计依据：《软件详细设计文档》6.4「参数传递」——大值类型用 span<const T> 传只读视图
 * 说明：设计的构建约束是 C++17（SAD 5.1.4），C++17 无 std::span；为守住「内核层零第三方
 *       链接」，此处提供最小实现，而不是引入 GSL。
 */

#include <cstddef>
#include <type_traits>
#include <vector>

namespace isa {

template <class T>
class span {
public:
    span() = default;
    span(T* p, std::size_t n) : p_(p), n_(n) {}
    span(T* b, T* e) : p_(b), n_(static_cast<std::size_t>(e - b)) {}

    template <class U, class = std::enable_if_t<std::is_convertible<U*, T*>::value>>
    span(const std::vector<U>& v) : p_(v.data()), n_(v.size()) {}  // NOLINT

    template <std::size_t N, class = std::enable_if_t<std::is_convertible<T (*)[N], T*>::value>>
    span(T (&a)[N]) : p_(a), n_(N) {}  // NOLINT

    T* data() const { return p_; }
    std::size_t size() const { return n_; }
    bool empty() const { return n_ == 0; }
    T& operator[](std::size_t i) const { return p_[i]; }
    T* begin() const { return p_; }
    T* end() const { return p_ + n_; }

private:
    T* p_{nullptr};
    std::size_t n_{0};
};

template <class T>
bool operator==(span<T> a, span<T> b) {
    if (a.size() != b.size()) return false;
    for (std::size_t i = 0; i < a.size(); ++i)
        if (!(a[i] == b[i])) return false;
    return true;
}

template <class T>
bool operator!=(span<T> a, span<T> b) { return !(a == b); }

}  // namespace isa
'''

RESULT_HPP = r'''#pragma once

/**
 * isa::Result<T> / isa::Err —— 统一的可预期失败表达
 *
 * 设计依据：《软件详细设计文档》6.4「返回」规则 + 类设计总则 G-6
 *   「可预期失败一律 Result<T>；可能无结果用 optional<T>；方法不抛异常」
 */

#include <optional>
#include <string>
#include <utility>
#include <variant>

namespace isa {

enum class ErrCode {
    Unauthorized,     // 登录失败：NoSuchUser / BadPassword / Disabled
    NotFound,
    Invalid,
    Conflict,         // 同名工作区冲突等
    Disabled,
    TooOld,           // 轨迹已被裁剪，不可回退
    AddrOutOfRange,
    TraceDisabled,
    Internal,
    NotImplemented,   // 骨架占位；实现完成后应彻底消失
};

struct Err {
    ErrCode code{ErrCode::Internal};
    std::string message;
};

template <class T>
class Result {
public:
    Result(T v) : v_(std::move(v)) {}    // NOLINT: 允许直接 return 值
    Result(Err e) : v_(std::move(e)) {}  // NOLINT: 允许直接 return 错误

    static Result ok(T v) { return Result(std::move(v)); }
    static Result err(Err e) { return Result(std::move(e)); }
    static Result err(ErrCode c, std::string m = {}) { return Result(Err{c, std::move(m)}); }

    bool isOk() const { return v_.index() == 0; }
    bool isErr() const { return v_.index() == 1; }

    const T& value() const { return std::get<0>(v_); }
    T& value() { return std::get<0>(v_); }
    const Err& error() const { return std::get<1>(v_); }

private:
    std::variant<T, Err> v_;
};

// 引用返回的特化：std::variant 不允许引用备选，故以指针承载
template <class T>
class Result<T&> {
public:
    Result(T& v) : p_(&v) {}             // NOLINT
    Result(Err e) : e_(std::move(e)) {}  // NOLINT

    static Result ok(T& v) { return Result(v); }
    static Result err(Err e) { return Result(std::move(e)); }
    static Result err(ErrCode c, std::string m = {}) { return Result(Err{c, std::move(m)}); }

    bool isOk() const { return p_ != nullptr; }
    bool isErr() const { return p_ == nullptr; }

    T& value() const { return *p_; }
    const Err& error() const { return e_; }

private:
    T* p_{nullptr};
    Err e_{};
};

template <>
class Result<void> {
public:
    Result() = default;
    Result(Err e) : e_(std::move(e)) {}  // NOLINT

    static Result ok() { return Result(); }
    static Result err(Err e) { return Result(std::move(e)); }
    static Result err(ErrCode c, std::string m = {}) { return Result(Err{c, std::move(m)}); }

    bool isOk() const { return !e_.has_value(); }
    bool isErr() const { return e_.has_value(); }
    const Err& error() const { return *e_; }

private:
    std::optional<Err> e_;
};

}  // namespace isa
'''

# ---------------------------------------------------------------- 前向声明

FWD_HPP = r'''#pragma once

/**
 * 前向声明 —— 跨子系统引用（指针 / 引用成员与参数）的公共入口
 *
 * 设计依据：《软件详细设计文档》6.2.4「跨子系统的关联全部指向接口」
 * 说明：各构件的头文件只把「能力」声明为指针 / 引用，故前向声明足够；
 *       完整类型只在 .cpp 里引入。这使「仅相邻层依赖」（sad P5）在头文件层也成立。
 */

namespace isa {

// 契约接口
class ICoreService;
class IDecodeTable;
class IIsaProvider;
class ICompareService;
class IAssembler;
class IRefSim;
class ISessionService;
class IIsaService;
class ILoadService;
class IDebugService;
class ITestService;
class IDiffService;
class IWorkspaceService;
class IStore;
class IConfig;
class ILogger;
class IIdGen;
class IProcessRunner;

// SS-1 / SS-2 / SS-3 / SS-4
class ArchState;
class Trace;
class TerminationGuard;
class EmulatorCore;
class IsaLoader;
class DecodeTable;
class CompareEngine;
class DiffScope;
class Divergence;
class ToolchainAdapter;
class RefSimAdapter;

// SS-5 / SS-6 / SS-8
class SessionContext;
class BreakpointTable;
class SessionService;
class IsaService;
class LoadService;
class DebugService;
class TestService;
class DiffService;
class WorkspaceService;
class HttpGateway;
class Router;
class AccessGuard;
class Bootstrapper;
class DbDriver;
class DbStore;
class FileConfig;
class StdLogger;
class UuidGen;
class ProcRunner;

}  // namespace isa
'''

# ---------------------------------------------------------------- 别名（A 组 20 个）

ALIASES = [
    ("Addr", "std::uint64_t", "地址；32 位 ISA 只用低 32 位"),
    ("Word", "std::uint32_t", "机器字"),
    ("Enc", "std::uint32_t", "指令编码"),
    ("RegIdx", "std::uint8_t", "寄存器序号"),
    ("StepNo", "std::uint64_t", "指令步序号"),
    ("UserId", "std::uint64_t", "用户标识"),
    ("Token", "std::string", "会话令牌（32 字节随机数的 base64url 编码，43 字符）"),
    ("WorkspaceId", "std::uint64_t", "工作区标识"),
    ("SpecId", "std::string", "ISA 描述标识"),
    ("SuiteId", "std::uint64_t", "用例集标识"),
    ("CaseId", "std::uint64_t", "用例标识"),
    ("ReportId", "std::uint64_t", "报告标识"),
    ("DivergenceId", "std::uint64_t", "分歧记录标识"),
    ("JobId", "std::string", "任务标识"),
    ("ExampleId", "std::string", "内置示例标识"),
    ("Pid", "std::int64_t", "进程标识"),
    ("Hash", "std::string", "内容摘要（十六进制）"),
    ("Version", "std::uint32_t", "乐观并发版本号"),
    ("Timestamp", "std::chrono::system_clock::time_point", "绝对时刻"),
    ("Duration", "std::chrono::seconds", "时间跨度"),
    # 以下 6 个为骨架补充（设计文档未列入别名清单，但正文引用了它们）
    ("Bytes", "std::vector<std::uint8_t>", "字节序列（骨架补充）"),
    ("Clock", "std::chrono::system_clock", "时钟（骨架补充）"),
    ("CsrId", "std::uint16_t", "CSR 序号（骨架补充）"),
    ("PageNo", "std::uint32_t", "稀疏内存页号（骨架补充）"),
    ("FieldMask", "std::uint32_t", "比对字段位掩码（骨架补充）"),
    ("BitMask", "std::uint64_t", "编码宽度位图（骨架补充）"),
]

# ---------------------------------------------------------------- 枚举（E-01 ~ E-19）

ENUMS = [
    ("RunState", ["NotReady", "Ready", "Running", "Paused", "Halted", "Faulted"],
     "E-01 内核运行状态（状态图②）", ""),
    ("RunMode", ["Step", "RunN", "UntilAddr", "ToBoundary", "Continue"],
     "E-02 运行模式；FR-4.3 的全部语义（D-1）", ""),
    ("RunReason", ["HitLimit", "Cancelled", "Halted", "Faulted", "ModeSatisfied", "NotReady"],
     "E-03 运行结束原因（RunResult.reason）", ""),
    ("GuardVerdict", ["None", "Halt", "Fault"],
     "E-04 终止判定结果", ""),
    ("FaultKind", ["IllegalInstruction", "MemAccessViolation", "MisalignedAccess", "UnknownCsr"],
     "E-05 异常种类（FR-3.5）", ""),
    ("Field", ["Pc", "Gpr", "Mem", "Csr"],
     "E-06 比对字段（位掩码，FR-7.2）", "std::uint32_t"),
    ("DiffMode", ["Stepwise", "Final"],
     "E-07 比对模式（FR-6.5）", ""),
    ("AttributionCategory", ["ImplDefect", "BaselineDeviation", "SpecAmbiguity"],
     "E-08 归因类别（FR-7.4）", ""),
    ("BpOp", ["Add", "Remove", "Toggle", "Enable", "Disable", "Clear", "EnableAll", "DisableAll"],
     "E-09 断点操作（UC-05 + C-03）", ""),
    ("SaveSelection", ["Program", "Suite", "Config"],
     "E-10 选择性保存位掩码（UC-12）", "std::uint32_t"),
    ("OpKind", ["Load", "Step", "Run", "Test", "Diff", "Workspace", "User"],
     "E-11 配额检查的操作分类", ""),
    ("Level", ["Debug", "Info", "Warn", "Error"],
     "E-12 日志级别", ""),
    ("DriverKind", ["Postgres", "Sqlite"],
     "E-13 数据库驱动（FR-9.2 双形态）", ""),
    ("JobState", ["Queued", "Running", "Cancelled", "Completed", "Finalized"],
     "E-14 对拍任务状态（状态图③）", ""),
    ("UiId", ["ui01", "ui02", "ui03", "ui04", "ui05", "ui06",
              "ui07", "ui08", "ui09", "ui10", "ui11", "ui12"],
     "E-15 界面标识；取值与 uid 阶段的 UI-01 ~ UI-12 一一对应", ""),
    ("ToastKind", ["Success", "Warn", "Error", "Info"],
     "E-16 统一提示类型（C-18）", ""),
    ("Severity", ["Error", "Warn", "Info"],
     "E-17 校验问题级别（Issue.severity）", ""),
    ("Role", ["User", "Admin"],
     "E-18 角色（DD-1 新增；原 E-01 ~ E-17 缺此项而 User 已引用）", ""),
    ("UserStatus", ["Active", "Disabled"],
     "E-19 账号状态（DD-1 新增）", ""),
    # 以下为骨架补充：设计正文引用但未列入 E-xx 清单的内核/领域内部枚举
    ("WriteKind", ["Gpr", "Mem", "Csr", "Pc"],
     "WriteOp.kind 的取值（骨架补充）", ""),
    ("OpClass", ["Nop", "Lui", "Auipc", "Jal", "Jalr", "Branch", "Load", "Store",
                 "AluImm", "Alu", "Fence", "System", "Csr", "Halt", "Unknown"],
     "内核侧操作类别（Instruction.opClass；骨架补充）", ""),
    ("ReadScope", ["Regs", "RegsAndMem"],
     "架构状态读取范围：是否含内存快照（骨架补充）", ""),
    ("SourceKind", ["Path", "Inline"],
     "SourceRef 的来源种类（骨架补充）", ""),
]

# ---------------------------------------------------------------- 值类型（B/C/E/F 组 + D 组纯值）

VALUES = [
    # (B) 内核与 ISA
    ("WriteOp", [
        ("kind", "WriteKind", "Gpr / Mem / Csr / Pc"),
        ("index", "std::uint32_t", "寄存器号 / 地址 / CSR 号"),
        ("oldValue", "Word", "旧值（回退依据）"),
        ("newValue", "Word", "新值"),
        ("len", "std::uint8_t", "字节长度（内存写用）"),
    ], "差分记录的最小单元；apply / Trace / CompareEngine 共用（SA-13）", True),

    ("StepRecord", [
        ("stepNo", "StepNo"),
        ("pc", "Addr"),
        ("enc", "Enc"),
        ("writes", "span<const WriteOp>"),
        ("faultKind", "std::optional<FaultKind>"),
    ], "一份记录三种用途：FR-3.3 / FR-4.4 / FR-7.2", False),

    ("Instruction", [
        ("opClass", "OpClass"),
        ("rd", "RegIdx"),
        ("rs1", "RegIdx"),
        ("rs2", "RegIdx"),
        ("imm", "std::int32_t"),
        ("width", "std::uint8_t"),
    ], "译码结果（SA-01 的语义模板）", False),

    ("RegisterDef", [("name", "std::string"), ("index", "RegIdx"), ("width", "std::uint8_t")],
     "ISA 描述的寄存器定义（骨架补充的具体化）", False),
    ("InstrDef", [("mnemonic", "std::string"), ("opClass", "OpClass"),
                  ("rdField", "std::string"), ("rs1Field", "std::string"), ("rs2Field", "std::string")],
     "ISA 描述的指令定义（骨架补充的具体化）", False),
    ("EncodingDef", [("pattern", "Enc"), ("mask", "Enc"), ("opClass", "OpClass")],
     "ISA 描述的编码域定义（骨架补充的具体化）", False),

    ("IsaSpec", [
        ("specId", "SpecId"),
        ("name", "std::string"),
        ("registers", "std::vector<RegisterDef>"),
        ("instructions", "std::vector<InstrDef>"),
        ("encodings", "std::vector<EncodingDef>"),
    ], "ISA 描述的内存表示（不落库，7.1.3）", False),

    ("Image", [
        ("bytes", "Bytes"),
        ("lo_", "Addr", "映像区间下界"),
        ("hi_", "Addr", "映像区间上界"),
        ("entryPc", "Addr"),
        ("stackPtr", "Addr"),
    ], "程序映像（含字节）", False),

    ("ImageDesc", [
        ("lo_", "Addr"),
        ("hi_", "Addr"),
        ("entryPc", "Addr"),
        ("stackPtr", "Addr"),
    ], "内核持有的映像摘要：只有区间与入口，不含字节", False),

    ("InitState", [
        ("sp", "Addr"),
        ("memInit", "std::vector<std::pair<Addr, Bytes>>", "C-08 的数据来源"),
    ], "装载初值", False),

    ("MemView", [
        ("data", "const std::uint8_t*"),
        ("size", "std::size_t"),
    ], "内存只读视图；ReadScope 不含内存时为 nullopt（骨架补充）", True),

    ("StateSnapshot", [
        ("pc", "Addr"),
        ("gpr", "std::array<Word, 32>"),
        ("csr", "span<const std::pair<CsrId, Word>>"),
        ("mem", "std::optional<MemView>", "可选：避免大拷贝"),
    ], "架构状态快照（可比较）", True),

    ("StepDelta", [
        ("stepNo", "StepNo"),
        ("pc", "Addr"),
        ("writes", "span<const WriteOp>"),
        ("reason", "RunReason"),
    ], "回推进界面的增量（SA-11）", False),

    ("FaultRecord", [
        ("kind", "FaultKind"),
        ("stepNo", "StepNo"),
        ("pc", "Addr"),
        ("enc", "Enc"),
        ("writes", "span<const WriteOp>"),
        ("regs", "std::array<Word, 32>"),
    ], "异常现场（FR-3.5 落盘）", False),

    ("RunResult", [
        ("delta", "StepDelta"),
        ("reason", "RunReason"),
        ("steps", "std::uint64_t"),
    ], "run 的返回值", False),

    # (C) 对拍与比对
    ("FieldDiff", [
        ("field", "Field"),
        ("index", "std::uint32_t"),
        ("valueA", "Word"),
        ("valueB", "Word"),
    ], "单个字段的差异（可比较）", True),

    ("Attribution", [
        ("category", "AttributionCategory"),
        ("note", "std::string"),
        ("by", "UserId"),
        ("at", "Timestamp"),
    ], "归因标注", False),

    ("DivergenceRow", [
        ("divId", "DivergenceId"),
        ("jobId", "JobId"),
        ("stepNo", "StepNo"),
        ("pc", "Addr"),
        ("fieldDiffs", "std::vector<FieldDiff>"),
        ("attribution", "std::optional<Attribution>"),
        ("note", "std::string"),
        ("owner", "UserId"),
    ], "分歧记录的持久化行（T-11）", False),

    ("ExpectedSpec", [
        ("finalAssert", "std::optional<StateSnapshot>", "终态断言"),
        ("sequence", "std::vector<StepRecord>", "逐条期望序列"),
    ], "联合类型：finalAssert 或 sequence 二选一，由 mode() 报告哪一种", False),

    ("CaseSnapshot", [
        ("caseId", "CaseId"),
        ("snapshot", "StateSnapshot"),
        ("firstDiffAt", "std::optional<StepNo>"),
        ("diffFields", "std::vector<FieldDiff>"),
    ], "用例复现快照（UC-09）", False),

    # (E) 适配与服务契约
    ("SourceRef", [
        ("kind", "SourceKind"),
        ("pathOrInline", "std::string"),
    ], "源码来源：路径或内联文本", False),

    ("Issue", [
        ("line", "int"),
        ("col", "int"),
        ("severity", "Severity"),
        ("code", "std::string"),
        ("message", "std::string"),
    ], "校验问题（IsaLoader / ToolchainAdapter 共用）", False),

    ("ToolchainSpec", [("path", "std::string"), ("args", "std::vector<std::string>")],
     "外部工具链描述", False),

    ("RunSpec", [
        ("cmd", "std::string"),
        ("args", "std::vector<std::string>"),
        ("stdinText", "std::string", "避开 <cstdio> 的 stdin 宏"),
        ("timeout", "Duration"),
    ], "子进程启动描述", False),

    ("RunOutcome", [
        ("exitCode", "int"),
        ("outText", "std::string", "避开 stdout 宏"),
        ("errText", "std::string", "避开 stderr 宏"),
        ("timedOut", "bool"),
    ], "子进程结果", False),

    ("LoadSpec", [
        ("source", "SourceRef"),
        ("base", "Addr"),
        ("entryPc", "Addr"),
        ("stackPtr", "Addr"),
        ("initMem", "std::vector<std::pair<Addr, Bytes>>"),
    ], "装载请求", False),

    ("Disasm", [("lines", "std::vector<std::string>")], "反汇编文本行", False),

    ("ProgramRef", [
        ("workspaceId", "WorkspaceId"),
        ("hash", "Hash"),
    ], "指向工作区内程序的引用", False),

    ("RunReport", [
        ("snapshot", "StateSnapshot"),
        ("reason", "RunReason"),
        ("writes", "std::vector<WriteOp>"),
    ], "单次运行的报告", False),

    # (D) 测试、账号与工作区（纯值部分）
    ("Credential", [("username", "std::string"), ("secret", "std::string")],
     "登录凭据（明文仅在传输中）", False),

    ("CredentialRow", [
        ("uid", "UserId"),
        ("secretHash", "std::string"),
        ("salt", "std::string"),
        ("kdf", "std::string", "算法标识；换算法只需新行写新值（DD-1）"),
        ("iterations", "int"),
    ], "口令验证材料（T-02）；凭据与身份分表（DD-1 / M-02）", False),

    ("Quota", [
        ("sessions", "int", "并发会话数上限"),
        ("requests", "int", "单位时间请求数上限"),
        ("instr", "std::uint64_t", "单次请求指令条数上限（NFR-Q5）"),
        ("bytes", "std::uint64_t", "工作区存储上限（64 MiB）"),
    ], "配额（骨架补充：users 表的 q_* 四列）", False),

    ("User", [
        ("uid", "UserId"),
        ("name", "std::string"),
        ("role", "Role"),
        ("quota", "Quota"),
        ("status", "UserStatus"),
    ], "用户身份（不含验证材料）", False),

    ("UserPatch", [
        ("quota", "std::optional<Quota>"),
        ("status", "std::optional<UserStatus>"),
    ], "UC-14 的部分更新", False),

    ("Usage", [
        ("sessions", "int", "派生：COUNT(sessions)，不落列（DD-4）"),
        ("requests", "int"),
        ("instr", "std::uint64_t"),
        ("bytes", "std::uint64_t", "派生：SUM(size_bytes)，不落列（DD-4）"),
    ], "窗口用量", False),

    ("LoginResult", [
        ("token", "Token"),
        ("workspace", "WorkspaceId"),
        ("isa", "SpecId"),
    ], "登录结果", False),

    ("SessionRow", [
        ("token", "Token"),
        ("uid", "UserId"),
        ("wsId", "WorkspaceId"),
        ("isaId", "SpecId"),
        ("createdAt", "Timestamp"),
        ("lastSeen", "Timestamp"),
        ("expiresAt", "Timestamp", "新增（DD-4）：last_seen + sessionTimeout，写行时算好"),
        ("endedAt", "std::optional<Timestamp>", "新增（DD-4）：dropSession 写入"),
    ], "会话审计行（T-04）", False),

    ("SessionConfig", [
        ("sp", "Addr"),
        ("initMem", "std::vector<std::pair<Addr, Bytes>>"),
        ("instrLimit", "std::uint64_t"),
        ("traceOn", "bool"),
    ], "会话/工作区配置（workspaces.config_blob）", False),

    ("WorkspaceBrief", [
        ("wsId", "WorkspaceId"),
        ("name", "std::string", "新增（DD-7）"),
        ("version", "Version"),
        ("updatedAt", "Timestamp"),
    ], "工作区列表项（UI-09）", False),

    ("WorkspaceRow", [
        ("wsId", "WorkspaceId"),
        ("owner", "UserId"),
        ("version", "Version"),
        ("programBlob", "std::string"),
        ("suiteBlob", "std::string", "已弃用（DD-2）：用例集落子表，此列不再使用"),
        ("configBlob", "std::string"),
    ], "工作区持久化行（T-05）", False),

    ("Breakpoint", [
        ("addr", "Addr"),
        ("op", "BpOp"),
        ("enabled", "bool"),
    ], "断点项", False),

    ("BreakpointRow", [
        ("owner", "UserId", "隔离谓词列"),
        ("wsId", "WorkspaceId", "新增（DD-6）：必须进主键，否则会话间互相覆盖"),
        ("items", "std::vector<Breakpoint>"),
    ], "断点表行（T-10）", False),

    # (F) 集成与并发
    ("HttpRequest", [
        ("method", "std::string"),
        ("path", "std::string"),
        ("headers", "std::vector<std::pair<std::string, std::string>>"),
        ("body", "std::string"),
        ("cred", "std::optional<Credential>"),
    ], "HTTP 入站请求", False),

    ("HttpResponse", [
        ("status", "int"),
        ("headers", "std::vector<std::pair<std::string, std::string>>"),
        ("body", "std::string"),
    ], "HTTP 出站响应", False),

    ("RouteKey", [("method", "std::string"), ("pathPattern", "std::string")],
     "路由键", False),

    ("Caller", [
        ("userId", "UserId"),
        ("role", "Role"),
        ("authEnabled", "bool"),
    ], "鉴权后的调用者身份", False),

    ("Params", [("items", "std::map<std::string, std::string>")], "参数表", False),

    ("Payload", [("json", "std::string")],
     "骨架：以 JSON 文本承载 variant 的序列化结果", False),

    ("Schema", [("fields", "std::vector<std::string>")],
     "骨架：字段名列表（实现时替换为逐字段类型描述）", False),

    ("Bound", [("params", "Params")], "已绑定的参数", False),

    ("Event", [("kind", "std::string"), ("payload", "Payload")],
     "WebSocket 事件（FR-6.4）", False),

    ("WsSession", [("id", "std::uint64_t")], "WebSocket 会话句柄", False),

]

# 需要手写的、带方法的值类型（放在 values.hpp 末尾）
VALUES_HAND = r'''
// WsId —— WebSocket 连接标识（骨架补充为具名别名）
using WsId = std::uint64_t;

// CancelToken —— 协作式取消原语（D-4）
//
// 全设计唯一使用共享所有权的地方：多个执行者需看到同一个标志，且标志的生命周期必须
// 长于所有执行者（JobEntry 可能先被清理而内核仍在收尾）。内核每
// IConfig.cancelCheckInterval() 步（默认 4096）读一次；子进程在轮询周期内读一次。
// 工具链升级到 C++20 后可直接换成 std::stop_source，签名不变。
class CancelToken {
public:
    CancelToken() : flag_(std::make_shared<std::atomic<bool>>(false)) {}

    void cancel() const { flag_->store(true, std::memory_order_relaxed); }
    bool isCancelled() const { return flag_->load(std::memory_order_relaxed); }
    void reset() const { flag_->store(false, std::memory_order_relaxed); }

private:
    std::shared_ptr<std::atomic<bool>> flag_;
};

// JobHandle —— 可中断句柄（UC-10「取消对拍」）
struct JobHandle {
    JobId jobId;
    double progress() const { return progress_; }
    void cancel() const { if (token_) token_->cancel(); }

    double progress_{0.0};
    std::shared_ptr<CancelToken> token_;
};

// JobEntry —— 对拍任务条目（不注入持久化，7.1.3）
struct JobEntry {
    JobState state;
    CancelToken token;
    Timestamp startedAt;
    double progress{0.0};
};
'''.strip()


def _alias_block():
    lines = []
    for n, t, c in ALIASES:
        lines.append("using %s = %s;%s" % (n, t, "  // " + c if c else ""))
    return "\n".join(lines)


def _enum_block():
    return "\n\n".join(en(n, v, d, b) for n, v, d, b in ENUMS)


def _value_block():
    out = []
    for name, fields, doc, eq in VALUES:
        out.append(st(name, fields, doc, eq))
    return "\n\n".join(out)


def gen_common():
    emit("include/isa/span.hpp", SPAN_HPP)
    emit("include/isa/result.hpp", RESULT_HPP)
    emit("include/isa/fwd.hpp", FWD_HPP)

    hpp("include/isa/aliases.hpp",
        "共享别名（20 个标识与基础别名）",
        "《软件详细设计文档》6.5.2 (A) 组",
        ["<chrono>", "<cstdint>", "<string>", "<vector>"],
        _alias_block(),
        extra=["（另含 6 个骨架补充别名，见行内标注）"])

    hpp("include/isa/enums.hpp",
        "共享枚举（19 个：E-01 ~ E-19）",
        "《软件详细设计文档》6.5.1",
        [],
        _enum_block(),
        extra=["（末尾 4 个为骨架补充：设计正文引用但未列入 E-xx 清单）"])

    hpp("include/isa/values.hpp",
        "共享值类型（内核/ISA、对拍、适配、集成四组）",
        "《软件详细设计文档》6.5.2 (B)(C)(E)(F) 组 + (D) 组纯值部分",
        ['"aliases.hpp"', '"enums.hpp"', '"span.hpp"', '"result.hpp"', '"fwd.hpp"',
         "<array>", "<atomic>", "<cstdint>", "<map>", "<memory>",
         "<optional>", "<string>", "<utility>", "<vector>"],
        _value_block() + "\n\n" + VALUES_HAND,
        extra=["领域数据对象（Program/Workspace/TestSuite/TestCase/TestReport/CaseResult）",
               "与依赖它们的行类型在 domain_types.hpp"])
