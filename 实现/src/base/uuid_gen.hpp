#pragma once

/**
 * UuidGen —— 标识生成实现（SS-8）
 *
 * 设计依据：6.4.8
 */

#include "base/i_id_gen.hpp"
#include "isa/values.hpp"

namespace isa {

class UuidGen : public IIdGen {
public:
    Token newToken();
    WorkspaceId newWorkspaceId();
    DivergenceId newDivergenceId();
    JobId newJobId();
};

}  // namespace isa
