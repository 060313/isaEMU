/**
 * ArchState —— 架构状态（SS-1 构件 2）
 *
 * 设计依据：6.4.1 / 6.3.3；档 2（装配可见）
 */

#include "core/arch_state.hpp"
#include "core/mem_types.hpp"

namespace isa {

void ArchState::apply(span<const WriteOp> writes) {
    // TODO: 实现 —— 差分写回；写 x0 被丢弃（M-03）
    (void)this;
}

StateSnapshot ArchState::snapshot(ReadScope scope) {
    // TODO: 实现 —— 取只读快照
    return {};
}

void ArchState::restore(const StateSnapshot& s) {
    // TODO: 实现 —— 仅 EmulatorCore 调用
    (void)this;
}

Bytes ArchState::read(Addr a, std::size_t n) {
    // TODO: 实现 —— 内存读
    return {};
}

void ArchState::write(Addr a, span<const std::uint8_t> bytes) {
    // TODO: 实现 —— 内存写
    (void)this;
}

void ArchState::reset(const InitState& init) {
    // TODO: 实现 —— 恢复初态
    (void)this;
}

}  // namespace isa
