# ISA 模拟系统 —— 实现骨架

本目录是《软件详细设计文档》的**代码落地骨架**：8 个子系统 / 35 个构件的目录结构、头文件契约与空实现全部就位，能编译、能链接、能通过类型检查，但业务逻辑尚未填充。

- 设计依据：《软件体系结构设计文档》（`../软件设计-v2/软件体系结构设计文档.md`）、《软件详细设计文档》（`../软件设计-v2/详细设计/软件详细设计文档.md》）、《用户界面设计文档》（`../软件设计-v2/用户界面设计文档.md`）
- 语言与版本：后端 C++17、前端 TypeScript 5（类设计 G-1）
- 完成度：**可编译空骨架**（不含业务逻辑）

---

## 一、目录结构

```
实现/
├── CMakeLists.txt              三个目标：isa_kernel（静态库）/ isa_server（静态库）/ isa_sim（可执行）
├── Makefile                    便捷构建入口（cmake 优先，无 cmake 时走 g++ 直编兜底；见第三节）
├── docker-compose.yml          云端形态「单机三容器」编排（见第三节）
├── .dockerignore               容器构建上下文裁剪
├── config.example.toml         本地形态配置示例（IConfig 九项 + db.path）
├── .env.example                云端形态环境变量示例（compose 用）
├── README.md                   本文件
├── _gen/                       代码生成器与 DDL 自检脚本（Python，见第五节）
├── include/isa/                跨子系统公共类型层（8 个头）
├── src/                        后端 SS-1 ~ SS-6、SS-8（74 个文件）
├── frontend/                   SS-7 前端（14 个文件）
├── schema/                     双形态 DDL（SQLite / PostgreSQL 同源）
├── docker/                     三个镜像的定义：Dockerfile.{edge,app,db} + nginx.conf
├── third_party/                第三方依赖清单与许可证归档（NFR-C4，见 3.4）
└── tests/smoke_test.cpp        冒烟测试（只覆盖三类已实现的语义）
```

> 仓库根另有 `软件工程/.gitignore`（忽略规则设计见 3.5），与 `需求分析/`、`软件设计-v2/` 同级共享。

### 1.1 子系统 → 目录映射（35 个构件）

| 子系统 | 层 | 构件数 | 目录 | 构件 |
| --- | --- | --- | --- | --- |
| SS-1 模拟执行内核 | L1 | 4 | `src/core/` | `EmulatorCore`、`ArchState`、`Trace`、`TerminationGuard`（另**定义** `IDecodeTable`） |
| SS-2 ISA 抽象 | L2 | 2 | `src/isa/` | `IsaLoader`、`DecodeTable`（实现 SS-1 定义的 `IDecodeTable`） |
| SS-3 比对 | L3 | 3 | `src/compare/` + `include/isa/compare_types.hpp` | `CompareEngine`、`DiffScope`、`Divergence` |
| SS-4 适配 | 跨层 | 2 | `src/adapt/` | `ToolchainAdapter`、`RefSimAdapter` |
| SS-5 领域服务 | L3 | 7 | `src/domain/` | `SessionService`、`IsaService`、`LoadService`、`DebugService`、`TestService`、`DiffService`、`WorkspaceService` |
| SS-6 集成 API | L3 | 4 | `src/api/` | `HttpGateway`、`Router`、`AccessGuard`、`Bootstrapper` |
| SS-7 前端 | L4 | 8 | `frontend/src/` | `AppShell` + `SessionView`、`IsaView`、`LoadView`、`DebugView`、`TestView`、`DiffView`、`WorkspaceView` |
| SS-8 基础服务 | 跨层 | 5 | `src/base/` | `IStore`、`IConfig`、`ILogger`、`IIdGen`、`IProcessRunner` |
| | | **35** | | |

**构件内部类**（按类设计 5.5 口径，**不计入 35**）：SS-5 的 `SessionContext`、`BreakpointTable`（`src/domain/`），SS-8 的 `DbStore`、`FileConfig`、`StdLogger`、`UuidGen`、`ProcRunner`（`src/base/`）。它们分别是 7 个领域服务与 5 个基础接口的实现体，属装配可见（档 2）。

### 1.2 `include/isa/` —— 公共类型层

| 文件 | 内容 | 设计出处 |
| --- | --- | --- |
| `span.hpp` | 最小 `isa::span<T>`（C++17 无 `std::span`） | SAD 5.1.4 |
| `result.hpp` | `ErrCode`（10 值）、`Err`、`Result<T>` / `Result<T&>` / `Result<void>` | 类设计 G-6 |
| `fwd.hpp` | 48 个前向声明，用于切开跨子系统头文件依赖 | 类设计 P2 |
| `aliases.hpp` | 26 个别名（20 个设计别名 + 6 个骨架补充） | 详细设计 6.5.2 |
| `enums.hpp` | 23 个枚举（E-01 ~ E-19 + 4 个骨架补充） | 详细设计 6.5.1 |
| `values.hpp` | 55 个结构型类型（52 个由分组数据表生成 + `CancelToken`/`JobHandle`/`JobEntry`）+ `WsId` 别名 | 详细设计 6.5.2 |
| `compare_types.hpp` | `DiffScope` / `Divergence` | 见下方说明 |
| `domain_types.hpp` | `Program` / `TestCase` / `TestSuite` / `TestReport` / `Workspace` 等 | 见下方说明 |

> `compare_types.hpp` 与 `domain_types.hpp` 之所以放在公共层：`DiffScope` / `Divergence` 同时被 SS-3 的 `ICompareService` 与 SS-8 的 `IStore` 引用，`Program` 同时被 SS-4 的 `IRefSim` 与 SS-3 的 `DiffRequest` 引用。若放进 `src/` 下某子系统目录，会让另一个子系统反向依赖它 —— 违反 SAD「仅相邻层依赖、禁止反向依赖」的硬规则。

### 1.3 `frontend/`

```
frontend/
├── package.json       scripts: build / typecheck
├── tsconfig.json      strict: true（刻意不开 noUnusedLocals / noUnusedParameters，见文件内注释）
├── index.html         唯一挂载点 #app
└── src/
    ├── types.ts       19 个枚举的前端镜像 + UiId（12 值与 ui-xx 一一对应）+ 16 个 interface
    ├── api-client.ts   ApiClient.call<T>(op, payload) / connect(onEvent)
    ├── app-shell.ts    AppShell：login / logout / exec / navigate / throttledRefresh / #applyDelta
    ├── main.ts         入口
    └── views/          7 个视图（各 3 ~ 5 个方法，对应 UI-01 ~ UI-12）
