#pragma once

/**
 * CompareEngine —— 比对引擎（SS-3 构件 1，零属性）
 *
 * 设计依据：6.4.4 / 6.3.3；类设计总则 G-4「函数式核心」
 */

#include "compare/icompare_service.hpp"
#include "isa/compare_types.hpp"
#include "isa/values.hpp"
#include <optional>

namespace isa {

class CompareEngine : public ICompareService {
public:
    std::optional<Divergence> compare(span<const StepRecord> a, span<const StepRecord> b, const DiffScope& sc, DivergenceId id);
    // 按步号同步推进，命中首个差异即返回
    std::optional<Divergence> compareFinal(const StateSnapshot& a, const StateSnapshot& b, const DiffScope& sc, DivergenceId id);
    // 终态比对
    std::optional<Divergence> firstDiff(span<const StepRecord> a, span<const StepRecord> b, const DiffScope& sc, DivergenceId id);
    // 只定位首个分歧（复用同一引擎）
};

}  // namespace isa
