#pragma once

/**
 * StdLogger —— 日志服务实现（SS-8，写标准错误）
 *
 * 设计依据：6.4.8
 */

#include "base/i_logger.hpp"
#include "isa/values.hpp"
#include <string_view>

namespace isa {

class StdLogger : public ILogger {
public:
    void log(Level lv, std::string_view msg);
    void logAt(Level lv, std::string_view msg, const FaultRecord& f);
};

}  // namespace isa
