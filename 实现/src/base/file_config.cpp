/**
 * FileConfig —— 配置服务实现（SS-8，从文件与环境变量读取）
 *
 * 设计依据：6.4.8；SA-09 双形态同源
 */

#include "base/file_config.hpp"

namespace isa {

DriverKind FileConfig::dbDriver() {
    // TODO: 实现 —— dbDriver
    return {};
}

bool FileConfig::authEnabled() {
    // TODO: 实现 —— authEnabled
    return false;
}

std::uint64_t FileConfig::instrLimit() {
    // TODO: 实现 —— instrLimit
    return {};
}

std::size_t FileConfig::traceCapacity() {
    // TODO: 实现 —— traceCapacity
    return {};
}

Duration FileConfig::sessionTimeout() {
    // TODO: 实现 —— sessionTimeout
    return {};
}

std::uint32_t FileConfig::cancelCheckInterval() {
    // TODO: 实现 —— cancelCheckInterval
    return {};
}

std::string FileConfig::toolchainPath() {
    // TODO: 实现 —— toolchainPath
    return {};
}

std::string FileConfig::spikePath() {
    // TODO: 实现 —— spikePath
    return {};
}

std::uint16_t FileConfig::port() {
    // TODO: 实现 —— port
    return {};
}

}  // namespace isa
