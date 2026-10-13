#pragma once

/**
 * IsaService —— ISA 管理服务（SS-5 构件 2）
 *
 * 设计依据：6.4.5；档 2。实现 IIsaService
 */

#include "domain/i_isa_service.hpp"
#include "isa/iisa_provider.hpp"
#include "isa/values.hpp"
#include <vector>

namespace isa {

class IsaService : public IIsaService {
public:
    IsaService(IIsaProvider& prov, IStore& store, ILogger& log);

    Result<IsaSpec> loadSpec(const SourceRef& src);
    // 装载描述
    std::vector<Issue> validate(const IsaSpec& spec);
    // 校验
    SpecId current();
    // 当前 ISA
    Result<void> switchTo(SpecId id);
    // 切换 ISA

private:
    Result<void> saveActive(const IsaSpec& spec);
    // 记录最近一次装载（仅作提示）
    IIsaProvider* prov_;  // 关联
    IStore* store_;  // 关联
    ILogger* log_;  // 关联
};

}  // namespace isa
