/**
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
