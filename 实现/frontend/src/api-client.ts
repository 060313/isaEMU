/**
 * api-client.ts —— 后端 REST / WebSocket 客户端（AppShell 的私有依赖）
 *
 * 设计依据：《软件详细设计文档》6.4.6（HttpGateway / Router 的对外契约）与
 *           《用户界面设计文档》第 8 章（前端不直接持有领域对象）。
 */

import { OpKind } from './types';

export interface ApiEnvelope<T> {
  ok: boolean;
  data?: T;
  error?: { code: string; message: string };
}

export class ApiClient {
  constructor(private readonly baseUrl: string) {}

  // 统一调用入口：经 SS-6 的 HttpGateway → Router → 领域服务
  async call<T>(op: OpKind, payload: unknown): Promise<T> {
    // TODO: POST ${baseUrl}/api/${op} 并解包 ApiEnvelope
    throw new Error(`not implemented: ApiClient.call(${op})`);
  }

  // WebSocket：接收 JobState / ToastKind 等主动推送（FR-6.4）
  connect(onEvent: (kind: string, payload: unknown) => void): WebSocket {
    // TODO: new WebSocket(`${baseUrl}/ws`) 并注册 onEvent
    throw new Error('not implemented: ApiClient.connect');
  }
}
