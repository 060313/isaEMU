#pragma once

/**
 * IIsaProvider —— ISA 描述的装载与校验契约
 *
 * 设计依据：6.4.2；5.4「定义方 SS-2、实现方 IsaLoader」
 */

#include "isa/values.hpp"
#include <vector>

namespace isa {

class IIsaProvider {
public:
    virtual ~IIsaProvider() = default;

    virtual Result<IsaSpec> load(const SourceRef& src) = 0;
    // 解析描述
    virtual std::vector<Issue> validate(const IsaSpec& spec) = 0;
    // 三段校验（M-07）
    virtual const IDecodeTable& buildDecodeTable(const IsaSpec& spec) = 0;
    // 构建译码表
    virtual std::vector<IsaSpec> available() = 0;
    // 内置描述列表
};

}  // namespace isa
