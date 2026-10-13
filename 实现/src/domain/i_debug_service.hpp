#pragma once

/**
 * IDebugService —— 调试服务契约
 *
 * 设计依据：6.4.2；UC-04 ~ UC-07
 */

#include "domain/session_context.hpp"
#include "isa/domain_types.hpp"
#include "isa/values.hpp"
#include "core/idecode_table.hpp"
#include "core/icore_service.hpp"
#include <optional>
#include <vector>

namespace isa {

class IDebugService {
public:
    virtual ~IDebugService() = default;

    virtual Result<RunResult> execute(RunMode m, Addr param, std::uint64_t limit) = 0;
    // 按模式分派（M-12）
    virtual StateSnapshot readState(ReadScope scope) = 0;
    // 读架构状态
    virtual Result<void> rollback(StepNo target) = 0;
    // 回退到指定步
    virtual std::vector<Breakpoint> registerBreakpoint(Addr a, BpOp op) = 0;
    // 断点增删改
    virtual bool checkHit(Addr a) = 0;
    // 断点命中判定
};

}  // namespace isa
