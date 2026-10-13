#pragma once

/**
 * DiffService —— 对拍服务（SS-5 构件 6）
 *
 * 设计依据：6.4.5；档 2。实现 IDiffService；任务在批次边界退出（M-14）
 */

#include "domain/i_diff_service.hpp"
#include "domain/session_service.hpp"
#include "compare/icompare_service.hpp"
#include "adapt/iref_sim.hpp"
#include "isa/values.hpp"
#include <map>

namespace isa {

class DiffService : public IDiffService {
public:
    DiffService(SessionService& sess, IRefSim& ref, ICompareService& cmp, IStore& store);

    Result<JobHandle> start(const DiffRequest& req, const CancelToken& tk);
    // 发起对拍
    Result<Divergence> diffDetail(DivergenceId id);
    // 分歧详情
    Result<void> annotate(span<const DivergenceId> ids, AttributionCategory cat, std::string note);
    // 批量归因
    bool degrade();
    // 参考方降级

private:
    std::vector<StepRecord> driveCore(const Program& p, const CancelToken& tk);
    // 驱动内核侧
    std::vector<StepRecord> driveRef(const Program& p, const CancelToken& tk);
    // 驱动参考方
    Result<JobEntry&> jobOf(JobId j);
    // 取任务条目
    SessionService* sess_;  // 关联
    IRefSim* ref_;  // 关联
    ICompareService* cmp_;  // 关联
    IStore* store_;  // 关联
    std::map<JobId, JobEntry> jobs_;  // 在跑的任务
};

}  // namespace isa
