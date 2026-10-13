/**
 * WorkspaceView.ts —— 视图（SS-7 构件）
 *
 * 设计依据：《软件详细设计文档》6.4.7；承载界面 UI-09
 */

import { AppShell } from '../app-shell';
import { SaveSelection, WorkspaceBrief } from '../types';

export class WorkspaceView {
  constructor(private readonly shell: AppShell) {}

  async save(selection: SaveSelection): Promise<void> {
    // TODO: → IWorkspaceService.save
    throw new Error('not implemented: WorkspaceView.save');
  }

  async load(id: number): Promise<void> {
    throw new Error('not implemented: WorkspaceView.load');
  }

  async list(): Promise<WorkspaceBrief[]> {
    throw new Error('not implemented: WorkspaceView.list');
  }
}
