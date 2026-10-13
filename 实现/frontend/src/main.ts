/**
 * main.ts —— 前端入口
 *
 * 设计依据：《用户界面设计文档》9.2（AppShell 为共用容器，主界面 = UI-02 调试工作台）
 */

import { AppShell } from './app-shell';
import { UiId } from './types';

const shell = new AppShell('http://localhost:8080');

// TODO: 按登录态决定首屏（未登录 → UI-01，已登录 → UI-02）
shell.navigate(UiId.Ui01);

export { shell };
