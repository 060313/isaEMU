/**
 * TestService —— 测试服务（SS-5 构件 5）
 *
 * 设计依据：6.4.5；档 2。实现 ITestService
 */

#include "domain/test_service.hpp"

namespace isa {

TestService::TestService(SessionService& sess, ICompareService& cmp, IStore& store) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

Result<TestReport> TestService::runSuite(SuiteId s, DiffMode m, const CancelToken& tk) {
    // TODO: 实现 —— 批量执行（M-13）
    return Result<TestReport>::err(ErrCode::NotImplemented, "TestService::runSuite");
}

std::vector<ReportRow> TestService::queryReports(UserId u, std::optional<SuiteId> s) {
    // TODO: 实现 —— 报告列表
    return {};
}

Result<TestReport> TestService::getReport(UserId u, ReportId id) {
    // TODO: 实现 —— 取报告
    return Result<TestReport>::err(ErrCode::NotImplemented, "TestService::getReport");
}

Result<CaseSnapshot> TestService::snapshotOf(ReportId r, CaseId c) {
    // TODO: 实现 —— 用例快照
    return Result<CaseSnapshot>::err(ErrCode::NotImplemented, "TestService::snapshotOf");
}

TestReport TestService::summarize(span<const CaseResult> rs) {
    // TODO: 实现 —— 汇总
    return {};
}

CaseResult TestService::runOne(const TestCase& c, DiffMode m, const CancelToken& tk) {
    // TODO: 实现 —— 单用例执行
    return {};
}

}  // namespace isa
