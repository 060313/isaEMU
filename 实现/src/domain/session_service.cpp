/**
 * SessionService —— 会话服务（SS-5 构件 1）
 *
 * 设计依据：6.4.5；档 2。实现 ISessionService
 */

#include "domain/session_service.hpp"

namespace isa {

SessionService::SessionService(IStore& store, IIdGen& ids, const IConfig& cfg, ILogger& log) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

Result<LoginResult> SessionService::login(const Credential& c) {
    // TODO: 实现 —— 取凭据行 → 哑元 KDF → 建会话（M-10）
    return Result<LoginResult>::err(ErrCode::NotImplemented, "SessionService::login");
}

void SessionService::logout(Token t) {
    // TODO: 实现 —— 结束会话
    (void)this;
}

Result<SessionContext&> SessionService::contextOf(Token t) {
    // TODO: 实现 —— 解析上下文（D-3）
    return Result<SessionContext&>::err(ErrCode::NotImplemented, "SessionService::contextOf");
}

std::size_t SessionService::reap(const Clock& now) {
    // TODO: 实现 —— 回收超时会话（M-11）
    return {};
}

std::vector<User> SessionService::listUsers() {
    // TODO: 实现 —— 用户列表
    return {};
}

Result<void> SessionService::updateUser(UserId u, const UserPatch& p) {
    // TODO: 实现 —— 更新用户
    return Result<void>::err(ErrCode::NotImplemented, "SessionService::updateUser");
}

Usage SessionService::queryUsage(UserId u) {
    // TODO: 实现 —— 窗口用量
    return {};
}

Result<LoginResult> SessionService::createSession(const Credential& c) {
    // TODO: 实现 —— 建会话 + 建工作区
    return Result<LoginResult>::err(ErrCode::NotImplemented, "SessionService::createSession");
}

bool SessionService::expired(const SessionContext& ctx, const Clock& now) const {
    // TODO: 实现 —— 超时判定
    return false;
}

}  // namespace isa
