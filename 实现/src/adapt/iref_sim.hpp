#pragma once

/**
 * IRefSim —— 参考模拟器适配契约（SS-4）
 *
 * 设计依据：6.4.2；5.4「定义方 SS-4、实现方 RefSimAdapter」
 */

#include "isa/values.hpp"
#include "isa/domain_types.hpp"
#include <vector>

namespace isa {

class IRefSim {
public:
    virtual ~IRefSim() = default;

    virtual Result<std::vector<StepRecord>> run(const Program& p, const DiffScope& sc, const CancelToken& tk) = 0;
    // 驱动参考方并解析提交日志
    virtual bool available() = 0;
    // 参考方是否可用
};

}  // namespace isa
