/**
 * ToolchainAdapter —— 工具链适配器（SS-4 构件 1）
 *
 * 设计依据：6.4.5；档 2。隔离外部工具链
 */

#include "adapt/toolchain_adapter.hpp"

namespace isa {

ToolchainAdapter::ToolchainAdapter(const IProcessRunner& runner, const IConfig& cfg) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

Result<Image> ToolchainAdapter::assemble(const SourceRef& src, const CancelToken& tk) {
    // TODO: 实现 —— 汇编
    return Result<Image>::err(ErrCode::NotImplemented, "ToolchainAdapter::assemble");
}

Result<Image> ToolchainAdapter::assembleWith(std::string_view args) {
    // TODO: 实现 —— 带参数调用子进程
    return Result<Image>::err(ErrCode::NotImplemented, "ToolchainAdapter::assembleWith");
}

std::vector<Issue> ToolchainAdapter::parseDiagnostics(std::string_view text) {
    // TODO: 实现 —— 解析工具链诊断
    return {};
}

}  // namespace isa
