#pragma once

/**
 * Bootstrapper —— 组合根（SS-6 构件 4）
 *
 * 设计依据：6.4.6；SA-08。全项目唯一出现 new 的地方
 * Container 是组合根的产出物：装配完成的各构件引用。
 */

#include "isa/values.hpp"
#include <memory>

namespace isa {

class IStore;
class ILogger;
class IConfig;
class SessionService;
class HttpGateway;

// Container —— 装配结果（骨架：只列关键构件，实现时补齐）
struct Container {
    std::unique_ptr<IStore> store;
    std::unique_ptr<SessionService> sessions;
    std::unique_ptr<HttpGateway> gateway;
};

// Bootstrapper —— 组合根
// 约束：全项目只有此处与 SessionContext 的构造出现 new（可用 grep -n "new " src/ 在 CI 里强制）
class Bootstrapper {
public:
    static Container build(const IConfig& cfg);
};

}  // namespace isa
