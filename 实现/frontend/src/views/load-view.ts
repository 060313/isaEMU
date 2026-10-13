/**
 * LoadView.ts —— 视图（SS-7 构件）
 *
 * 设计依据：《软件详细设计文档》6.4.7；承载界面 UI-03、UI-12
 */

import { AppShell } from '../app-shell';
import { SessionConfig } from '../types';

export class LoadView {
  constructor(private readonly shell: AppShell) {}

  async submit(src: string, base: number, init: SessionConfig): Promise<void> {
    // TODO: 装载程序 → ILoadService.loadProgram
    throw new Error('not implemented: LoadView.submit');
  }

  preview(disasm: string[]): void {
    // TODO: 渲染反汇编预览
    throw new Error('not implemented: LoadView.preview');
  }

  async loadExample(id: string): Promise<void> {
    // TODO: 载入内置示例
    throw new Error('not implemented: LoadView.loadExample');
  }
}
