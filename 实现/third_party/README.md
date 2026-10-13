# 第三方依赖与许可归档（`third_party/`）

本目录是 **NFR-C4「许可合规」的落点**：所有第三方依赖的清单与许可证原文归档于此，发布前按此目录逐项核对链接链路。

设计依据：《软件体系结构设计文档》5.3.2（选定资源及集成方式）、5.3.3（许可合规判定）、7.1（`third_party/` 用于依赖清单与许可证归档）、7.3（许可合规的强制方式）。

---

## 一、依赖清单

| 资源 | 版本 / 许可证 | 归属层 | 集成方式 | 是否进入产品链接链路 |
| --- | --- | --- | --- | --- |
| Vue 3 + Vite + Vue Router + Pinia | MIT | L4 | 源码依赖，前端构建为静态资源包 | 是（前端包） |
| CodeMirror 6 | MIT | L4 | 源码依赖，汇编源与 ISA 描述编辑 | 是（前端包） |
| TypeScript 5 | Apache-2.0 | L4 | 编译期依赖 | 否（仅构建期） |
| Boost（Beast + Asio） | 1.92 / BSL-1.0 | L3 | 源码 / 库依赖，HTTP 与 WebSocket 服务端 | 是（服务端可执行） |
| nlohmann/json | MIT | L3 | 头文件依赖，报文的序列化与反序列化 | 是（服务端可执行） |
| ELFIO | 3.12 / MIT | L3 | 头文件依赖，实现 FR-2.1 的「ELF 可装载段载入」 | 是（服务端可执行） |
| libpqxx | BSD-3-Clause | L3 | 库依赖，PostgreSQL 访问 | 是（服务端可执行） |
| SQLite3 | Public Domain | L3 | 库依赖，本地形态存储 | 是（服务端可执行） |
| GoogleTest / Google Benchmark | BSD-3 / Apache-2.0 | 构建期 | 仅测试目标链接 | 否（不进产品） |
| CMake | BSD-3-Clause | 构建期 | 构建系统 | 否（仅构建期） |
| spdlog | MIT | L3 | 可选，日志服务实现之一 | 是（若采用） |
| PostgreSQL | 16+ / PostgreSQL License | 部署期 | 独立服务进程 | 否（独立进程） |
| Docker / Podman | Apache-2.0 | 部署期 | 云端形态的容器运行时 | 否（运行时） |
| nginx | BSD-2-Clause | 部署期 | 云端形态的边缘容器（本地形态不使用） | 否（独立进程） |
| Spike（riscv-isa-sim） | 1.1.0 / BSD-3-Clause | 外部 | **子进程调用**，对拍基准 | 否（子进程） |
| riscv-gnu-toolchain | **GPLv2** | 外部 | **子进程调用**，汇编与链接 | **否（子进程，见下）** |

---

## 二、许可合规判定（NFR-C4）

- **产品链接链路**（前端包 + 服务端可执行 + 内核静态库）**全部落在宽松许可**：
  MIT / BSD-2 / BSD-3 / BSL-1.0 / Apache-2.0 / PostgreSQL License / 公有领域。
- **GPLv2 的 riscv-gnu-toolchain 不进入链接链路**：仅以**外部进程**方式调用，本项目**不链接其库、不分发其源码**，因此**不产生传染**。
  这是 SS-4 `ToolchainAdapter` 存在的核心原因之一（SAD 5.3.4 / SA-06）。
- 交付形态为「**源码 + 构建脚本**」，工具链与参考模拟器由**环境预装并在启动时探测**（LIM-04）；
  云端形态由应用容器镜像预装（SAD 6.1），本地形态由用户安装或随部署包提供（SAD 6.3）。
- **内核层零第三方链接**（NFR-C4 / NFR-I2 / NFR-I3）：`isa_kernel` 目标只允许 C++ 标准库，
  由 `CMakeLists.txt` 的三个目标与 `docker/Dockerfile.app` 的构建期检查共同强制（SAD 7.3）。

---

## 三、归档约定

发布前把各依赖的**许可证原文**放进 `licenses/`，文件名与依赖名一致：

```
third_party/
├── README.md            本文件：依赖清单与合规判定
└── licenses/
    ├── boost.txt        BSL-1.0
    ├── nlohmann-json.txt
    ├── elfio.txt
    ├── libpqxx.txt
    ├── sqlite3.txt      Public Domain
    ├── spdlog.txt
    ├── nginx.txt
    ├── postgresql.txt
    └── riscv-gnu-toolchain.txt   GPLv2（仅作存档，说明其不进入链接链路）
```

`licenses/` 为空属**预期**：骨架阶段尚未引入任何第三方依赖（`include/isa/` 与 `src/` 只依赖 C++17 标准库），
依赖随对应构件实现逐步引入时再逐项归档。

---

## 四、与当前骨架的差距

当前骨架**未链接任何第三方库**，是刻意为之（SAD 5.1.4 的构建约束 + 骨架阶段零依赖）：

| 依赖 | 骨架中的现状 | 引入时机 |
| --- | --- | --- |
| nlohmann/json | `std::string` 承载 JSON 文本（详细设计 6.5.2 约定③） | SS-6 `HttpGateway` 实现报文序列化时 |
| Boost.Beast / Asio | `HttpGateway` 为契约空壳 | SS-6 实现 HTTP / WebSocket 服务端时 |
| ELFIO | 无 | SS-5 `LoadService` 实现 ELF 段载入时 |
| libpqxx / SQLite3 | `DbDriver` 只有抽象与 `LogicalType` | SS-8 `DbStore` 实现 O-01 ~ O-18 时 |
| spdlog | `StdLogger` 为自研空壳 | 可选替换 |
| GoogleTest / Benchmark | `tests/smoke_test.cpp` 用断言与退出码，无框架 | 测试规模扩大时 |

接入方式：在 `CMakeLists.txt` 的 `isa_server` 目标处 `find_package` / `FetchContent`；
**不得**让 `isa_kernel` 产生任何第三方链接（SAD 7.3 的机械检查）。
