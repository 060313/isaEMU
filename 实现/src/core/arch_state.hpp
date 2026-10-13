#pragma once

/**
 * ArchState —— 架构状态（SS-1 构件 2）
 *
 * 设计依据：6.4.1 / 6.3.3；档 2（装配可见）
 */

#include "core/mem_types.hpp"
#include "isa/values.hpp"
#include <array>
#include <cstdint>

namespace isa {

class ArchState {
public:
    void apply(span<const WriteOp> writes);
    // 差分写回；写 x0 被丢弃（M-03）
    StateSnapshot snapshot(ReadScope scope);
    // 取只读快照
    void restore(const StateSnapshot& s);
    // 仅 EmulatorCore 调用
    Bytes read(Addr a, std::size_t n);
    // 内存读
    void write(Addr a, span<const std::uint8_t> bytes);
    // 内存写
    void reset(const InitState& init);
    // 恢复初态

private:
    Addr pc_;  // 程序计数器
    std::array<Word, 32> gpr_;  // 32 个通用寄存器（含 x0）
    CsrFile csr_;  // CSR 稀疏封装
    MemImage mem_;  // 稀疏页内存；空表示未写过处读 0
};

}  // namespace isa
