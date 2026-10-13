/**
 * IsaView.ts —— 视图（SS-7 构件）
 *
 * 设计依据：《软件详细设计文档》6.4.7；承载界面 UI-04
 */

import { AppShell } from '../app-shell';
import { Issue } from '../types';

export class IsaView {
  constructor(private readonly shell: AppShell) {}

  async upload(file: File): Promise<void> {
    // TODO: 上传 ISA 描述 → IIsaService.loadSpec
    throw new Error('not implemented: IsaView.upload');
  }

  renderIssues(issues: Issue[]): void {
    // TODO: 渲染校验问题列表
    throw new Error('not implemented: IsaView.renderIssues');
  }

  // C-10：重新校验入口
  async revalidate(): Promise<void> {
    throw new Error('not implemented: IsaView.revalidate');
  }
}
