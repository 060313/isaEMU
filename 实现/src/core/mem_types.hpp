#pragma once

/**
 * 内核内部内存与 CSR 类型（档 3）
 *
 * 设计依据：6.3.3 ArchState 的属性类型；不被跨子系统引用
 * 骨架：CsrFile / MemImage 为 ArchState 的内部结构，不参与跨子系统传递
 */

#include "isa/values.hpp"
#include <cstdint>
#include <map>
#include <vector>

namespace isa {

// Page —— 一页内存（稀疏分配，不预分配整段地址空间）
struct Page {
    static constexpr std::size_t kSize = 4096;
    std::vector<std::uint8_t> bytes;  // 长度为 kSize
};

// MemImage —— 稀疏页内存（NFR-Q5 内存用量受控的落点）
class MemImage {
public:
    std::uint8_t readByte(Addr a) const;              // 未写过处读 0
    void writeByte(Addr a, std::uint8_t v);
    MemView view() const;                             // 快照用只读视图
private:
    std::map<PageNo, Page> pages_;  // 按需分配
};

// CsrFile —— CSR 稀疏封装（4096 项）
class CsrFile {
public:
    Word read(CsrId id) const;
    void write(CsrId id, Word v);
    std::vector<std::pair<CsrId, Word>> touched() const;  // 已写过的项（快照用）
private:
    std::map<CsrId, Word> regs_;
};

// WriteOpList —— 一步产生的全部写操作（EmulatorCore::cycle 的产出类型）
using WriteOpList = std::vector<WriteOp>;

}  // namespace isa
