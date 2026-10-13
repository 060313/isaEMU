#pragma once

/**
 * IProcessRunner —— 外部进程调用契约（SS-8）
 *
 * 设计依据：6.4.8；SA-06：外部工具与参考模拟器一律经子进程隔离
 */

#include "isa/values.hpp"
#include <string>

namespace isa {

class IProcessRunner {
public:
    virtual ~IProcessRunner() = default;

    virtual Result<RunOutcome> run(const RunSpec& spec, const CancelToken& tk) = 0;
    // 即起即收
    virtual bool available(const std::string& path) = 0;
    // 路径可用性探测
};

}  // namespace isa
