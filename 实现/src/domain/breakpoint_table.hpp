#pragma once

/**
 * BreakpointTable —— 断点表（SS-5 的内部结构，档 3）
 *
 * 设计依据：6.4.1 / 6.3.3；随工作区持久化（T-10）
 */

#include "isa/values.hpp"
#include <map>
#include <vector>

namespace isa {

class BreakpointTable {
public:
    std::vector<Breakpoint> apply(Addr a, BpOp op);
    // 增删改（E-09 的八种操作）
    bool hits(Addr a) const;
    // 命中判定
    const std::vector<Breakpoint>& items() const;
    // 全部断点
    void loadFrom(const BreakpointRow& row);
    // 从持久化行恢复
    BreakpointRow toRow(UserId u, WorkspaceId w) const;
    // 导出为持久化行

private:
    std::map<Addr, Breakpoint> on_;  // 按地址索引
};

}  // namespace isa
