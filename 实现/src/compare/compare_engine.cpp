/**
 * CompareEngine —— 比对引擎（SS-3 构件 1，零属性）
 *
 * 设计依据：6.4.4 / 6.3.3；类设计总则 G-4「函数式核心」
 */

#include "compare/compare_engine.hpp"

namespace isa {

std::optional<Divergence> CompareEngine::compare(span<const StepRecord> a, span<const StepRecord> b, const DiffScope& sc, DivergenceId id) {
    // TODO: 实现 —— 按步号同步推进，命中首个差异即返回
    return {};
}

std::optional<Divergence> CompareEngine::compareFinal(const StateSnapshot& a, const StateSnapshot& b, const DiffScope& sc, DivergenceId id) {
    // TODO: 实现 —— 终态比对
    return {};
}

std::optional<Divergence> CompareEngine::firstDiff(span<const StepRecord> a, span<const StepRecord> b, const DiffScope& sc, DivergenceId id) {
    // TODO: 实现 —— 只定位首个分歧（复用同一引擎）
    return {};
}

}  // namespace isa
