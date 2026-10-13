/**
 * SessionView.ts —— 视图（SS-7 构件）
 *
 * 设计依据：《软件详细设计文档》6.4.7；承载界面 UI-01、UI-10
 */

import { AppShell } from '../app-shell';
import { Credential, LoginResult } from '../types';

export class SessionView {
  constructor(private readonly shell: AppShell) {}

  async onSubmit(): Promise<void> {
    // TODO: 收集表单 → AppShell.login
    throw new Error('not implemented: SessionView.onSubmit');
  }

  render(result: LoginResult): void {
    // TODO: 渲染登录结果
    throw new Error('not implemented: SessionView.render');
  }

  // C-17：危险操作二次确认
  confirmDangerous(action: string): boolean {
    // TODO: 弹出确认框
    throw new Error(`not implemented: SessionView.confirmDangerous(${action})`);
  }
}
