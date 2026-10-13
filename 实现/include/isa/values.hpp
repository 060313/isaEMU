#pragma once

/**
 * 共享值类型（内核/ISA、对拍、适配、集成四组）
 *
 * 设计依据：《软件详细设计文档》6.5.2 (B)(C)(E)(F) 组 + (D) 组纯值部分
 * 领域数据对象（Program/Workspace/TestSuite/TestCase/TestReport/CaseResult）
 * 与依赖它们的行类型在 domain_types.hpp
 */

#include "aliases.hpp"
#include "enums.hpp"
#include "span.hpp"
#include "result.hpp"
#include "fwd.hpp"
#include <array>
#include <atomic>
#include <cstdint>
#include <map>
#include <memory>
#include <optional>
#include <string>
#include <utility>
#include <vector>

namespace isa {

// 差分记录的最小单元；apply / Trace / CompareEngine 共用（SA-13）
struct WriteOp {
    WriteKind kind;  // Gpr / Mem / Csr / Pc
    std::uint32_t index;  // 寄存器号 / 地址 / CSR 号
    Word oldValue;  // 旧值（回退依据）
    Word newValue;  // 新值
    std::uint8_t len;  // 字节长度（内存写用）

    bool operator==(const WriteOp& o) const { return kind == o.kind && index == o.index && oldValue == o.oldValue && newValue == o.newValue && len == o.len; }
};

// 一份记录三种用途：FR-3.3 / FR-4.4 / FR-7.2
struct StepRecord {
    StepNo stepNo;
    Addr pc;
    Enc enc;
    span<const WriteOp> writes;
    std::optional<FaultKind> faultKind;
};

// 译码结果（SA-01 的语义模板）
struct Instruction {
    OpClass opClass;
    RegIdx rd;
    RegIdx rs1;
    RegIdx rs2;
    std::int32_t imm;
    std::uint8_t width;
};

// ISA 描述的寄存器定义（骨架补充的具体化）
struct RegisterDef {
    std::string name;
    RegIdx index;
    std::uint8_t width;
};

// ISA 描述的指令定义（骨架补充的具体化）
struct InstrDef {
    std::string mnemonic;
    OpClass opClass;
    std::string rdField;
    std::string rs1Field;
    std::string rs2Field;
};

// ISA 描述的编码域定义（骨架补充的具体化）
struct EncodingDef {
    Enc pattern;
    Enc mask;
    OpClass opClass;
};

// ISA 描述的内存表示（不落库，7.1.3）
struct IsaSpec {
    SpecId specId;
    std::string name;
    std::vector<RegisterDef> registers;
    std::vector<InstrDef> instructions;
    std::vector<EncodingDef> encodings;
};

// 程序映像（含字节）
struct Image {
    Bytes bytes;
    Addr lo_;  // 映像区间下界
    Addr hi_;  // 映像区间上界
    Addr entryPc;
    Addr stackPtr;
};

// 内核持有的映像摘要：只有区间与入口，不含字节
struct ImageDesc {
    Addr lo_;
    Addr hi_;
    Addr entryPc;
    Addr stackPtr;
};

// 装载初值
struct InitState {
    Addr sp;
    std::vector<std::pair<Addr, Bytes>> memInit;  // C-08 的数据来源
};

// 内存只读视图；ReadScope 不含内存时为 nullopt（骨架补充）
struct MemView {
    const std::uint8_t* data;
    std::size_t size;

    bool operator==(const MemView& o) const { return data == o.data && size == o.size; }
};

// 架构状态快照（可比较）
struct StateSnapshot {
    Addr pc;
    std::array<Word, 32> gpr;
    span<const std::pair<CsrId, Word>> csr;
    std::optional<MemView> mem;  // 可选：避免大拷贝

    bool operator==(const StateSnapshot& o) const { return pc == o.pc && gpr == o.gpr && csr == o.csr && mem == o.mem; }
};

// 回推进界面的增量（SA-11）
struct StepDelta {
    StepNo stepNo;
    Addr pc;
    span<const WriteOp> writes;
    RunReason reason;
};

// 异常现场（FR-3.5 落盘）
struct FaultRecord {
    FaultKind kind;
    StepNo stepNo;
    Addr pc;
    Enc enc;
    span<const WriteOp> writes;
    std::array<Word, 32> regs;
};

// run 的返回值
struct RunResult {
    StepDelta delta;
    RunReason reason;
    std::uint64_t steps;
};

// 单个字段的差异（可比较）
struct FieldDiff {
    Field field;
    std::uint32_t index;
    Word valueA;
    Word valueB;

