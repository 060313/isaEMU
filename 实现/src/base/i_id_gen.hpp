#pragma once

/**
 * IIdGen —— 标识生成契约（SS-8）
 *
 * 设计依据：6.4.8；数据设计总则 G-2：业务标识由 IIdGen 生成，不依赖数据库自增
 */

#include "isa/values.hpp"

namespace isa {

class IIdGen {
public:
    virtual ~IIdGen() = default;

    virtual Token newToken() = 0;
    virtual WorkspaceId newWorkspaceId() = 0;
    virtual DivergenceId newDivergenceId() = 0;
    virtual JobId newJobId() = 0;
};

}  // namespace isa
