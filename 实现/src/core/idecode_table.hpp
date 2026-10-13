#pragma once

/**
 * IDecodeTable —— 译码表契约（SA-01 依赖倒置：由内核侧定义、ISA 抽象层实现）
 *
 * 设计依据：6.4.2；5.4 表
 */

#include "isa/values.hpp"
#include <cstdint>

namespace isa {

class IDecodeTable {
public:
    virtual ~IDecodeTable() = default;

    virtual const Instruction& lookup(Enc enc) = 0;
    // O(1) 下标访问
    virtual unsigned width() = 0;
    // 一条指令的字节宽度
};

}  // namespace isa
