#pragma once

/**
 * IStore —— 持久化服务契约（SS-8；18 个操作）
 *
 * 设计依据：7.4.2 操作清单；6.4.8
 */

#include "isa/domain_types.hpp"
#include "isa/compare_types.hpp"
#include "isa/values.hpp"
#include "isa/span.hpp"
#include <optional>
#include <string>
#include <vector>

namespace isa {

class IStore {
public:
    virtual ~IStore() = default;

    virtual std::optional<User> findUser(UserId u) = 0;
    // O-01；谓词 uid = :u
    virtual std::optional<User> findUserByName(std::string n) = 0;
    // O-02；免谓词入口（登录前）
    virtual std::optional<CredentialRow> findCredential(std::string n) = 0;
    // O-03；免谓词入口（DD-1 新增）
    virtual void saveUser(UserId u, const User& x) = 0;
    // O-04；UPSERT
    virtual std::vector<User> queryUsers() = 0;
    // O-05；管理员视角
    virtual Usage queryUsage(UserId u) = 0;
    // O-06；三段组装（DD-4）
    virtual void saveSession(Token t, const SessionRow& r) = 0;
    // O-07；按 token 定位（免谓词）
    virtual void dropSession(Token t) = 0;
    // O-08；写 ended_at，不物理删
    virtual Version putWorkspace(UserId u, const Workspace& w) = 0;
    // O-09；事务 T-1
    virtual std::optional<Workspace> getWorkspace(UserId u, WorkspaceId id) = 0;
    // O-10；含 optional<Program> / vector<TestSuite>
    virtual std::vector<WorkspaceBrief> queryWorkspaces(UserId u) = 0;
    // O-11；UI-09 列表（DD-5 新增）
    virtual void saveReport(UserId u, const TestReport& r) = 0;
    // O-12；事务 T-2
    virtual std::optional<TestReport> getReport(UserId u, ReportId id) = 0;
    // O-13；不含 snapshot_blob
    virtual std::vector<ReportRow> queryReports(UserId u, std::optional<SuiteId> s) = 0;
    // O-14；UI-06 列表（DD-5 新增）
    virtual void saveBreakpoints(UserId u, const BreakpointRow& b) = 0;
    // O-15；整表替换
    virtual BreakpointRow loadBreakpoints(UserId u, WorkspaceId w) = 0;
    // O-16；双参（M-09 签名细化）
    virtual void saveDivergence(UserId u, span<const Divergence> d) = 0;
    // O-17；批量 INSERT
    virtual std::vector<Divergence> queryDivergence(UserId u, JobId j) = 0;
    // O-18；job_id 为逻辑引用，无外键
};

}  // namespace isa
