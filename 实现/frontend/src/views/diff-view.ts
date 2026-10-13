/**
 * DiffView.ts —— 视图（SS-7 构件）
 *
 * 设计依据：《软件详细设计文档》6.4.7；承载界面 UI-07、UI-08
 */

import { AppShell } from '../app-shell';
import { AttributionCategory } from '../types';

export class DiffView {
  constructor(private readonly shell: AppShell) {}

  async start(program: number, scope: number): Promise<void> {
    // TODO: → IDiffService.start
    throw new Error('not implemented: DiffView.start');
  }

  async cancel(jobId: string): Promise<void> {
    throw new Error('not implemented: DiffView.cancel');
  }

  // C-14：批量归因
  async annotate(divIds: number[], category: AttributionCategory, note: string): Promise<void> {
    throw new Error('not implemented: DiffView.annotate');
  }
}
