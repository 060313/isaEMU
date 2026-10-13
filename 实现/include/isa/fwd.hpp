#pragma once

/**
 * 前向声明 —— 跨子系统引用（指针 / 引用成员与参数）的公共入口
 *
 * 设计依据：《软件详细设计文档》6.2.4「跨子系统的关联全部指向接口」
 * 说明：各构件的头文件只把「能力」声明为指针 / 引用，故前向声明足够；
 *       完整类型只在 .cpp 里引入。这使「仅相邻层依赖」（sad P5）在头文件层也成立。
 */

namespace isa {

// 契约接口
class ICoreService;
class IDecodeTable;
class IIsaProvider;
class ICompareService;
class IAssembler;
class IRefSim;
class ISessionService;
class IIsaService;
class ILoadService;
class IDebugService;
class ITestService;
class IDiffService;
class IWorkspaceService;
class IStore;
class IConfig;
class ILogger;
class IIdGen;
class IProcessRunner;

// SS-1 / SS-2 / SS-3 / SS-4
class ArchState;
class Trace;
class TerminationGuard;
class EmulatorCore;
class IsaLoader;
class DecodeTable;
class CompareEngine;
class DiffScope;
class Divergence;
class ToolchainAdapter;
class RefSimAdapter;

// SS-5 / SS-6 / SS-8
class SessionContext;
class BreakpointTable;
class SessionService;
class IsaService;
class LoadService;
class DebugService;
class TestService;
class DiffService;
class WorkspaceService;
class HttpGateway;
class Router;
class AccessGuard;
class Bootstrapper;
class DbDriver;
class DbStore;
class FileConfig;
class StdLogger;
class UuidGen;
class ProcRunner;

}  // namespace isa
