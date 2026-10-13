/**
 * EmulatorCore —— 执行内核（SS-1 构件 1）
 *
 * 设计依据：6.4.1 / 6.3.3；档 2。实现 ICoreService
 */

#include "core/emulator_core.hpp"

namespace isa {

EmulatorCore::EmulatorCore(std::size_t traceCapacity) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

void EmulatorCore::load(const Image& img, Addr base, const InitState& init) {
    // TODO: 实现 —— 整体替换式装载
    (void)this;
}

void EmulatorCore::attachDecodeTable(const IDecodeTable& dt) {
    // TODO: 实现 —— 绑定译码表
    (void)this;
}

StepDelta EmulatorCore::step(std::uint32_t n) {
    // TODO: 实现 —— 执行 n 步（默认 1）
    return {};
}

RunResult EmulatorCore::run(RunMode m, Addr param, std::uint64_t limit, const CancelToken& tk) {
    // TODO: 实现 —— 主循环（M-01）
    return {};
}

void EmulatorCore::pause() {
    // TODO: 实现 —— 请求暂停
    (void)this;
}

void EmulatorCore::reset() {
    // TODO: 实现 —— 恢复初态
    (void)this;
}

RunState EmulatorCore::state() {
    // TODO: 实现 —— 只读查询
    return {};
}

StateSnapshot EmulatorCore::reads(ReadScope scope) {
    // TODO: 实现 —— 只读快照
    return {};
}

void EmulatorCore::restore(const StateSnapshot& s) {
    // TODO: 实现 —— 用快照覆盖状态（R2）
    (void)this;
}

WriteOpList EmulatorCore::cycle() {
    // TODO: 实现 —— 管道四段：取指 → 译码 → 执行 → 写回（M-02）
    return {};
}

bool EmulatorCore::atBoundary() {
    // TODO: 实现 —— pc 不在映像区间内（FR-4.3 的边界判定）
    return false;
}

void EmulatorCore::deliver(const StepDelta& d) {
    // TODO: 实现 —— 组装增量
    (void)this;
}

}  // namespace isa
