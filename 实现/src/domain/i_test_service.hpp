#pragma once

/**
 * ITestService —— 测试服务契约
 *
 * 设计依据：6.4.2；UC-08 / UC-09
 */

#include "domain/session_context.hpp"
#include "isa/domain_types.hpp"
#include "isa/values.hpp"
#include "core/idecode_table.hpp"
#include "core/icore_service.hpp"
#include <optional>
#include <vector>

namespace isa {

class ITestService {
public:
    virtual ~ITestService() = default;

    virtual Result<TestReport> runSuite(SuiteId s, DiffMode m, const CancelToken& tk) = 0;
    // 批量执行（M-13）
    virtual std::vector<ReportRow> queryReports(UserId u, std::optional<SuiteId> s) = 0;
    // 报告列表（DD-5）
    virtual Result<TestReport> getReport(UserId u, ReportId id) = 0;
    // 取报告（不含 snapshot_blob）
    virtual Result<CaseSnapshot> snapshotOf(ReportId r, CaseId c) = 0;
    // 取用例复现快照
};

}  // namespace isa
