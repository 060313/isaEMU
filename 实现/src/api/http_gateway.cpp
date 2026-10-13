/**
 * HttpGateway —— HTTP / WebSocket 网关（SS-6 构件 1）
 *
 * 设计依据：6.4.6；档 2。UC-01 ~ UC-14 的统一入口
 */

#include "api/http_gateway.hpp"

namespace isa {

HttpGateway::HttpGateway(Router& router, AccessGuard& guard) {
    // TODO: 构造（注入依赖 / 建立组合成员）
}

HttpResponse HttpGateway::handle(const HttpRequest& req) {
    // TODO: 实现 —— 入口：拆为 unwrap + wrap 两段
    return {};
}

void HttpGateway::push(WsSession& ws, const Event& e) {
    // TODO: 实现 —— WebSocket 主动推送（FR-6.4）
    (void)this;
}

Result<Payload> HttpGateway::unwrap(const HttpRequest& req) {
    // TODO: 实现 —— 解析请求体、校验 Schema
    return Result<Payload>::err(ErrCode::NotImplemented, "HttpGateway::unwrap");
}

HttpResponse HttpGateway::wrap(const Result<Payload>& r) {
    // TODO: 实现 —— 结果 / 错误统一封装
    return {};
}

}  // namespace isa
