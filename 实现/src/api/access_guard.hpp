#pragma once

/**
 * AccessGuard —— 鉴权与配额检查（SS-6 构件 3）
 *
 * 设计依据：6.4.6；档 2。SA-05 的唯一落点
 */

#include "isa/values.hpp"
#include <mutex>

namespace isa {

class AccessGuard {
public:
    AccessGuard(const IConfig& cfg, IStore& store, ILogger& log);

    Result<Caller> authorize(const Credential& c);
    // 鉴权（方式一）
    Result<void> checkQuota(UserId u, OpKind op);
    // 配额检查（方式一）
    Result<void> checkInstrLimit(UserId u, std::uint64_t n);
    // 单次请求指令条数上限（与 IConfig.instrLimit 同源，C-02 的收口）

private:
    const IConfig* cfg_;  // 关联
    IStore* store_;  // 关联
    ILogger* log_;  // 关联
    std::map<UserId, std::pair<std::uint64_t, Timestamp>> rate_;  // 窗口限流计数（进程内并发，见 7.4.5.1）
};

}  // namespace isa
