#pragma once

/**
 * ICompareService —— 比对契约（SS-3，SA-04 使比对独立成子系统）
 *
 * 设计依据：6.4.2；5.4「定义方 SS-3、实现方 CompareEngine、调用方 SS-5 两个服务」
 */

#include "isa/compare_types.hpp"
#include "isa/values.hpp"
#include <optional>

namespace isa {

class ICompareService {
public:
    virtual ~ICompareService() = default;

    virtual std::optional<Divergence> compare(span<const StepRecord> a, span<const StepRecord> b, const DiffScope& sc, DivergenceId id) = 0;
    // 逐条比对；nullopt 表示一致（M-09）
    virtual std::optional<Divergence> compareFinal(const StateSnapshot& a, const StateSnapshot& b, const DiffScope& sc, DivergenceId id) = 0;
    // 终态比对
};

}  // namespace isa
