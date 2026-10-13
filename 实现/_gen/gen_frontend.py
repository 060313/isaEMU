# -*- coding: utf-8 -*-
"""SS-7 前端骨架（TypeScript 5）—— 8 个构件与后端 API 客户端。"""
from render import ROOT, emit


def w(rel, text):
    emit("frontend/" + rel, text)


PKG = r'''{
  "name": "isa-sim-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "description": "ISA 模拟系统前端骨架（SS-7 / 8 个构件）",
  "scripts": {
    "build": "tsc -p tsconfig.json && node -e \"require('fs').cpSync('index.html','dist/index.html')\"",
    "typecheck": "tsc -p tsconfig.json --noEmit"
  },
  "devDependencies": {
    "typescript": "^5.4.0"
  }
}'''

TSCONFIG = r'''{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ES2020",
    "moduleResolution": "bundler",
    "lib": ["ES2020", "DOM"],
    "strict": true,
    "noImplicitOverride": true,
    // 骨架阶段刻意不开 noUnusedLocals / noUnusedParameters：
    // 空实现的形参本身就是「方法契约」的书面表达，参数未用属预期；
    // 二者不属于 strict，实现填充完成后可再开启。
    "outDir": "dist",
    "rootDir": "src",
    "sourceMap": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}'''

# 注意：tsc 只编译 .ts，不会把 index.html 一起搬进 dist/。
# 构建脚本（npm run build / Makefile 的 frontend / Dockerfile.edge）负责把它复制过去，
# 使 dist/ 成为自包含的「前端静态资源包」（SAD 6.1）——由 nginx 直接托管。
# 因此这里引用的是 ./main.js 而不是 ./dist/main.js。
INDEX_HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ISA 模拟系统</title>
</head>
<body>
  <!-- 应用外壳的唯一挂载点；12 个界面（UI-01 ~ UI-12）由 AppShell 路由切换 -->
  <div id="app"></div>
  <!-- 本文件会被复制进 dist/，与编译产物同级 -->
  <script type="module" src="./main.js"></script>
</body>
</html>'''

TYPES_TS = r'''/**
 * types.ts —— 前端镜像的类型（枚举与跨界面传递的数据）
 *
 * 设计依据：《软件详细设计文档》6.5.1（19 个枚举）与 6.5.2（值类型）；
 *           《用户界面设计文档》第 6 章（28 跳与携带数据）。
 * 说明：后端是类型的权威来源，此处只镜像前端用到的部分。
 */

// E-01 ~ E-19（后端枚举的前端镜像）
export enum RunState { NotReady = 'NotReady', Ready = 'Ready', Running = 'Running', Paused = 'Paused', Halted = 'Halted', Faulted = 'Faulted' }
export enum RunMode { Step = 'Step', RunN = 'RunN', UntilAddr = 'UntilAddr', ToBoundary = 'ToBoundary', Continue = 'Continue' }
export enum RunReason { HitLimit = 'HitLimit', Cancelled = 'Cancelled', Halted = 'Halted', Faulted = 'Faulted', ModeSatisfied = 'ModeSatisfied', NotReady = 'NotReady' }
export enum GuardVerdict { None = 'None', Halt = 'Halt', Fault = 'Fault' }
export enum FaultKind { IllegalInstruction = 'IllegalInstruction', MemAccessViolation = 'MemAccessViolation', MisalignedAccess = 'MisalignedAccess', UnknownCsr = 'UnknownCsr' }
export enum Field { Pc = 1, Gpr = 2, Mem = 4, Csr = 8 }
export enum DiffMode { Stepwise = 'Stepwise', Final = 'Final' }
export enum AttributionCategory { ImplDefect = 'ImplDefect', BaselineDeviation = 'BaselineDeviation', SpecAmbiguity = 'SpecAmbiguity' }
export enum BpOp { Add = 'Add', Remove = 'Remove', Toggle = 'Toggle', Enable = 'Enable', Disable = 'Disable', Clear = 'Clear', EnableAll = 'EnableAll', DisableAll = 'DisableAll' }
export enum SaveSelection { Program = 1, Suite = 2, Config = 4 }
export enum OpKind { Load = 'Load', Step = 'Step', Run = 'Run', Test = 'Test', Diff = 'Diff', Workspace = 'Workspace', User = 'User' }
export enum Level { Debug = 'Debug', Info = 'Info', Warn = 'Warn', Error = 'Error' }
export enum DriverKind { Postgres = 'Postgres', Sqlite = 'Sqlite' }
export enum JobState { Queued = 'Queued', Running = 'Running', Cancelled = 'Cancelled', Completed = 'Completed', Finalized = 'Finalized' }
export enum ToastKind { Success = 'Success', Warn = 'Warn', Error = 'Error', Info = 'Info' }
export enum Severity { Error = 'Error', Warn = 'Warn', Info = 'Info' }
export enum Role { User = 'User', Admin = 'Admin' }
export enum UserStatus { Active = 'Active', Disabled = 'Disabled' }

// E-15：12 个界面编号与 uid 阶段一一对应；跳转目标是枚举而不是裸字符串
export enum UiId {
  Ui01 = 'ui-01', Ui02 = 'ui-02', Ui03 = 'ui-03', Ui04 = 'ui-04',
  Ui05 = 'ui-05', Ui06 = 'ui-06', Ui07 = 'ui-07', Ui08 = 'ui-08',
  Ui09 = 'ui-09', Ui10 = 'ui-10', Ui11 = 'ui-11', Ui12 = 'ui-12',
}