```

### 1.4 `schema/`

两份 DDL **同源**（SA-09），差异由 `DbDriver` 抽象吸收：

| | SQLite | PostgreSQL |
| --- | --- | --- |
| 用途 | 本地单可执行 | 云端单机三容器 |
| 差异 | `INTEGER PRIMARY KEY`、`TEXT`、`PRAGMA foreign_keys = ON` | `BIGINT`、`VARCHAR(n)`、`TIMESTAMPTZ` |

两份结构一致：**11 张业务表 + `schema_version`（1 列，不计入 83）/ 83 列 / 13 个外键 / 9 个索引（IX-01 ~ IX-09：7 个显式 `CREATE INDEX` + 2 处内联 UNIQUE）**。

---

## 二、构建与验证

> 日常构建推荐直接用 `Makefile`（见 3.1）：它会自动选择 cmake 或直编兜底，并把下面各步串成 `make backend / test / typecheck / schema / verify`。本节保留手工命令，便于在 CI 或脚本里逐步复现。

### 2.1 CMake（首选）

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
ctest --test-dir build --output-on-failure      # 运行 smoke 测试
./build/bin/isa_sim                              # 主程序（骨架阶段返回 0）
```

三个目标按层组织，`isa_kernel` **不链接任何第三方库** —— 这是 NFR-C4「内核层零第三方链接」在构建系统上的落点；`isa_server` 通过 `target_link_libraries(... isa_kernel)` 单向依赖。

### 2.2 无 CMake 时的直编兜底

本机（MinGW w64devkit + g++ 15.2.0）无 `cmake`，可用：

```bash
GXX=/d/MyGCC/GNU-w64devkit-gcc/w64devkit/bin/g++

# 逐文件语法检查（27 个 .cpp）
for f in $(find src -name '*.cpp'); do $GXX -std=c++17 -Iinclude -Isrc -fsyntax-only "$f" || echo "FAIL $f"; done

# 链接与运行
CORE=$(find src/core src/isa src/compare -name '*.cpp')
SRV=$(find src/adapt src/domain src/api src/base -name '*.cpp')
$GXX -std=c++17 -Iinclude -Isrc $CORE tests/smoke_test.cpp -o build/isa_smoke.exe && ./build/isa_smoke.exe
$GXX -std=c++17 -Iinclude -Isrc $CORE $SRV src/main.cpp -o build/isa_sim.exe && ./build/isa_sim.exe
```

