/**
 * SessionContext —— 会话上下文（SS-5 的内部结构，档 3）
 *
 * 设计依据：6.3.3；R3 / SA-03：内核生命周期由会话上下文唯一负责
 */

#include "domain/session_context.hpp"

namespace isa {

SessionContext::SessionContext(Token t, UserId u, WorkspaceId w, SpecId isa, class IStore& store) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

const Token& SessionContext::token() const {
    // TODO: 实现 —— 会话令牌
    static Token kFallback{};
    return kFallback;
}

UserId SessionContext::uid() const {
    // TODO: 实现 —— 所有者（隔离谓词来源）
    return {};
}

WorkspaceId SessionContext::ws() const {
    // TODO: 实现 —— 默认工作区
    return {};
}

SpecId SessionContext::isa() const {
    // TODO: 实现 —— 当前 ISA（会话级；多会话可各用不同 ISA）
    return {};
}

void SessionContext::touch(const Clock& now) {
    // TODO: 实现 —— 推进 lastSeen（落库有 tHeartbeat 节流）
    (void)this;
}

bool SessionContext::expired(const Clock& now, Duration timeout) const {
    // TODO: 实现 —— 空闲超时判定
    return false;
}

ICoreService& SessionContext::core() {
    // TODO: 返回内核引用（D-3）
    return *core_;
}

BreakpointTable& SessionContext::breakpoints() {
    // TODO: 实现 —— 断点表
    static BreakpointTable kFallback{};
    return kFallback;
}

}  // namespace isa
