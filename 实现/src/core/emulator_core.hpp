#pragma once

/**
 * EmulatorCore —— 执行内核（SS-1 构件 1）
 *
 * 设计依据：6.4.1 / 6.3.3；档 2。实现 ICoreService
 */

#include "core/icore_service.hpp"
#include "core/arch_state.hpp"
#include "core/trace.hpp"
#include "core/termination_guard.hpp"
#include "isa/values.hpp"

namespace isa {

class EmulatorCore : public ICoreService {
public:
    explicit EmulatorCore(std::size_t traceCapacity);

    void load(const Image& img, Addr base, const InitState& init);
    // 整体替换式装载
    void attachDecodeTable(const IDecodeTable& dt);
    // 绑定译码表
    StepDelta step(std::uint32_t n = 1);
    // 执行 n 步（默认 1）
    RunResult run(RunMode m, Addr param, std::uint64_t limit, const CancelToken& tk);
    // 主循环（M-01）
    void pause();
    // 请求暂停
    void reset();
    // 恢复初态
    RunState state();
    // 只读查询
    StateSnapshot reads(ReadScope scope);
    // 只读快照
    void restore(const StateSnapshot& s);
    // 用快照覆盖状态（R2）

private:
    WriteOpList cycle();
    // 管道四段：取指 → 译码 → 执行 → 写回（M-02）
    bool atBoundary();
    // pc 不在映像区间内（FR-4.3 的边界判定）
    void deliver(const StepDelta& d);
    // 组装增量
    std::unique_ptr<ArchState> arch_;  // 组合 R-01
    std::unique_ptr<Trace> trace_;  // 组合 R-02
    std::unique_ptr<TerminationGuard> guard_;  // 组合 R-03
    const IDecodeTable* decode_;  // 非拥有关联；未装载译码表时为空
    ImageDesc image_;  // 映像摘要；atBoundary() 读它
    RunState st_;  // 状态图② 的六取值之一
    std::uint64_t steps_;  // 本次装载后的累计步数
    std::uint64_t limit_;  // 本次运行的条数上限（参数快照，非会话配置）
    const CancelToken* tk_;  // 本次运行的取消令牌
    bool traceOn_;  // 轨迹开关
};

}  // namespace isa
