#pragma once

/**
 * DecodeTable —— 译码表（SS-2 构件 2，不可变）
 *
 * 设计依据：6.4.3 / 6.3.3；档 2。实现 SS-1 定义的 IDecodeTable（SA-01）
 */

#include "core/idecode_table.hpp"
#include "isa/values.hpp"
#include <cstdint>
#include <vector>

namespace isa {

class DecodeTable : public IDecodeTable {
public:
    const Instruction& lookup(Enc enc);
    // O(1) 下标访问（M-08）
    unsigned width();
    // 指令宽度
    static DecodeTable build(const IsaSpec& spec);
    // 静态工厂

private:
    DecodeTable(const IsaSpec& spec, BitMask wide, std::vector<Instruction> rows);
    const IsaSpec spec_;  // 构建它的描述（保留供 width() 与审计）
    const BitMask wide_;  // 编码宽度位图
    const std::vector<Instruction> rows_;  // 直表；长度 1 << kMaxEncBits
};

}  // namespace isa
