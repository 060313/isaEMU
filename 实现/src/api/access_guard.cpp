/**
 * AccessGuard —— 鉴权与配额检查（SS-6 构件 3）
 *
 * 设计依据：6.4.6；档 2。SA-05 的唯一落点
 */

#include "api/access_guard.hpp"

namespace isa {

AccessGuard::AccessGuard(const IConfig& cfg, IStore& store, ILogger& log) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

Result<Caller> AccessGuard::authorize(const Credential& c) {
    // TODO: 实现 —— 鉴权（方式一）
    return Result<Caller>::err(ErrCode::NotImplemented, "AccessGuard::authorize");
}

Result<void> AccessGuard::checkQuota(UserId u, OpKind op) {
    // TODO: 实现 —— 配额检查（方式一）
    return Result<void>::err(ErrCode::NotImplemented, "AccessGuard::checkQuota");
}

Result<void> AccessGuard::checkInstrLimit(UserId u, std::uint64_t n) {
    // TODO: 实现 —— 单次请求指令条数上限（与 IConfig.instrLimit 同源，C-02 的收口）
    return Result<void>::err(ErrCode::NotImplemented, "AccessGuard::checkInstrLimit");
}

}  // namespace isa
