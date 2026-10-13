/**
 * TestView.ts —— 视图（SS-7 构件）
 *
 * 设计依据：《软件详细设计文档》6.4.7；承载界面 UI-05、UI-06
 */

import { AppShell } from '../app-shell';
import { DiffMode, TestReport } from '../types';

export class TestView {
  constructor(private readonly shell: AppShell) {}

  async run(suiteId: number, mode: DiffMode): Promise<void> {
    // TODO: → ITestService.runSuite
    throw new Error('not implemented: TestView.run');
  }

  renderReport(report: TestReport): void {
    throw new Error('not implemented: TestView.renderReport');
  }

  // C-13：跨用例复用 —— 在调试工作台中复现
  async reproduceInDebug(caseId: number): Promise<void> {
    throw new Error('not implemented: TestView.reproduceInDebug');
  }
}
