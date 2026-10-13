#pragma once

/**
 * IsaLoader —— 描述装载与校验（SS-2 构件 1）
 *
 * 设计依据：6.4.3；档 2
 */

#include "isa/iisa_provider.hpp"
#include "isa/decode_table.hpp"
#include "core/idecode_table.hpp"
#include "isa/values.hpp"
#include <vector>

namespace isa {

class IsaLoader : public IIsaProvider {
public:
    Result<IsaSpec> load(const SourceRef& src);
    // 解析
    std::vector<Issue> validate(const IsaSpec& spec);
    // 三段校验
    const IDecodeTable& buildDecodeTable(const IsaSpec& spec);
    // 构建并缓存译码表
    std::vector<IsaSpec> available();
    // 内置描述

private:
    std::vector<Issue> threeStage(const IsaSpec& spec);
    // 三段：完备性 / 寄存器定义 / 编码域自洽（M-07）
    std::optional<IsaSpec> active_;  // 最近一次装载（仅作提示，不是「当前 ISA」的权威）
    std::unique_ptr<DecodeTable> table_;  // 已构建的译码表（组合）
};

}  // namespace isa
