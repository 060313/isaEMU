#pragma once

/**
 * IWorkspaceService —— 工作区服务契约
 *
 * 设计依据：6.4.2；UC-12
 */

#include "domain/session_context.hpp"
#include "isa/domain_types.hpp"
#include "isa/values.hpp"
#include "core/idecode_table.hpp"
#include "core/icore_service.hpp"
#include <optional>
#include <vector>

namespace isa {

class IWorkspaceService {
public:
    virtual ~IWorkspaceService() = default;

    virtual Result<Version> save(SaveSelection sel) = 0;
    // 选择性保存
    virtual Result<Workspace> load(WorkspaceId id) = 0;
    // 加载工作区
    virtual std::vector<WorkspaceBrief> list(UserId u) = 0;
    // 工作区列表（UI-09）
};

}  // namespace isa
