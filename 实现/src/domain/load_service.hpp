#pragma once

/**
 * LoadService —— 装载服务（SS-5 构件 3）
 *
 * 设计依据：6.4.5；档 2。实现 ILoadService；D-7 的决策点在这里
 */

#include "domain/i_load_service.hpp"
#include "domain/session_service.hpp"
#include "adapt/iassembler.hpp"
#include "isa/values.hpp"
#include <vector>

namespace isa {

class LoadService : public ILoadService {
public:
    LoadService(IAssembler& asm_, IStore& store, SessionService& sess);

    Result<Image> assemble(const SourceRef& src);
    // 仅汇编（D-7）
    Result<LoadResult> loadProgram(const LoadSpec& s);
    // 汇编 + 装载
    std::vector<ExampleId> examples();
    // 内置示例

private:
    ICoreService* coreOf(Token t);
    // 经会话上下文取内核（D-3）
    IAssembler* asm_;  // 关联
    IStore* store_;  // 关联
    SessionService* sess_;  // 关联
};

}  // namespace isa
