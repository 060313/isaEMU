#pragma once

/**
 * 比对共享类型：DiffScope / Divergence（档 1）
 *
 * 设计依据：6.4.4 / 6.3.3；档 1（公开契约）。因被 ICompareService 与 IStore 共同引用，置于公共头以避免 SS-3 与 SS-5 之间的头文件循环
 */

#include "isa/values.hpp"
#include <optional>
#include <string>
#include <vector>

namespace isa {

// DiffScope —— 比对子集（不可变）
class DiffScope {
public:
    static DiffScope preset();                              // 默认子集（PC + GPR + 内存写 + 被改 CSR）
    DiffScope configure(FieldMask fields, DiffMode mode) const;  // 内部整体重建
    bool includes(Field f) const;                           // 位掩码判定

    FieldMask fields_{0};   // FR-7.2 的字段子集
    std::uint32_t gprMask_{0xFFFFFFFFu};  // 32 个 GPR 的逐位开关
    DiffMode mode_{DiffMode::Stepwise};
};

// Divergence —— 分歧记录（档 1 数据对象；唯一带可变方法的共享类型）
class Divergence {
public:
    static Divergence make(DivergenceId id, StepNo step, const StateSnapshot& a,
                           const StateSnapshot& b);
    span<const FieldDiff> diffFields() const;
    void update(const Attribution& attr);                   // 唯一可变方法（UC-11）

    // public 只读：读得到，构造后不变
    DivergenceId divId{};
    StepNo stepNo{};
    StateSnapshot sideA;
    StateSnapshot sideB;

private:
    std::vector<FieldDiff> diffs_;          // 差异字段清单
    std::optional<Attribution> attr_{};     // 归因标注
    std::string note_;
};

}  // namespace isa
