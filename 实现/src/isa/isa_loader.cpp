/**
 * IsaLoader —— 描述装载与校验（SS-2 构件 1）
 *
 * 设计依据：6.4.3；档 2
 */

#include "isa/isa_loader.hpp"

namespace isa {

Result<IsaSpec> IsaLoader::load(const SourceRef& src) {
    // TODO: 实现 —— 解析
    return Result<IsaSpec>::err(ErrCode::NotImplemented, "IsaLoader::load");
}

std::vector<Issue> IsaLoader::validate(const IsaSpec& spec) {
    // TODO: 实现 —— 三段校验
    return {};
}

const IDecodeTable& IsaLoader::buildDecodeTable(const IsaSpec& spec) {
    // TODO: 构建并缓存译码表
    return *table_;
}

std::vector<IsaSpec> IsaLoader::available() {
    // TODO: 实现 —— 内置描述
    return {};
}

std::vector<Issue> IsaLoader::threeStage(const IsaSpec& spec) {
    // TODO: 实现 —— 三段：完备性 / 寄存器定义 / 编码域自洽（M-07）
    return {};
}

}  // namespace isa
