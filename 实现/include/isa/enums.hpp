#pragma once

/**
 * 共享枚举（19 个：E-01 ~ E-19）
 *
 * 设计依据：《软件详细设计文档》6.5.1
 * （末尾 4 个为骨架补充：设计正文引用但未列入 E-xx 清单）
 */

namespace isa {

// E-01 内核运行状态（状态图②）
enum class RunState {
    NotReady,
    Ready,
    Running,
    Paused,
    Halted,
    Faulted,
};

// E-02 运行模式；FR-4.3 的全部语义（D-1）
enum class RunMode {
    Step,
    RunN,
    UntilAddr,
    ToBoundary,
    Continue,
};

// E-03 运行结束原因（RunResult.reason）
enum class RunReason {
    HitLimit,
    Cancelled,
    Halted,
    Faulted,
    ModeSatisfied,
    NotReady,
};

// E-04 终止判定结果
enum class GuardVerdict {
    None,
    Halt,
    Fault,
};

// E-05 异常种类（FR-3.5）
enum class FaultKind {
    IllegalInstruction,
    MemAccessViolation,
    MisalignedAccess,
    UnknownCsr,
};

// E-06 比对字段（位掩码，FR-7.2）
enum class Field {
    Pc,
    Gpr,
    Mem,
    Csr,
};

inline Field operator|(Field a, Field b) {
    return static_cast<Field>(static_cast<std::uint32_t>(a) | static_cast<std::uint32_t>(b));
}
inline Field operator&(Field a, Field b) {
    return static_cast<Field>(static_cast<std::uint32_t>(a) & static_cast<std::uint32_t>(b));
}
inline bool has(Field set, Field f) {
    return (static_cast<std::uint32_t>(set) & static_cast<std::uint32_t>(f)) != 0;
}

// E-07 比对模式（FR-6.5）
enum class DiffMode {
    Stepwise,
    Final,
};

// E-08 归因类别（FR-7.4）
enum class AttributionCategory {
    ImplDefect,
    BaselineDeviation,
    SpecAmbiguity,
};

// E-09 断点操作（UC-05 + C-03）
enum class BpOp {
    Add,
    Remove,
    Toggle,
    Enable,
    Disable,
    Clear,
    EnableAll,
    DisableAll,
};

// E-10 选择性保存位掩码（UC-12）
enum class SaveSelection {
    Program,
    Suite,
    Config,
};

inline SaveSelection operator|(SaveSelection a, SaveSelection b) {
    return static_cast<SaveSelection>(static_cast<std::uint32_t>(a) | static_cast<std::uint32_t>(b));
}
inline SaveSelection operator&(SaveSelection a, SaveSelection b) {
    return static_cast<SaveSelection>(static_cast<std::uint32_t>(a) & static_cast<std::uint32_t>(b));
}
inline bool has(SaveSelection set, SaveSelection f) {
    return (static_cast<std::uint32_t>(set) & static_cast<std::uint32_t>(f)) != 0;
}

// E-11 配额检查的操作分类
enum class OpKind {
    Load,
    Step,
    Run,
    Test,
    Diff,
    Workspace,
    User,
};

// E-12 日志级别
enum class Level {
    Debug,
    Info,
    Warn,
    Error,
};

// E-13 数据库驱动（FR-9.2 双形态）
enum class DriverKind {
    Postgres,
    Sqlite,
};

// E-14 对拍任务状态（状态图③）
enum class JobState {
    Queued,
    Running,
    Cancelled,
    Completed,
    Finalized,
};

// E-15 界面标识；取值与 uid 阶段的 UI-01 ~ UI-12 一一对应
enum class UiId {
    ui01,
    ui02,
    ui03,
    ui04,
    ui05,
    ui06,
    ui07,
    ui08,
    ui09,
    ui10,
    ui11,
    ui12,
};

// E-16 统一提示类型（C-18）
enum class ToastKind {
    Success,
    Warn,
    Error,
    Info,
};

// E-17 校验问题级别（Issue.severity）
enum class Severity {
    Error,
    Warn,
    Info,
};

// E-18 角色（DD-1 新增；原 E-01 ~ E-17 缺此项而 User 已引用）
enum class Role {
    User,
    Admin,
};

// E-19 账号状态（DD-1 新增）
enum class UserStatus {
    Active,
    Disabled,
};

// WriteOp.kind 的取值（骨架补充）
enum class WriteKind {
    Gpr,
    Mem,
    Csr,
    Pc,
};

// 内核侧操作类别（Instruction.opClass；骨架补充）
enum class OpClass {
    Nop,
    Lui,
    Auipc,
    Jal,
    Jalr,
    Branch,
    Load,
    Store,
    AluImm,
    Alu,
    Fence,
    System,
    Csr,
    Halt,
    Unknown,
};

// 架构状态读取范围：是否含内存快照（骨架补充）
enum class ReadScope {
    Regs,
    RegsAndMem,
};

// SourceRef 的来源种类（骨架补充）
enum class SourceKind {
    Path,
    Inline,
};

}  // namespace isa
