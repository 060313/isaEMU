/**
 * DebugService —— 调试服务（SS-5 构件 4）
 *
 * 设计依据：6.4.5；档 2。实现 IDebugService；断点展开在服务层（M-12）
 */

#include "domain/debug_service.hpp"

namespace isa {

DebugService::DebugService(SessionService& sess, ILogger& log) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

Result<RunResult> DebugService::execute(RunMode m, Addr param, std::uint64_t limit) {
    // TODO: 实现 —— 按模式分派
    return Result<RunResult>::err(ErrCode::NotImplemented, "DebugService::execute");
}

StateSnapshot DebugService::readState(ReadScope scope) {
    // TODO: 实现 —— 读状态
    return {};
}

Result<void> DebugService::rollback(StepNo target) {
    // TODO: 实现 —— 回退
    return Result<void>::err(ErrCode::NotImplemented, "DebugService::rollback");
}

std::vector<Breakpoint> DebugService::registerBreakpoint(Addr a, BpOp op) {
    // TODO: 实现 —— 断点操作
    return {};
}

bool DebugService::checkHit(Addr a) {
    // TODO: 实现 —— 断点命中
    return false;
}

Result<WorkspaceId> DebugService::effectiveWs(Token t) {
    // TODO: 实现 —— 从会话上下文取工作区（供断点读写）
    return Result<WorkspaceId>::err(ErrCode::NotImplemented, "DebugService::effectiveWs");
}

}  // namespace isa
