/**
 * IsaService —— ISA 管理服务（SS-5 构件 2）
 *
 * 设计依据：6.4.5；档 2。实现 IIsaService
 */

#include "domain/isa_service.hpp"

namespace isa {

IsaService::IsaService(IIsaProvider& prov, IStore& store, ILogger& log) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

Result<IsaSpec> IsaService::loadSpec(const SourceRef& src) {
    // TODO: 实现 —— 装载描述
    return Result<IsaSpec>::err(ErrCode::NotImplemented, "IsaService::loadSpec");
}

std::vector<Issue> IsaService::validate(const IsaSpec& spec) {
    // TODO: 实现 —— 校验
    return {};
}

SpecId IsaService::current() {
    // TODO: 实现 —— 当前 ISA
    return {};
}

Result<void> IsaService::switchTo(SpecId id) {
    // TODO: 实现 —— 切换 ISA
    return Result<void>::err(ErrCode::NotImplemented, "IsaService::switchTo");
}

Result<void> IsaService::saveActive(const IsaSpec& spec) {
    // TODO: 实现 —— 记录最近一次装载（仅作提示）
    return Result<void>::err(ErrCode::NotImplemented, "IsaService::saveActive");
}

}  // namespace isa
