/**
 * DecodeTable —— 译码表（SS-2 构件 2，不可变）
 *
 * 设计依据：6.4.3 / 6.3.3；档 2。实现 SS-1 定义的 IDecodeTable（SA-01）
 */

#include "isa/decode_table.hpp"

namespace isa {

const Instruction& DecodeTable::lookup(Enc enc) {
    // TODO: 返回 rows_[enc & kMask]；骨架返回静态占位
    static const Instruction kEmpty{};
    return kEmpty;
}

unsigned DecodeTable::width() {
    // TODO: 实现 —— 指令宽度
    return {};
}

DecodeTable DecodeTable::build(const IsaSpec& spec) {
    // TODO: 构建直表
    return DecodeTable(spec, BitMask{}, std::vector<Instruction>{});
}

DecodeTable::DecodeTable(const IsaSpec& spec, BitMask wide, std::vector<Instruction> rows)
    : spec_(spec), wide_(wide), rows_(std::move(rows)) {}

}  // namespace isa
