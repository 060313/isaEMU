#pragma once

/**
 * ToolchainAdapter —— 工具链适配器（SS-4 构件 1）
 *
 * 设计依据：6.4.5；档 2。隔离外部工具链
 */

#include "adapt/iassembler.hpp"
#include "isa/domain_types.hpp"
#include "isa/values.hpp"
#include <string>

namespace isa {

class ToolchainAdapter : public IAssembler {
public:
    explicit ToolchainAdapter(const IProcessRunner& runner, const IConfig& cfg);

    Result<Image> assemble(const SourceRef& src, const CancelToken& tk);
    // 汇编

private:
    Result<Image> assembleWith(std::string_view args);
    // 带参数调用子进程
    std::vector<Issue> parseDiagnostics(std::string_view text);
    // 解析工具链诊断
    const IProcessRunner* runner_;  // 关联
    const IConfig* cfg_;  // 关联；取 toolchainPath()
};

}  // namespace isa
