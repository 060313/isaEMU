#pragma once

/**
 * TerminationGuard —— 终止与异常判定（SS-1 构件 4）
 *
 * 设计依据：6.4.1 / 6.3.3；档 2
 */

#include "isa/values.hpp"
#include <array>
#include <optional>

namespace isa {

class TerminationGuard {
public:
    GuardVerdict check(const ArchState& st, Enc enc);
    // 先查终止序列，再查停机条件（M-06）
    void captureFault(const FaultRecord& f);
    // 写入异常现场
    void reset();
    // 清除终止与异常标志

private:
    std::array<Enc, 3> last_;  // 最近三条指令编码
    bool halted_;  // 已判定的终止标志
    std::optional<FaultRecord> fault_;  // 异常现场
};

}  // namespace isa
