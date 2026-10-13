#pragma once

/**
 * 领域数据对象（SS-5 的值对象）
 *
 * 设计依据：6.4.5「数据对象的方法」；类设计 6.2 值类型清单
 * 置于公共头而非 SS-5 目录：Program 被 SS-4 的 IRefSim 与 SS-3 的 DiffRequest 引用，
 * 若放 src/domain/ 会造成头文件层的反向依赖。
 * 注：这些是值对象（6.2 有权威清单），与「设计类」是两个口径（评审 ①-3 / ⑥-3）。
 */

#include "isa/values.hpp"
#include "isa/compare_types.hpp"
#include <optional>
#include <string>
#include <vector>

namespace isa {

// Program —— 已装载的程序（组合进 Workspace，可由选择性保存单独缺席）
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
};

}  // namespace isa
