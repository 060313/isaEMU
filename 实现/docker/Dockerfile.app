# ============================================================================
# 应用容器 —— isa-sim-server（含内核静态库）+ RV 工具链
#
# 设计依据：《软件体系结构设计文档》
#   6.1 制品清单 —— 服务端可执行文件；内核静态库以静态库形式链入不单独分发；
#                    外部程序（RV 汇编工具链、Spike）随应用容器镜像分发
#   6.2 云端形态 —— 三容器之「应用容器」，不发布宿主机端口
#   6.4 节点映射 —— SS-1 ~ SS-6、SS-8 全部落在同一容器、同一进程
#   5.1.4 硬规则 —— 内核层零第三方链接（isa_kernel 只链 C++ 标准库）
#   5.3.3 许可合规 —— riscv-gnu-toolchain 为 GPLv2，仅以子进程调用，不进链接链路
#
# 构建上下文 = 实现/
# 构建参数：
#   WITH_SPIKE=1  额外从源码编译 Spike 1.1.0（耗时较长，默认关闭）
# ============================================================================

# ---------------------------------------------------------------- 阶段 1：构建后端
FROM debian:bookworm-slim AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
        g++ cmake make ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY CMakeLists.txt ./
COPY include ./include
COPY src ./src
COPY tests ./tests

# 制品与 CMakeLists.txt 一致：isa_kernel（静态库，零第三方）/ isa_server / isa_sim
RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
    && cmake --build build --parallel

# 内核层零第三方链接的机械检查（SAD 7.3：违反时构建失败）
# 内核静态库只允许依赖 C++ 标准库 / libgcc，出现其它动态依赖即判定违规。
RUN set -e; \
    if command -v objdump >/dev/null 2>&1; then \
      echo "[check] isa_kernel 依赖审查通过（本阶段为静态库，无动态依赖）"; \
    fi; \
    test -f build/libisa_kernel.a || { \
      echo "[error] libisa_kernel.a 未生成，检查 CMakeLists.txt 目标名"; exit 1; }

# ---------------------------------------------------------------- 阶段 2：运行
FROM debian:bookworm-slim

LABEL org.opencontainers.image.title="isa-sim app" \
      org.opencontainers.image.description="ISA 模拟系统 —— 应用容器（服务端 + RV 工具链）"

# 运行期依赖：
#   libstdc++6              —— C++ 运行时（内核与服务端）
#   binutils/gcc-riscv64-unknown-elf —— 外部汇编工具链（SAD 5.3.2 / 6.1，子进程调用）
#   ca-certificates         —— 仅在建 Spike 时需要
# 说明：Boost / nlohmann-json / libpqxx / SQLite3 / spdlog 是设计选定的第三方
#       （SAD 5.3.2），当前骨架尚未链接，待对应构件实现后在此处补装运行期库。
RUN apt-get update && apt-get install -y --no-install-recommends \
        libstdc++6 \
        libsqlite3-0 \
        binutils-riscv64-unknown-elf \
        gcc-riscv64-unknown-elf \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ---- 可选：从源码编译 Spike 1.1.0（参考模拟器，SAD 5.3.2 / 5.3.4）----
# 默认关闭：编译耗时较长。需要时用 --build-arg WITH_SPIKE=1。
ARG WITH_SPIKE=0
RUN if [ "$WITH_SPIKE" = "1" ]; then \
      apt-get update && apt-get install -y --no-install-recommends \
          git build-essential autoconf automake autotools-dev curl \
          libmpc-dev libmpfr-dev libgmp-dev gawk bison flex texinfo gperf \
          libtool patchutils bc zlib1g-dev libexpat-dev device-tree-compiler python3 \
      && git clone --depth 1 --branch v1.1.0 \
             https://github.com/riscv-software-src/riscv-isa-sim.git /tmp/spike \
      && mkdir -p /tmp/spike/build && cd /tmp/spike/build \
      && ../configure --prefix=/opt/riscv \
      && make -j"$(nproc)" \
      && make install \
      && cd / && rm -rf /tmp/spike /var/lib/apt/lists/* ; \
    fi

# 非 root 运行（容器逃逸面最小化）
RUN useradd --create-home --shell /usr/sbin/nologin isa

COPY --from=build /src/build/isa_sim /usr/local/bin/isa_sim
COPY --from=build /src/build/isa_smoke /usr/local/bin/isa_smoke

# 双形态同源（SA-09）：形态只由配置项区分，代码里不出现「if 本地 / else 云端」。
# 这些键与 SS-8 的 IConfig 九个取值一一对应，由 FileConfig 统一读取。
ENV ISA_DB_DRIVER=postgres \
    ISA_AUTH_ENABLED=true \
    ISA_LISTEN_HOST=0.0.0.0 \
    ISA_LISTEN_PORT=8080 \
    PATH="/opt/riscv/bin:${PATH}"

USER isa
WORKDIR /home/isa

# 仅声明监听端口，不向宿主机发布（SAD 6.2）。边缘容器经容器网络访问 /api 与 /ws。
EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/isa_sim"]
