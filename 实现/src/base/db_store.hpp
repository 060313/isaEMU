#pragma once

/**
 * DbStore —— 持久化服务实现（SS-8）
 *
 * 设计依据：7.4；6.4.8。实现 IStore；D-5 的 scoped 是隔离唯一入口
 */

#include "base/i_store.hpp"
#include "base/db_driver.hpp"
#include "isa/values.hpp"
#include <string>
#include <vector>

namespace isa {

class DbStore : public IStore {
public:
    explicit DbStore(DbDriver& driver);

    std::optional<User> findUser(UserId u);
    std::optional<User> findUserByName(std::string n);
    std::optional<CredentialRow> findCredential(std::string n);
    void saveUser(UserId u, const User& x);
    std::vector<User> queryUsers();
    Usage queryUsage(UserId u);
    void saveSession(Token t, const SessionRow& r);
    void dropSession(Token t);
    Version putWorkspace(UserId u, const Workspace& w);
    std::optional<Workspace> getWorkspace(UserId u, WorkspaceId id);
    std::vector<WorkspaceBrief> queryWorkspaces(UserId u);
    void saveReport(UserId u, const TestReport& r);
    std::optional<TestReport> getReport(UserId u, ReportId id);
    std::vector<ReportRow> queryReports(UserId u, std::optional<SuiteId> s);
    void saveBreakpoints(UserId u, const BreakpointRow& b);
    BreakpointRow loadBreakpoints(UserId u, WorkspaceId w);
    void saveDivergence(UserId u, span<const Divergence> d);
    std::vector<Divergence> queryDivergence(UserId u, JobId j);

private:
    std::string scoped(std::string sql, UserId u);
    // M-15：唯一拼装入口，追加 AND owner_id = :u；参数经占位符绑定（不拼字符串）
    DbDriver* driver_;  // 关联
};

}  // namespace isa
