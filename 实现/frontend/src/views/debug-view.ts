/**
 * DebugView.ts —— 视图（SS-7 构件）
 *
 * 设计依据：《软件详细设计文档》6.4.7；承载界面 UI-02（主界面）
 */

import { AppShell } from '../app-shell';
import { RunMode } from '../types';

export class DebugView {
  constructor(private readonly shell: AppShell) {}

  async execute(mode: RunMode, param: number, n: number): Promise<void> {
    // TODO: → IDebugService.execute
    throw new Error('not implemented: DebugView.execute');
  }

  async readState(scope: string): Promise<void> {
    throw new Error('not implemented: DebugView.readState');
  }

  async rollback(step: number): Promise<void> {
    throw new Error('not implemented: DebugView.rollback');
  }

  // C-05 快捷键仅界面侧，不影响领域服务
  onShortcut(k: string): void {
    throw new Error(`not implemented: DebugView.onShortcut(${k})`);
  }

  private renderViews(): void {
    throw new Error('not implemented: DebugView.renderViews');
  }
}
