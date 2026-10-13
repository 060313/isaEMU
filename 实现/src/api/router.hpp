#pragma once

/**
 * Router —— 请求路由分发（SS-6 构件 2）
 *
 * 设计依据：6.4.6；档 2。UC-13
 */

#include "isa/values.hpp"
#include <string>

namespace isa {

class Router {
public:
    Result<Payload> route(const RouteKey& key, const Params& params);
    // 查表分发并绑定参数

private:
    Result<Bound> bind(const Schema& schema, const Params& params);
    // 参数绑定与类型校验
    std::map<RouteKey, std::string> table_;  // 路由表（骨架：键 → 处理器标识）
};

}  // namespace isa
