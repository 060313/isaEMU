#pragma once

/**
 * FileConfig —— 配置服务实现（SS-8，从文件与环境变量读取）
 *
 * 设计依据：6.4.8；SA-09 双形态同源
 */

#include "base/i_config.hpp"
#include "isa/values.hpp"
#include <string>

namespace isa {

class FileConfig : public IConfig {
public:
    DriverKind dbDriver();
    bool authEnabled();
    std::uint64_t instrLimit();
    std::size_t traceCapacity();
    Duration sessionTimeout();
    std::uint32_t cancelCheckInterval();
    std::string toolchainPath();
    std::string spikePath();
    std::uint16_t port();

private:
    std::string path_;  // 配置文件路径
};

}  // namespace isa
