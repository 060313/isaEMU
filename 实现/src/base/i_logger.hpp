#pragma once

/**
 * ILogger —— 日志服务契约（SS-8）
 *
 * 设计依据：6.4.8；异常现场（FR-3.5）落这里
 */

#include "isa/values.hpp"
#include <string_view>

namespace isa {

class ILogger {
public:
    virtual ~ILogger() = default;

    virtual void log(Level lv, std::string_view msg) = 0;
    virtual void logAt(Level lv, std::string_view msg, const FaultRecord& f) = 0;
    // 带异常现场的日志
};

}  // namespace isa
