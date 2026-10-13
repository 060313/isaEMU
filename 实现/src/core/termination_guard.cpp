/**
 * TerminationGuard —— 终止与异常判定（SS-1 构件 4）
 *
 * 设计依据：6.4.1 / 6.3.3；档 2
 */

#include "core/termination_guard.hpp"

namespace isa {

GuardVerdict TerminationGuard::check(const ArchState& st, Enc enc) {
    // TODO: 实现 —— 先查终止序列，再查停机条件（M-06）
    return {};
}

void TerminationGuard::captureFault(const FaultRecord& f) {
    // TODO: 实现 —— 写入异常现场
    (void)this;
}

void TerminationGuard::reset() {
    // TODO: 实现 —— 清除终止与异常标志
    (void)this;
}

}  // namespace isa
