# ============================================================================
# ISA 模拟系统 —— 便捷构建入口
#
# 设计依据：《软件体系结构设计文档》7.2（构建与制品）、7.3（依赖方向与许可合规的自动化检查）
#
# 定位：本文件只是 CMake 的便捷外壳，**不引入第二套构建定义**。
#       有 cmake 的环境走 cmake（制品与 CMakeLists.txt 完全一致）；
#       没有 cmake 的环境用 `make direct` 走 g++ 直编直链兜底
#       （本机开发环境即属后者：只有 g++ 15.2.0 与 make）。
#
# 为什么 recipe 里的输出消息一律写英文：
#   Windows 下 make 把 recipe 字符串按系统 ANSI 代码页传给 shell，文件里的
#   UTF-8 中文会被转码破坏（实测「已清理…」变成「完叉…」）。注释不进入 shell
#   故保留中文；需要给人看的输出改为 ASCII，避免在 cmd / Git Bash 下乱码。
#
# 常用：make help
# ============================================================================

CMAKE      ?= cmake
CTEST      ?= ctest
BUILD_TYPE ?= Debug
BUILD_DIR  ?= build
PYTHON     ?= python
TSC        ?= tsc

# 注意：CXX / CXXFLAGS 是 make 的内建变量（MinGW 下 CXX 默认指向
# x86_64-w64-mingw32-g++，用 ?= 不会生效），故这里显式赋值。
# 命令行仍可覆盖：make CXX=clang++ / make EXTRA_CXXFLAGS="-O2 -Wextra"
CXX            := g++
CXXSTD         := c++17
EXTRA_CXXFLAGS ?=
CXXFLAGS       := -std=$(CXXSTD) -Wall -Iinclude -Isrc $(EXTRA_CXXFLAGS)

HAVE_CMAKE := $(shell command -v $(CMAKE) >/dev/null 2>&1 && echo yes)

ifeq ($(OS),Windows_NT)
  EXE       := .exe
  CMAKE_BIN := $(BUILD_DIR)/bin
else
  EXE       :=
  CMAKE_BIN := $(BUILD_DIR)
endif

# 源码划分与 CMakeLists.txt 的三个目标保持一致
KERNEL_SRC := $(wildcard src/core/*.cpp) $(wildcard src/isa/*.cpp) $(wildcard src/compare/*.cpp)
SERVER_SRC := $(wildcard src/adapt/*.cpp) $(wildcard src/domain/*.cpp) \
              $(wildcard src/api/*.cpp) $(wildcard src/base/*.cpp)
ALL_SRC    := $(sort $(wildcard src/*.cpp) $(wildcard src/*/*.cpp))

.DEFAULT_GOAL := all
.PHONY: all backend direct frontend typecheck test run schema verify clean distclean help

# ---------------------------------------------------------------- 主目标
all: backend frontend
	@echo "== backend + frontend build complete =="

# ---------------------------------------------------------------- 后端
backend:
ifeq ($(HAVE_CMAKE),yes)
	@$(CMAKE) -S . -B $(BUILD_DIR) -DCMAKE_BUILD_TYPE=$(BUILD_TYPE)
	@$(CMAKE) --build $(BUILD_DIR) --parallel
else
	@echo "[hint] cmake not found ($(CMAKE)); falling back to direct g++ build"
	@$(MAKE) --no-print-directory direct
endif

# 无 cmake 时的兜底：逐文件语法检查 + 链接两个可执行文件
direct: | $(BUILD_DIR)
	@for f in $(ALL_SRC); do \
	   $(CXX) $(CXXFLAGS) -fsyntax-only $$f || exit 1; \
	 done
	@echo "[ok] syntax check passed: $(words $(ALL_SRC)) source files"
	$(CXX) $(CXXFLAGS) $(KERNEL_SRC) tests/smoke_test.cpp -o $(BUILD_DIR)/isa_smoke$(EXE)
	$(CXX) $(CXXFLAGS) $(KERNEL_SRC) $(SERVER_SRC) src/main.cpp -o $(BUILD_DIR)/isa_sim$(EXE)
	@echo "[ok] built $(BUILD_DIR)/isa_sim$(EXE) and $(BUILD_DIR)/isa_smoke$(EXE)"

