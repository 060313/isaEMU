#pragma once

/**
 * SessionService —— 会话服务（SS-5 构件 1）
 *
 * 设计依据：6.4.5；档 2。实现 ISessionService
 */

#include "domain/i_session_service.hpp"
#include "domain/session_context.hpp"
#include "isa/values.hpp"
#include <map>
#include <memory>

namespace isa {

class SessionService : public ISessionService {
public:
    SessionService(IStore& store, IIdGen& ids, const IConfig& cfg, ILogger& log);

    Result<LoginResult> login(const Credential& c);
    // 取凭据行 → 哑元 KDF → 建会话（M-10）
    void logout(Token t);
    // 结束会话
    Result<SessionContext&> contextOf(Token t);
    // 解析上下文（D-3）
    std::size_t reap(const Clock& now);
    // 回收超时会话（M-11）
    std::vector<User> listUsers();
    // 用户列表
    Result<void> updateUser(UserId u, const UserPatch& p);
    // 更新用户
    Usage queryUsage(UserId u);
    // 窗口用量

private:
    Result<LoginResult> createSession(const Credential& c);
    // 建会话 + 建工作区
    bool expired(const SessionContext& ctx, const Clock& now) const;
    // 超时判定
    IStore* store_;  // 关联
    IIdGen* ids_;  // 关联
    const IConfig* cfg_;  // 关联
    ILogger* log_;  // 关联
    std::map<Token, std::unique_ptr<SessionContext>> live_;  // 活跃会话；移出即触发内核析构
};

}  // namespace isa