### 2.3 前端类型检查

```bash
cd frontend
npm install          # 只装 typescript
npm run typecheck    # tsc -p tsconfig.json --noEmit
```

> 无网络时可用任意已装的 `tsc 5.4` 直接跑：
> `node <路径>/typescript/bin/tsc -p tsconfig.json --noEmit`

### 2.4 DDL 自检

推荐直接用随附的自检脚本（同时校验两份 DDL，并逐项打印期望值）：

```bash
make schema            # 等价于 python _gen/check_schema.py
```

等价的手写版本：

```bash
python - <<'PY'
import sqlite3, pathlib
con = sqlite3.connect(":memory:"); con.execute("PRAGMA foreign_keys = ON")
con.executescript(pathlib.Path("schema/sqlite_schema.sql").read_text(encoding="utf-8"))
q = con.execute
tabs = [r[0] for r in q("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
print("表", len(tabs))
print("列", sum(len(list(q("pragma table_info(%s)" % t))) for t in tabs))
print("外键", sum(len(list(q("pragma foreign_key_list(%s)" % t))) for t in tabs))
PY
# 期望：表 12 / 列 84 / 外键 13
```

---

---

## 三、构建入口与部署

### 3.1 `Makefile` —— 便捷构建入口

`Makefile` 只是 CMake 的**外壳，不引入第二套构建定义**：有 `cmake` 的环境走 cmake（制品与 `CMakeLists.txt` 完全一致），没有则自动回退到 `g++` 直编直链（本机开发环境即属后者）。

```bash
make help        # 列出全部目标与可覆盖变量
make             # = make all（backend + frontend）
make backend     # 后端：cmake 优先，缺失时自动 fallback 到 direct
make direct      # 强制 g++ 直编：逐文件语法检查 + 链接 isa_sim / isa_smoke
make frontend    # 前端：tsc 编译 + 把 index.html 复制进 dist/（自包含静态包）
make typecheck   # 前端类型检查（tsc --noEmit）
make test        # 跑冒烟测试
make run         # 构建并运行 isa_sim
make schema      # 校验两份 DDL 的表 / 列 / 外键 / 索引计数
make verify      # = test + typecheck + schema
make clean       # 删后端构建产物
make distclean   # clean + 删 frontend/dist 与 node_modules
```

可覆盖变量：`CMAKE / CTEST / BUILD_TYPE / BUILD_DIR / CXX / EXTRA_CXXFLAGS / PYTHON / TSC`，例如
`make typecheck TSC=/path/to/typescript/bin/tsc`、`make direct EXTRA_CXXFLAGS=-Wextra`。

> **两条 Windows 环境注意**（本机即 Windows + MinGW w64devkit）：
> 1. `CXX` / `CXXFLAGS` 是 make 的**内建变量**，MinGW 下 `CXX` 默认指向 `x86_64-w64-mingw32-g++`，用 `?=` 不生效 —— 所以 Makefile 里是**显式赋值**，命令行仍可覆盖。
> 2. **recipe 里的输出消息一律写英文**：Windows 下 make 按系统 ANSI 代码页把 recipe 字符串传给 shell，文件里的 UTF-8 中文会被转码破坏（实测「已清理…」→「完叉…」）。注释不进入 shell，故保留中文。

### 3.2 容器化 —— 云端形态「单机三容器」

对齐 SAD 6.2 / 6.5 / 7.2：**边缘（nginx，唯一发布 443）/ 应用（不发布端口）/ 数据（PostgreSQL 16，不发布端口）**。

| 文件 | 内容 |
| --- | --- |
| `docker/Dockerfile.edge` | 多阶段：node 构建前端 → nginx 托管 `dist/` 并反代 `/api`、`/ws` |
| `docker/Dockerfile.app` | 多阶段：debian 构建后端 → 运行期含 RV 工具链；`WITH_SPIKE=1` 时额外从源码编译 Spike 1.1.0 |
| `docker/Dockerfile.db` | `postgres:16` + 初始化 `schema/postgres_schema.sql` |
| `docker/nginx.conf` | 上游用 resolver + 变量**请求时解析**（应用晚就绪时只返 502，不因上游缺失而退出） |
| `docker-compose.yml` | 三容器编排 + `isa-net` 桥接网络 + `pgdata` 卷 |