$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# ---------------------------------------------------------------- 前端（SS-7）
frontend:
	@command -v $(TSC) >/dev/null 2>&1 || { \
	   echo "[hint] tsc not found; run 'cd frontend && npm install' first"; exit 1; }
	@cd frontend && $(TSC) -p tsconfig.json
	@cp frontend/index.html frontend/dist/index.html
	@echo "[ok] built frontend/dist/ (self-contained static package)"

typecheck:
	@command -v $(TSC) >/dev/null 2>&1 || { \
	   echo "[hint] tsc not found; run 'cd frontend && npm install' first"; exit 1; }
	@cd frontend && $(TSC) -p tsconfig.json --noEmit
	@echo "[ok] frontend typecheck passed: 0 errors"

# ---------------------------------------------------------------- 测试与运行
test:
ifeq ($(HAVE_CMAKE),yes)
	@$(CTEST) --test-dir $(BUILD_DIR) --output-on-failure
else
	@$(MAKE) --no-print-directory direct >/dev/null
	@$(BUILD_DIR)/isa_smoke$(EXE)
endif

run:
ifeq ($(HAVE_CMAKE),yes)
	@$(CMAKE) -S . -B $(BUILD_DIR) -DCMAKE_BUILD_TYPE=$(BUILD_TYPE) >/dev/null
	@$(CMAKE) --build $(BUILD_DIR) --parallel >/dev/null
else
	@$(MAKE) --no-print-directory direct >/dev/null
endif
	@if [ -x "$(CMAKE_BIN)/isa_sim$(EXE)" ]; then "$(CMAKE_BIN)/isa_sim$(EXE)"; \
	 elif [ -x "$(BUILD_DIR)/isa_sim$(EXE)" ]; then "$(BUILD_DIR)/isa_sim$(EXE)"; \
	 else echo "[error] isa_sim$(EXE) not found; run 'make backend' first"; exit 1; fi

# ---------------------------------------------------------------- 校验
# 两份 DDL 的表 / 列 / 外键 / 索引计数（对齐详细设计 7.3 的数据设计基线）
schema:
	@$(PYTHON) _gen/check_schema.py

verify: test typecheck schema
	@echo "== all checks passed =="

# ---------------------------------------------------------------- 清理
clean:
	@rm -rf $(BUILD_DIR)
	@echo "[ok] backend build artifacts removed"

distclean: clean
	@rm -rf frontend/dist frontend/node_modules frontend/tsconfig.tsbuildinfo
	@echo "[ok] frontend artifacts and dependencies removed"

# ---------------------------------------------------------------- 帮助
help:
	@echo "ISA simulator - build targets:"
	@echo "  all        build backend + frontend (default)"
	@echo "  backend    build backend (cmake when available, else direct g++)"
	@echo "  direct     force plain g++ build (fallback when cmake is absent)"
	@echo "  frontend   build frontend to frontend/dist/"
	@echo "  typecheck  frontend type check (tsc --noEmit)"
	@echo "  test       run the smoke test"
	@echo "  run        build and run isa_sim"
	@echo "  schema     verify table/column/FK/index counts in both DDL files"
	@echo "  verify     run all checks (test + typecheck + schema)"
	@echo "  clean      remove backend build artifacts"
	@echo "  distclean  clean + remove frontend artifacts and node_modules"
	@echo ""
	@echo "Overridable variables:"
	@echo "  CMAKE CTEST BUILD_TYPE BUILD_DIR CXX EXTRA_CXXFLAGS PYTHON TSC"
	@echo "  e.g.  make typecheck TSC=/path/to/typescript/bin/tsc"
	@echo "        make direct EXTRA_CXXFLAGS=-Wextra"
