/**
 * Router —— 请求路由分发（SS-6 构件 2）
 *
 * 设计依据：6.4.6；档 2。UC-13
 */

#include "api/router.hpp"

namespace isa {

Result<Payload> Router::route(const RouteKey& key, const Params& params) {
    // TODO: 实现 —— 查表分发并绑定参数
    return Result<Payload>::err(ErrCode::NotImplemented, "Router::route");
}

Result<Bound> Router::bind(const Schema& schema, const Params& params) {
    // TODO: 实现 —— 参数绑定与类型校验
    return Result<Bound>::err(ErrCode::NotImplemented, "Router::bind");
}

}  // namespace isa
