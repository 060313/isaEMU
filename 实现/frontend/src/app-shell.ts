/**
 * app-shell.ts —— AppShell（SS-7 构件 1，UI-11）
 *
 * 设计依据：《软件详细设计文档》6.4.7；《用户界面设计文档》9.2（UI-11 为 11 个界面的共用外壳，
 *           不计为界面）。职责三合一：路由 / 全局状态 / API 客户端。
 * 刷新节流（NFR-Q3）落在 throttledRefresh：连续运行时合并刷新请求。
 */

import { ApiClient } from './api-client';
import { Credential, LoginResult, StepDelta, UiId } from './types';

export class AppShell {
  private token = '';
  private current: UiId = UiId.Ui01;
  private readonly api: ApiClient;

  constructor(baseUrl: string) {
    this.api = new ApiClient(baseUrl);
  }

  async login(cred: Credential): Promise<LoginResult> {
    // TODO: 经 api.call 调 ISessionService.login，成功后保存 token 并跳到 UI-02
    throw new Error('not implemented: AppShell.login');
  }

  logout(): void {
    // TODO: 调 ISessionService.logout，清空 token 并回到 UI-01
    throw new Error('not implemented: AppShell.logout');
  }

  async exec(op: string, payload: unknown): Promise<unknown> {
    // TODO: 按 op 分派到 ApiClient.call
    throw new Error(`not implemented: AppShell.exec(${op})`);
  }

  navigate(uiId: UiId, mode?: string): void {
    // TODO: 路由切换（28 条 J-xx 跳转）
    throw new Error(`not implemented: AppShell.navigate(${uiId}, ${mode})`);
  }

  throttledRefresh(): void {
    // TODO: 合并高频刷新请求（NFR-Q3 的响应性要求）
    throw new Error('not implemented: AppShell.throttledRefresh');
  }

  // 把执行增量应用到当前视图（SA-11）
  private applyDelta(delta: StepDelta): void {
    // TODO: 按 delta.writes 局部更新寄存器 / 内存视图
    throw new Error('not implemented: AppShell.applyDelta');
  }
}
