#pragma once

/**
 * IConfig —— 配置服务契约（SS-8）
 *
 * 设计依据：6.4.8；双形态同源（SA-09）只靠配置项区分
 */

#include "isa/values.hpp"
#include <cstdint>
#include <string>

namespace isa {

class IConfig {
public:
    virtual ~IConfig() = default;

    virtual DriverKind dbDriver() = 0;
    virtual bool authEnabled() = 0;
    virtual std::uint64_t instrLimit() = 0;
    // 「上限」的唯一取值点（C-02 的收口）
    virtual std::size_t traceCapacity() = 0;
    virtual Duration sessionTimeout() = 0;
    virtual std::uint32_t cancelCheckInterval() = 0;
    // 取消检查的批次间隔，默认 4096（⑦-1）
    virtual std::string toolchainPath() = 0;
    virtual std::string spikePath() = 0;
    virtual std::uint16_t port() = 0;
};

}  // namespace isa
