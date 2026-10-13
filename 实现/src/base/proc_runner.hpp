#pragma once

/**
 * ProcRunner —— 外部进程调用实现（SS-8）
 *
 * 设计依据：6.4.8
 */

#include "base/i_process_runner.hpp"
#include "isa/values.hpp"
#include <string>

namespace isa {

class ProcRunner : public IProcessRunner {
public:
    Result<RunOutcome> run(const RunSpec& spec, const CancelToken& tk);
    bool available(const std::string& path);
};

}  // namespace isa
