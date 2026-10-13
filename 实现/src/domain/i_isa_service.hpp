#pragma once

/**
 * IIsaService —— ISA 管理契约
 *
 * 设计依据：6.4.2；UC-02
 */

#include "domain/session_context.hpp"
#include "isa/domain_types.hpp"
#include "isa/values.hpp"
#include "core/idecode_table.hpp"
#include "core/icore_service.hpp"
#include <optional>
#include <vector>

namespace isa {

class IIsaService {
public:
    virtual ~IIsaService() = default;

    virtual Result<IsaSpec> loadSpec(const SourceRef& src) = 0;
    // 装载描述
    virtual std::vector<Issue> validate(const IsaSpec& spec) = 0;
    // 校验
    virtual SpecId current() = 0;
    // 当前 ISA 标识
    virtual Result<void> switchTo(SpecId id) = 0;
    // 切换 ISA
};

}  // namespace isa
