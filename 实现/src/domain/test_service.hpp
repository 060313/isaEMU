#pragma once

/**
 * TestService —— 测试服务（SS-5 构件 5）
 *
 * 设计依据：6.4.5；档 2。实现 ITestService
 */

#include "domain/i_test_service.hpp"
#include "domain/session_service.hpp"
#include "compare/icompare_service.hpp"
#include "isa/values.hpp"
#include <map>

namespace isa {

class TestService : public ITestService {
public:
    TestService(SessionService& sess, ICompareService& cmp, IStore& store);

    Result<TestReport> runSuite(SuiteId s, DiffMode m, const CancelToken& tk);
    // 批量执行（M-13）
    std::vector<ReportRow> queryReports(UserId u, std::optional<SuiteId> s);
    // 报告列表
    Result<TestReport> getReport(UserId u, ReportId id);
    // 取报告
    Result<CaseSnapshot> snapshotOf(ReportId r, CaseId c);
    // 用例快照

private:
    TestReport summarize(span<const CaseResult> rs);
    // 汇总
    CaseResult runOne(const TestCase& c, DiffMode m, const CancelToken& tk);
    // 单用例执行
    SessionService* sess_;  // 关联
    ICompareService* cmp_;  // 关联
    IStore* store_;  // 关联
    std::map<JobId, JobEntry> jobs_;  // 在跑的任务
};

}  // namespace isa