```bash
cp .env.example .env        # 必须设置 POSTGRES_PASSWORD（留空则 compose 直接报错退出）
docker compose up --build
# 浏览器访问 https://localhost（自签名证书，需手动信任）
```

设计要点：

- **端口发布规则**：只有边缘容器发布宿主机端口（`HTTPS_PORT`，默认 443）；应用与数据仅在容器网络内可达。
- **双形态同源（SA-09）**：云端不是另一套代码，形态只由配置项区分 —— compose 通过 `ISA_DB_DRIVER=postgres` 等环境变量把 `FileConfig` 指向云端形态。
- **不发布弱口令**：`POSTGRES_PASSWORD` 用 `${VAR:?msg}` 语法强制必填，未配置时 compose 直接失败退出。
- 应用容器内以**非 root 用户** `isa` 运行；`EXPOSE 8080` 仅为文档性声明（不发布到宿主机）。
- **这不是集群编排**：LIM-01 / LIM-06 / LIM-10 明确不做多主机调度、服务网格与副本伸缩，本文件只在一台主机上编排三个容器。

> **验证状态**：`isa-sim/db:16` 起容器后 PostgreSQL 真建出 **11 张业务表 + `schema_version` / 83 列 / 13 外键 / 9 个 `ix_*` 索引**，与 SQLite 侧数值逐一一致（SA-09「双形态同源」的实测背书）；`isa-sim/edge:0.1` 的 `/healthz`、首页（自有 `index.html`）与 `/main.js` 均返回 200。
> `isa-sim/app:0.1` **仅通过 `docker compose config` 的语法校验，未实际构建**（多阶段构建需装 RV 工具链，耗时较长，本次跳过）。

### 3.3 配置示例与形态区分

| 文件 | 形态 | 说明 |
| --- | --- | --- |
| `config.example.toml` | 本地（单可执行 + SQLite） | `IConfig` 九个配置项 + `db.path`；复制为 `config.toml` 后使用 |
| `.env.example` | 云端（三容器） | compose 用的数据库凭据、`HTTPS_PORT`、`WITH_SPIKE` |

两者的**读取优先级一致**：环境变量 > 配置文件 > 内置默认值，全部由 SS-8 的 `FileConfig` 统一实现，其余代码不出现「if 本地 / else 云端」的判断（SAD 6.6 / T5）。

`config.toml` 与 `.env` 都被 `.gitignore` 忽略（凭据与本机路径不入版本库），而 `*.example.*` 必须入库。

### 3.4 `third_party/` —— 依赖清单与许可归档

`third_party/README.md` 是 **NFR-C4「许可合规」的落点**：列明全部第三方依赖的版本、许可证、归属层、集成方式与**是否进入产品链接链路**。

关键结论：产品链接链路（前端包 + 服务端可执行 + 内核静态库）**全部落在宽松许可**；GPLv2 的 riscv-gnu-toolchain **仅以子进程调用**，不链接其库、不分发其源码，因而不产生传染 —— 这正是 SS-4 `ToolchainAdapter` 存在的核心原因之一（SAD 5.3.4 / SA-06）。`licenses/` 目前为空属**预期**（骨架未引入任何第三方依赖），依赖随对应构件实现时逐项归档。

### 3.5 仓库忽略规则

仓库根的 `../.gitignore` 只忽略「可由源码再生成」与「本机私有」的东西：构建产物（`build/`、`*.o`、`*.exe`）、前端依赖与产物（`node_modules/`、`dist/`）、运行时数据库文件（`*.db`、`*.sqlite3`）、Python 缓存、本机凭据（`.env`、`config.toml`）、编辑器与系统文件。

所有**交付物一律入库**：源码、头文件、DDL、构建脚本、图件（`.svg`）、文档（`.md`）、`*.example.*`、`_gen/` 生成器源码。

> 一个易踩的坑：`*.db` 会顺带匹配 `docker/Dockerfile.db`，故 `.gitignore` 里用 `!Dockerfile.db` 显式排除。

