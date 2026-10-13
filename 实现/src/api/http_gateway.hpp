#pragma once

/**
 * HttpGateway —— HTTP / WebSocket 网关（SS-6 构件 1）
 *
 * 设计依据：6.4.6；档 2。UC-01 ~ UC-14 的统一入口
 */

#include "isa/values.hpp"
#include "api/router.hpp"
#include "api/access_guard.hpp"
#include <string>

namespace isa {

class HttpGateway {
public:
    HttpGateway(Router& router, AccessGuard& guard);

    HttpResponse handle(const HttpRequest& req);
    // 入口：拆为 unwrap + wrap 两段
    void push(WsSession& ws, const Event& e);
    // WebSocket 主动推送（FR-6.4）

private:
    Result<Payload> unwrap(const HttpRequest& req);
    // 解析请求体、校验 Schema
    HttpResponse wrap(const Result<Payload>& r);
    // 结果 / 错误统一封装
    Router* router_;  // 关联
    AccessGuard* guard_;  // 关联
};

}  // namespace isa
