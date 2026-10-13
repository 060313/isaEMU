/**
 * ProcRunner —— 外部进程调用实现（SS-8）
 *
 * 设计依据：6.4.8
 */

#include "base/proc_runner.hpp"

namespace isa {

Result<RunOutcome> ProcRunner::run(const RunSpec& spec, const CancelToken& tk) {
    // TODO: 实现 —— run
    return Result<RunOutcome>::err(ErrCode::NotImplemented, "ProcRunner::run");
}

bool ProcRunner::available(const std::string& path) {
    // TODO: 实现 —— available
    return false;
}

}  // namespace isa
