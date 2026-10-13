#pragma once

/**
 * DebugService —— 调试服务（SS-5 构件 4）
 *
 * 设计依据：6.4.5；档 2。实现 IDebugService；断点展开在服务层（M-12）
 */

#include "domain/i_debug_service.hpp"
#include "domain/session_service.hpp"
#include "isa/values.hpp"

namespace isa {

class DebugService : public IDebugService {
public:
    DebugService(SessionService& sess, ILogger& log);

    Result<RunResult> execute(RunMode m, Addr param, std::uint64_t limit);
    // 按模式分派
    StateSnapshot readState(ReadScope scope);
    // 读状态
    Result<void> rollback(StepNo target);
    // 回退
    std::vector<Breakpoint> registerBreakpoint(Addr a, BpOp op);
    // 断点操作
    bool checkHit(Addr a);
    // 断点命中

private:
    Result<WorkspaceId> effectiveWs(Token t);
    // 从会话上下文取工作区（供断点读写）
    SessionService* sess_;  // 关联
    ILogger* log_;  // 关联
};

}  // namespace isa
