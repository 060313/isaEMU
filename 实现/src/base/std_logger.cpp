/**
 * StdLogger —— 日志服务实现（SS-8，写标准错误）
 *
 * 设计依据：6.4.8
 */

#include "base/std_logger.hpp"

namespace isa {

void StdLogger::log(Level lv, std::string_view msg) {
    // TODO: 实现 —— log
    (void)this;
}

void StdLogger::logAt(Level lv, std::string_view msg, const FaultRecord& f) {
    // TODO: 实现 —— logAt
    (void)this;
}

}  // namespace isa
