#pragma once

/**
 * IDiffService —— 对拍服务契约
 *
 * 设计依据：6.4.2；UC-10 / UC-11
 */

#include "domain/session_context.hpp"
#include "isa/domain_types.hpp"
#include "isa/values.hpp"
#include "core/idecode_table.hpp"
#include "core/icore_service.hpp"
#include <optional>
#include <vector>

namespace isa {

class IDiffService {
public:
    virtual ~IDiffService() = default;

    virtual Result<JobHandle> start(const DiffRequest& req, const CancelToken& tk) = 0;
    // 发起对拍（M-14）
    virtual Result<Divergence> diffDetail(DivergenceId id) = 0;
    // 分歧详情
    virtual Result<void> annotate(span<const DivergenceId> ids, AttributionCategory cat, std::string note) = 0;
    // 批量归因（C-14）
    virtual bool degrade() = 0;
    // 参考方降级状态
};

}  // namespace isa
