/**
 * LoadService —— 装载服务（SS-5 构件 3）
 *
 * 设计依据：6.4.5；档 2。实现 ILoadService；D-7 的决策点在这里
 */

#include "domain/load_service.hpp"

namespace isa {

LoadService::LoadService(IAssembler& asm_, IStore& store, SessionService& sess) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

Result<Image> LoadService::assemble(const SourceRef& src) {
    // TODO: 实现 —— 仅汇编（D-7）
    return Result<Image>::err(ErrCode::NotImplemented, "LoadService::assemble");
}

Result<LoadResult> LoadService::loadProgram(const LoadSpec& s) {
    // TODO: 实现 —— 汇编 + 装载
    return Result<LoadResult>::err(ErrCode::NotImplemented, "LoadService::loadProgram");
}

std::vector<ExampleId> LoadService::examples() {
    // TODO: 实现 —— 内置示例
    return {};
}

ICoreService* LoadService::coreOf(Token t) {
    // TODO: 实现 —— 经会话上下文取内核（D-3）
    return {};
}

}  // namespace isa
