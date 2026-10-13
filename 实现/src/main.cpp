/**
 * isa-sim 主程序 —— 骨架空壳
 *
 * 设计依据：《软件详细设计文档》6.4.6（Bootstrapper 为组合根）
 * 装配顺序：读配置 → Bootstrapper::build → 启动网关。
 * 骨架阶段只做装配链路占位，返回 0。
 */

#include "api/bootstrapper.hpp"
#include "base/file_config.hpp"
#include "base/i_config.hpp"

int main(int argc, char** argv) {
    (void)argc;
    (void)argv;

    // TODO: FileConfig 从路径读配置 → Bootstrapper::build(cfg) → gateway->handle(...)
    return 0;
}
