/**
 * Trace —— 执行轨迹（SS-1 构件 3）
 *
 * 设计依据：6.4.1 / 6.3.3；档 2。轨迹可裁剪为 SA-13 的「可回退」提供落点
 */

#include "core/trace.hpp"

namespace isa {

Trace::Trace(std::size_t cap) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

void Trace::enable(bool on) {
    // TODO: 实现 —— 关闭时不追加；rewindTo 返回 Err(TraceDisabled)
    (void)this;
}

void Trace::append(const StepRecord& rec) {
    // TODO: 实现 —— 追加一条记录
    (void)this;
}

span<const StepRecord> Trace::query(StepNo from, StepNo to) {
    // TODO: 实现 —— 按步号区间查询
    return {};
}

Result<StateSnapshot> Trace::rewindTo(StepNo target) {
    // TODO: 实现 —— 逆序撤销写操作（M-04）
    return Result<StateSnapshot>::err(ErrCode::NotImplemented, "Trace::rewindTo");
}

void Trace::trim() {
    // TODO: 实现 —— 裁剪至不超限（M-05）
    (void)this;
}

StepNo Trace::base() {
    // TODO: 实现 —— 已被裁剪掉的最早步号
    return {};
}

}  // namespace isa
