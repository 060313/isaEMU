/**
 * WorkspaceService —— 工作区服务（SS-5 构件 7）
 *
 * 设计依据：6.4.5；档 2。实现 IWorkspaceService
 */

#include "domain/workspace_service.hpp"

namespace isa {

WorkspaceService::WorkspaceService(IStore& store, SessionService& sess) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

Result<Version> WorkspaceService::save(SaveSelection sel) {
    // TODO: 实现 —— 选择性保存（事务 T-1）
    return Result<Version>::err(ErrCode::NotImplemented, "WorkspaceService::save");
}

Result<Workspace> WorkspaceService::load(WorkspaceId id) {
    // TODO: 实现 —— 加载工作区
    return Result<Workspace>::err(ErrCode::NotImplemented, "WorkspaceService::load");
}

std::vector<WorkspaceBrief> WorkspaceService::list(UserId u) {
    // TODO: 实现 —— 工作区列表
    return {};
}

Workspace WorkspaceService::pack(SaveSelection sel) {
    // TODO: 实现 —— 把会话现场打包为 Workspace
    return {};
}

Workspace WorkspaceService::unpack(const WorkspaceRow& row) {
    // TODO: 实现 —— 把持久化行还原为 Workspace
    return {};
}

}  // namespace isa
