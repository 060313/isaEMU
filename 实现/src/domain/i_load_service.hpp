#pragma once

/**
 * ILoadService —— 装载服务契约
 *
 * 设计依据：6.4.2；UC-03 / UC-12
 */

#include "domain/session_context.hpp"
#include "isa/domain_types.hpp"
#include "isa/values.hpp"
#include "core/idecode_table.hpp"
#include "core/icore_service.hpp"
#include <optional>
#include <vector>

namespace isa {

class ILoadService {
public:
    virtual ~ILoadService() = default;

    virtual Result<Image> assemble(const SourceRef& src) = 0;
    // 仅汇编（D-7：不接着调 loadProgram 即为「仅汇编不装载」）
    virtual Result<LoadResult> loadProgram(const LoadSpec& s) = 0;
    // 汇编 + 装载（整体替换式）
    virtual std::vector<ExampleId> examples() = 0;
    // 内置示例列表
};

}  // namespace isa
