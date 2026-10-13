#pragma once

/**
 * RefSimAdapter —— 参考模拟器适配（SS-4 构件 2）
 *
 * 设计依据：6.4.5；档 2
 */

#include "adapt/iref_sim.hpp"
#include "isa/values.hpp"
#include <vector>

namespace isa {

class RefSimAdapter : public IRefSim {
public:
    explicit RefSimAdapter(const IProcessRunner& runner, const IConfig& cfg);

    Result<std::vector<StepRecord>> run(const Program& p, const DiffScope& sc, const CancelToken& tk);
    // 驱动参考方
    bool available();
    // 可用性探测

private:
    void degrade();
    // 标记降级（参考方不可用时）
    const IProcessRunner* runner_;  // 关联
    const IConfig* cfg_;  // 关联；取 spikePath()
    bool degraded_;  // 降级标志
};

}  // namespace isa