// ---- 跨界面传递的数据（选择后端值类型中界面需要的一层）----
export interface Credential { username: string; secret: string }
export interface User { uid: number; name: string; role: Role; status: UserStatus }
export interface LoginResult { token: string; workspace: number; isa: string }
export interface WorkspaceBrief { wsId: number; name: string; version: number; updatedAt: string }
export interface SessionConfig { sp: number; instrLimit: number; traceOn: boolean }
export interface WriteOp { kind: string; index: number; oldValue: number; newValue: number; len: number }
export interface StepDelta { stepNo: number; pc: number; writes: WriteOp[]; reason: RunReason }
export interface RunResult { delta: StepDelta; reason: RunReason; steps: number }
export interface StateSnapshot { pc: number; gpr: number[]; csr: Array<[number, number]> }
export interface Issue { line: number; col: number; severity: Severity; code: string; message: string }
export interface FieldDiff { field: Field; index: number; valueA: number; valueB: number }
export interface Divergence {
  divId: number; jobId: string; stepNo: number; pc: number;
  fieldDiffs: FieldDiff[]; category?: AttributionCategory; note?: string;
}
export interface CaseResult { caseId: number; passed: boolean; firstDiffAt?: number; diffFields: FieldDiff[] }
export interface TestReport {
  reportId: number; suiteId: number; owner: number;
  startedAt: string; finishedAt: string; results: CaseResult[];
}
export interface ReportRow { reportId: number; suiteId: number; summary: string }
export interface Breakpoint { addr: number; op: BpOp; enabled: boolean }
'''

API_CLIENT_TS = r'''/**
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
'''

APP_SHELL_TS = r'''/**
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
'''

VIEWS = [
    ("session-view.ts", "SessionView", "UI-01、UI-10", """  async onSubmit(): Promise<void> {
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
  }"""),

    ("isa-view.ts", "IsaView", "UI-04", """  async upload(file: File): Promise<void> {
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
  }"""),

    ("load-view.ts", "LoadView", "UI-03、UI-12", """  async submit(src: string, base: number, init: SessionConfig): Promise<void> {
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
  }"""),

    ("debug-view.ts", "DebugView", "UI-02（主界面）", """  async execute(mode: RunMode, param: number, n: number): Promise<void> {
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
  }"""),

    ("test-view.ts", "TestView", "UI-05、UI-06", """  async run(suiteId: number, mode: DiffMode): Promise<void> {
    // TODO: → ITestService.runSuite
    throw new Error('not implemented: TestView.run');
  }

  renderReport(report: TestReport): void {
    throw new Error('not implemented: TestView.renderReport');
  }

  // C-13：跨用例复用 —— 在调试工作台中复现
  async reproduceInDebug(caseId: number): Promise<void> {
    throw new Error('not implemented: TestView.reproduceInDebug');
  }"""),

    ("diff-view.ts", "DiffView", "UI-07、UI-08", """  async start(program: number, scope: number): Promise<void> {
    // TODO: → IDiffService.start
    throw new Error('not implemented: DiffView.start');
  }

  async cancel(jobId: string): Promise<void> {
    throw new Error('not implemented: DiffView.cancel');
  }

  // C-14：批量归因
  async annotate(divIds: number[], category: AttributionCategory, note: string): Promise<void> {
    throw new Error('not implemented: DiffView.annotate');
  }"""),

    ("workspace-view.ts", "WorkspaceView", "UI-09", """  async save(selection: SaveSelection): Promise<void> {
    // TODO: → IWorkspaceService.save
    throw new Error('not implemented: WorkspaceView.save');
  }

  async load(id: number): Promise<void> {
    throw new Error('not implemented: WorkspaceView.load');
  }

  async list(): Promise<WorkspaceBrief[]> {
    throw new Error('not implemented: WorkspaceView.list');
  }"""),
]

VIEW_IMPORT = {
    "session-view.ts": "Credential, LoginResult",
    "isa-view.ts": "Issue",
    "load-view.ts": "SessionConfig",
    "debug-view.ts": "RunMode",
    "test-view.ts": "DiffMode, TestReport",
    "diff-view.ts": "AttributionCategory",
    "workspace-view.ts": "SaveSelection, WorkspaceBrief",
}

MAIN_TS = r'''/**
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
'''


def gen_frontend():
    w("package.json", PKG)
    w("tsconfig.json", TSCONFIG)
    w("index.html", INDEX_HTML)
    w("src/types.ts", TYPES_TS)
    w("src/api-client.ts", API_CLIENT_TS)
    w("src/app-shell.ts", APP_SHELL_TS)

    for fname, cls, ui, body in VIEWS:
        imp = VIEW_IMPORT[fname]
        text = ("/**\n"
                " * %s.ts —— %s（SS-7 构件）\n"
                " *\n"
                " * 设计依据：《软件详细设计文档》6.4.7；承载界面 %s\n"
                " */\n\n"
                "import { AppShell } from '../app-shell';\n"
                "import { %s } from '../types';\n\n"
                "export class %s {\n"
                "  constructor(private readonly shell: AppShell) {}\n\n"
                "%s\n"
                "}\n") % (cls, "视图", ui, imp, cls, body)
        w("src/views/" + fname, text)

    w("src/main.ts", MAIN_TS)