---

## 四、骨架约定

1. **可预期失败一律 `Result<T>`，方法不抛异常**（类设计 G-6）。`ErrCode::NotImplemented` 是**骨架专用占位**，注释已写明「实现完成后应彻底消失」。
2. **`CancelToken` 是唯一给出完整实现的类型**（`include/isa/values.hpp`）：全设计唯一的共享所有权处（`shared_ptr<atomic<bool>>`），内核每 `IConfig.cancelCheckInterval()`（默认 4096）步检查一次。
3. **内核头不依赖 SS-8 契约**：`EmulatorCore` 的构造参数是 `std::size_t traceCapacity` 而非 `const IConfig&`，以保住「内核层零第三方链接」的干净边界。
4. **跨子系统只传接口与值类型**：跨子系统只需指针 / 引用，故 `fwd.hpp` 的前向声明已足够；完整类型一律经 `include/isa/` 的公共层。
5. **JSON 暂以 `std::string` 承载**：设计预留 `nlohmann/json`（详细设计 6.5.2 约定③），骨架阶段不引入第三方依赖；接入时在 `CMakeLists.txt` 的 `isa_server` 处 `find_package` / `FetchContent` 即可。
6. **`IDecodeTable` 由内核侧定义**（`src/core/idecode_table.hpp`）、SS-2 实现（`DecodeTable`）—— 这是 SA-01 依赖倒置的落点。

---

## 五、代码生成器与自检脚本 `_gen/`

骨架中的多数文件由生成器产出，便于批量修订与保持结构一致。生成器**不是**交付物的一部分，改动后建议重跑。

```bash
python _gen/gen.py            # 重新生成 include/isa/、src/、frontend/
python _gen/check_schema.py   # 校验两份 DDL 的计数（= make schema）
```

| 文件 | 职责 |
| --- | --- |
| `render.py` | 低层渲染工具：`emit`（写文件）、`origin`（统一「设计依据」文件头）、`st`（结构体）、`en`（枚举 + 位掩码运算符）、`hpp`/`cpp`（命名空间包装） |
| `data_common.py` | 公共类型层：`span` / `result` / `fwd` / `aliases` / `enums` / `values` |
| `data_layers.py` | 各子系统构件：接口头、类头、空实现 `.cpp`、数据表 |
| `gen_frontend.py` | SS-7 前端 8 个构件与 4 个配置文件 |
| `gen.py` | 主入口，依次调用三者 |
| `check_schema.py` | 只读自检：解析两份 DDL 并核对表 / 列 / 外键 / 索引计数（基线 11 / 83 / 13 / 9） |

> 注意：`schema/*.sql`、`CMakeLists.txt`、`Makefile`、`docker/*`、`docker-compose.yml`、`tests/smoke_test.cpp`、本 README **不是**生成产物，需手工维护。

> 改生成器时务必让**产物与生成器同步**：例如 `tsconfig.json` 的开关调整要落在 `gen_frontend.py` 的 `TSCONFIG` 常量上，否则重跑一次就会被覆盖回去。

---

## 六、下一步

按依赖顺序逐项消灭 `ErrCode::NotImplemented`，建议从内向外：

1. **SS-8 基础服务**（`src/base/`）：接 SQLite 驱动实现 `DbStore` 的 18 个操作（O-01 ~ O-18）；`FileConfig` 读配置。
2. **SS-1 / SS-2 内核**（`src/core/`、`src/isa/`）：取指—译码—执行—写回；`Trace` 的定容裁剪（`TooOld`）；`IsaLoader` 的描述校验。
3. **SS-3 / SS-4**（`src/compare/`、`src/adapt/`）：逐条比对与终态比对；子进程调用外部工具链与 Spike。
4. **SS-5 领域服务**（`src/domain/`）：7 个服务串起上述能力；两个事务 T-1 `putWorkspace` / T-2 `saveReport`。
5. **SS-6 集成 API**（`src/api/`）：HTTP / WebSocket 边界、鉴权与配额、`Bootstrapper` 装配。
6. **SS-7 前端**（`frontend/`）：`ApiClient` 接通 REST / WS，7 个视图按 ui 文档的 28 条跳转接线。
7. 实现填充完成后，可把 `tsconfig.json` 的 `noUnusedLocals` / `noUnusedParameters` 重新打开。
