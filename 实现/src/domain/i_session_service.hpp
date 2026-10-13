#pragma once

/**
 * ISessionService —— 会话服务契约
 *
 * 设计依据：6.4.2；UC-01 / UC-14
 */

#include "domain/session_context.hpp"
#include "isa/domain_types.hpp"
#include "isa/values.hpp"
#include "core/idecode_table.hpp"
#include "core/icore_service.hpp"
#include <optional>
#include <vector>

namespace isa {

class ISessionService {
public:
    virtual ~ISessionService() = default;

    virtual Result<LoginResult> login(const Credential& c) = 0;
    // 取凭据行 → 哑元 KDF → 建会话 + 建工作区（M-10）
    virtual void logout(Token t) = 0;
    // 结束会话
    virtual Result<SessionContext&> contextOf(Token t) = 0;
    // 解析会话上下文（D-3：服务不持有内核引用）
    virtual std::size_t reap(const Clock& now) = 0;
    // 回收超时会话（M-11）
    virtual std::vector<User> listUsers() = 0;
    // 管理员视角的用户列表
    virtual Result<void> updateUser(UserId u, const UserPatch& p) = 0;
    // 配额与状态的局部更新
    virtual Usage queryUsage(UserId u) = 0;
    // 窗口用量
};

}  // namespace isa
