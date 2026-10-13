/**
 * RefSimAdapter —— 参考模拟器适配（SS-4 构件 2）
 *
 * 设计依据：6.4.5；档 2
 */

#include "adapt/ref_sim_adapter.hpp"

namespace isa {

RefSimAdapter::RefSimAdapter(const IProcessRunner& runner, const IConfig& cfg) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

Result<std::vector<StepRecord>> RefSimAdapter::run(const Program& p, const DiffScope& sc, const CancelToken& tk) {
    // TODO: 实现 —— 驱动参考方
    return Result<std::vector<StepRecord>>::err(ErrCode::NotImplemented, "RefSimAdapter::run");
}

bool RefSimAdapter::available() {
    // TODO: 实现 —— 可用性探测
    return false;
}

void RefSimAdapter::degrade() {
    // TODO: 实现 —— 标记降级（参考方不可用时）
    (void)this;
}

}  // namespace isa