    bool operator==(const FieldDiff& o) const { return field == o.field && index == o.index && valueA == o.valueA && valueB == o.valueB; }
};

// 归因标注
struct Attribution {
    AttributionCategory category;
    std::string note;
    UserId by;
    Timestamp at;
};

// 分歧记录的持久化行（T-11）
struct DivergenceRow {
    DivergenceId divId;
    JobId jobId;
    StepNo stepNo;
    Addr pc;
    std::vector<FieldDiff> fieldDiffs;
    std::optional<Attribution> attribution;
    std::string note;
    UserId owner;
};

// 联合类型：finalAssert 或 sequence 二选一，由 mode() 报告哪一种
struct ExpectedSpec {
    std::optional<StateSnapshot> finalAssert;  // 终态断言
    std::vector<StepRecord> sequence;  // 逐条期望序列
};

// 用例复现快照（UC-09）
struct CaseSnapshot {
    CaseId caseId;
    StateSnapshot snapshot;
    std::optional<StepNo> firstDiffAt;
    std::vector<FieldDiff> diffFields;
};

// 源码来源：路径或内联文本
struct SourceRef {
    SourceKind kind;
    std::string pathOrInline;
};

// 校验问题（IsaLoader / ToolchainAdapter 共用）
struct Issue {
    int line;
    int col;
    Severity severity;
    std::string code;
    std::string message;
};

// 外部工具链描述
struct ToolchainSpec {
    std::string path;
    std::vector<std::string> args;
};

// 子进程启动描述
struct RunSpec {
    std::string cmd;
    std::vector<std::string> args;
    std::string stdinText;  // 避开 <cstdio> 的 stdin 宏
    Duration timeout;
};

// 子进程结果
struct RunOutcome {
    int exitCode;
    std::string outText;  // 避开 stdout 宏
    std::string errText;  // 避开 stderr 宏
    bool timedOut;
};

// 装载请求
struct LoadSpec {
    SourceRef source;
    Addr base;
    Addr entryPc;
    Addr stackPtr;
    std::vector<std::pair<Addr, Bytes>> initMem;
};

// 反汇编文本行
struct Disasm {
    std::vector<std::string> lines;
};

// 指向工作区内程序的引用
struct ProgramRef {
    WorkspaceId workspaceId;
    Hash hash;
};

// 单次运行的报告
struct RunReport {
    StateSnapshot snapshot;
    RunReason reason;
    std::vector<WriteOp> writes;
};

// 登录凭据（明文仅在传输中）
struct Credential {
    std::string username;
    std::string secret;
};

// 口令验证材料（T-02）；凭据与身份分表（DD-1 / M-02）
struct CredentialRow {
    UserId uid;
    std::string secretHash;
    std::string salt;
    std::string kdf;  // 算法标识；换算法只需新行写新值（DD-1）
    int iterations;
};

// 配额（骨架补充：users 表的 q_* 四列）
struct Quota {
    int sessions;  // 并发会话数上限
    int requests;  // 单位时间请求数上限
    std::uint64_t instr;  // 单次请求指令条数上限（NFR-Q5）
    std::uint64_t bytes;  // 工作区存储上限（64 MiB）
};

// 用户身份（不含验证材料）
struct User {
    UserId uid;
    std::string name;
    Role role;
    Quota quota;
    UserStatus status;
};

// UC-14 的部分更新
struct UserPatch {
    std::optional<Quota> quota;
    std::optional<UserStatus> status;
};

// 窗口用量
struct Usage {
    int sessions;  // 派生：COUNT(sessions)，不落列（DD-4）
    int requests;
    std::uint64_t instr;
    std::uint64_t bytes;  // 派生：SUM(size_bytes)，不落列（DD-4）
};

// 登录结果
struct LoginResult {
    Token token;
    WorkspaceId workspace;
    SpecId isa;
};

// 会话审计行（T-04）
struct SessionRow {
    Token token;
    UserId uid;
    WorkspaceId wsId;
    SpecId isaId;
    Timestamp createdAt;
    Timestamp lastSeen;
    Timestamp expiresAt;  // 新增（DD-4）：last_seen + sessionTimeout，写行时算好
    std::optional<Timestamp> endedAt;  // 新增（DD-4）：dropSession 写入
};

// 会话/工作区配置（workspaces.config_blob）
struct SessionConfig {
    Addr sp;
    std::vector<std::pair<Addr, Bytes>> initMem;
    std::uint64_t instrLimit;
    bool traceOn;
};

// 工作区列表项（UI-09）
struct WorkspaceBrief {
    WorkspaceId wsId;
    std::string name;  // 新增（DD-7）
    Version version;
    Timestamp updatedAt;
};

// 工作区持久化行（T-05）
struct WorkspaceRow {
    WorkspaceId wsId;
    UserId owner;
    Version version;
    std::string programBlob;
    std::string suiteBlob;  // 已弃用（DD-2）：用例集落子表，此列不再使用
    std::string configBlob;
};

// 断点项
struct Breakpoint {
    Addr addr;
    BpOp op;
    bool enabled;
};

// 断点表行（T-10）
struct BreakpointRow {
    UserId owner;  // 隔离谓词列
    WorkspaceId wsId;  // 新增（DD-6）：必须进主键，否则会话间互相覆盖
    std::vector<Breakpoint> items;
};

// HTTP 入站请求
struct HttpRequest {
    std::string method;
    std::string path;
    std::vector<std::pair<std::string, std::string>> headers;
    std::string body;
    std::optional<Credential> cred;
};

// HTTP 出站响应
struct HttpResponse {
    int status;
    std::vector<std::pair<std::string, std::string>> headers;
    std::string body;
};

// 路由键
struct RouteKey {
    std::string method;
    std::string pathPattern;
};

// 鉴权后的调用者身份
struct Caller {
    UserId userId;
    Role role;
    bool authEnabled;
};

// 参数表
struct Params {
    std::map<std::string, std::string> items;
};

// 骨架：以 JSON 文本承载 variant 的序列化结果
struct Payload {
    std::string json;
};

// 骨架：字段名列表（实现时替换为逐字段类型描述）
struct Schema {
    std::vector<std::string> fields;
};

// 已绑定的参数
struct Bound {
    Params params;
};

// WebSocket 事件（FR-6.4）
struct Event {
    std::string kind;
    Payload payload;
};

// WebSocket 会话句柄
struct WsSession {
    std::uint64_t id;
};

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

}  // namespace isa
