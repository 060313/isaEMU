/**
 * BreakpointTable —— 断点表（SS-5 的内部结构，档 3）
 *
 * 设计依据：6.4.1 / 6.3.3；随工作区持久化（T-10）
 */

#include "domain/breakpoint_table.hpp"

namespace isa {

std::vector<Breakpoint> BreakpointTable::apply(Addr a, BpOp op) {
    // TODO: 实现 —— 增删改（E-09 的八种操作）
    return {};
}

bool BreakpointTable::hits(Addr a) const {
    // TODO: 实现 —— 命中判定
    return false;
}

const std::vector<Breakpoint>& BreakpointTable::items() const {
    // TODO: 实现 —— 全部断点
    static std::vector<Breakpoint> kFallback{};
    return kFallback;
}

void BreakpointTable::loadFrom(const BreakpointRow& row) {
    // TODO: 实现 —— 从持久化行恢复
    (void)this;
}

BreakpointRow BreakpointTable::toRow(UserId u, WorkspaceId w) const {
    // TODO: 实现 —— 导出为持久化行
    return {};
}

}  // namespace isa
