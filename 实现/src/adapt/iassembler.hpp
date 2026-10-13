#pragma once

/**
 * IAssembler —— 工具链适配契约（SS-4，SA-06 使外部工具经子进程隔离）
 *
 * 设计依据：6.4.2；5.4「定义方 SS-4、实现方 ToolchainAdapter」
 */

#include "isa/values.hpp"

namespace isa {

class IAssembler {
public:
    virtual ~IAssembler() = default;

    virtual Result<Image> assemble(const SourceRef& src, const CancelToken& tk) = 0;
    // 汇编；D-7：不再提供 assembleOnly，「仅汇编不装载」是调用方不调 loadProgram
};

}  // namespace isa
