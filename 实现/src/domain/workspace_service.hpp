#pragma once

/**
 * WorkspaceService —— 工作区服务（SS-5 构件 7）
 *
 * 设计依据：6.4.5；档 2。实现 IWorkspaceService
 */

#include "domain/i_workspace_service.hpp"
#include "domain/session_service.hpp"
#include "isa/values.hpp"
#include <vector>

namespace isa {

class WorkspaceService : public IWorkspaceService {
public:
    WorkspaceService(IStore& store, SessionService& sess);

    Result<Version> save(SaveSelection sel);
    // 选择性保存（事务 T-1）
    Result<Workspace> load(WorkspaceId id);
    // 加载工作区
    std::vector<WorkspaceBrief> list(UserId u);
    // 工作区列表

private:
    Workspace pack(SaveSelection sel);
    // 把会话现场打包为 Workspace
    Workspace unpack(const WorkspaceRow& row);
    // 把持久化行还原为 Workspace
    IStore* store_;  // 关联
    SessionService* sess_;  // 关联
};

}  // namespace isa
