#pragma once

/**
 * Trace —— 执行轨迹（SS-1 构件 3）
 *
 * 设计依据：6.4.1 / 6.3.3；档 2。轨迹可裁剪为 SA-13 的「可回退」提供落点
 */

#include "isa/values.hpp"
#include <cstdint>
#include <deque>

namespace isa {

class Trace {
public:
    explicit Trace(std::size_t cap);

    void enable(bool on);
    // 关闭时不追加；rewindTo 返回 Err(TraceDisabled)
    void append(const StepRecord& rec);
    // 追加一条记录
    span<const StepRecord> query(StepNo from, StepNo to);
    // 按步号区间查询
    Result<StateSnapshot> rewindTo(StepNo target);
    // 逆序撤销写操作（M-04）
    void trim();
    // 裁剪至不超限（M-05）
    StepNo base();
    // 已被裁剪掉的最早步号

private:
    std::deque<StepRecord> rec_;  // 尾部追加、头部弹出
    std::size_t cap_;  // IConfig.traceCapacity（落地值 1048576）
    StepNo base_;  // 已被裁剪掉的最早步号
    bool on_;  // 轨迹开关（与 EmulatorCore.traceOn_ 同步）
};

}  // namespace isa
