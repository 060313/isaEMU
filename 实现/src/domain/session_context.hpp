#pragma once

/**
 * SessionContext —— 会话上下文（SS-5 的内部结构，档 3）
 *
 * 设计依据：6.3.3；R3 / SA-03：内核生命周期由会话上下文唯一负责
 */

#include "core/icore_service.hpp"
#include "domain/breakpoint_table.hpp"
#include "isa/values.hpp"
#include <memory>

namespace isa {

class SessionContext {
public:
    SessionContext(Token t, UserId u, WorkspaceId w, SpecId isa, class IStore& store);

    const Token& token() const;
    // 会话令牌
    UserId uid() const;
    // 所有者（隔离谓词来源）
    WorkspaceId ws() const;
    // 默认工作区
    SpecId isa() const;
    // 当前 ISA（会话级；多会话可各用不同 ISA）
    void touch(const Clock& now);
    // 推进 lastSeen（落库有 tHeartbeat 节流）
    bool expired(const Clock& now, Duration timeout) const;
    // 空闲超时判定
    ICoreService& core();
    // D-3：服务经此取内核引用，而不是自行持有
    BreakpointTable& breakpoints();
    // 断点表

private:
    Token token_;  // 构造注入
    UserId uid_;  // 构造注入
    WorkspaceId ws_;  // 构造注入
    SpecId isa_;  // 构造注入
    Timestamp lastSeen_;  // 构造时 = clock.now()
    std::unique_ptr<ICoreService> core_;  // 组合 R-05 / SA-03
    std::unique_ptr<BreakpointTable> bps_;  // 组合 R-06
};

}  // namespace isa
