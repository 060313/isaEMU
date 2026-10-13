/**
 * DiffService —— 对拍服务（SS-5 构件 6）
 *
 * 设计依据：6.4.5；档 2。实现 IDiffService；任务在批次边界退出（M-14）
 */

#include "domain/diff_service.hpp"

namespace isa {

DiffService::DiffService(SessionService& sess, IRefSim& ref, ICompareService& cmp, IStore& store) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

Result<JobHandle> DiffService::start(const DiffRequest& req, const CancelToken& tk) {
    // TODO: 实现 —— 发起对拍
    return Result<JobHandle>::err(ErrCode::NotImplemented, "DiffService::start");
}

Result<Divergence> DiffService::diffDetail(DivergenceId id) {
    // TODO: 实现 —— 分歧详情
    return Result<Divergence>::err(ErrCode::NotImplemented, "DiffService::diffDetail");
}

Result<void> DiffService::annotate(span<const DivergenceId> ids, AttributionCategory cat, std::string note) {
    // TODO: 实现 —— 批量归因
    return Result<void>::err(ErrCode::NotImplemented, "DiffService::annotate");
}

bool DiffService::degrade() {
    // TODO: 实现 —— 参考方降级
    return false;
}

std::vector<StepRecord> DiffService::driveCore(const Program& p, const CancelToken& tk) {
    // TODO: 实现 —— 驱动内核侧
    return {};
}

std::vector<StepRecord> DiffService::driveRef(const Program& p, const CancelToken& tk) {
    // TODO: 实现 —— 驱动参考方
    return {};
}

Result<JobEntry&> DiffService::jobOf(JobId j) {
    // TODO: 实现 —— 取任务条目
    return Result<JobEntry&>::err(ErrCode::NotImplemented, "DiffService::jobOf");
}

}  // namespace isa
