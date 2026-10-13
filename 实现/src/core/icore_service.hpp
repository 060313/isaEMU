#pragma once

/**
 * ICoreService —— 模拟执行内核的对外契约
 *
 * 设计依据：6.4.2；5.4「定义方 SS-1、实现方 EmulatorCore、调用方 SS-5/SS-6」
 */

#include "core/idecode_table.hpp"
#include "isa/values.hpp"
#include <cstdint>

namespace isa {

class ICoreService {
public:
    virtual ~ICoreService() = default;

    virtual void load(const Image& img, Addr base, const InitState& init) = 0;
    // 整体替换式装载
    virtual void attachDecodeTable(const IDecodeTable& dt) = 0;
    // 绑定译码表（可重复调用以切换 ISA）
    virtual StepDelta step(std::uint32_t n) = 0;
    // 执行 n 步；接口不带默认参数，默认值在 EmulatorCore 的声明里
    virtual RunResult run(RunMode m, Addr param, std::uint64_t limit, const CancelToken& tk) = 0;
    // 主循环（活动图①）
    virtual void pause() = 0;
    // 置 Paused；在下一次循环判定时生效
    virtual void reset() = 0;
    // 恢复装载初态；保留映像与译码表
    virtual RunState state() = 0;
    // 只读查询；不产生状态转移
    virtual StateSnapshot reads(ReadScope scope) = 0;
    // 取架构状态只读快照（R2：查询路径与执行路径分离）
    virtual void restore(const StateSnapshot& s) = 0;
    // 用快照覆盖 ArchState（R2 新增，UC-07 的回退落点）
};

}  // namespace isa
