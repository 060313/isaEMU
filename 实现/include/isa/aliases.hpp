#pragma once

/**
 * 共享别名（20 个标识与基础别名）
 *
 * 设计依据：《软件详细设计文档》6.5.2 (A) 组
 * （另含 6 个骨架补充别名，见行内标注）
 */

#include <chrono>
#include <cstdint>
#include <string>
#include <vector>

namespace isa {

using Addr = std::uint64_t;  // 地址；32 位 ISA 只用低 32 位
using Word = std::uint32_t;  // 机器字
using Enc = std::uint32_t;  // 指令编码
using RegIdx = std::uint8_t;  // 寄存器序号
using StepNo = std::uint64_t;  // 指令步序号
using UserId = std::uint64_t;  // 用户标识
using Token = std::string;  // 会话令牌（32 字节随机数的 base64url 编码，43 字符）
using WorkspaceId = std::uint64_t;  // 工作区标识
using SpecId = std::string;  // ISA 描述标识
using SuiteId = std::uint64_t;  // 用例集标识
using CaseId = std::uint64_t;  // 用例标识
using ReportId = std::uint64_t;  // 报告标识
using DivergenceId = std::uint64_t;  // 分歧记录标识
using JobId = std::string;  // 任务标识
using ExampleId = std::string;  // 内置示例标识
using Pid = std::int64_t;  // 进程标识
using Hash = std::string;  // 内容摘要（十六进制）
using Version = std::uint32_t;  // 乐观并发版本号
using Timestamp = std::chrono::system_clock::time_point;  // 绝对时刻
using Duration = std::chrono::seconds;  // 时间跨度
using Bytes = std::vector<std::uint8_t>;  // 字节序列（骨架补充）
using Clock = std::chrono::system_clock;  // 时钟（骨架补充）
using CsrId = std::uint16_t;  // CSR 序号（骨架补充）
using PageNo = std::uint32_t;  // 稀疏内存页号（骨架补充）
using FieldMask = std::uint32_t;  // 比对字段位掩码（骨架补充）
using BitMask = std::uint64_t;  // 编码宽度位图（骨架补充）

}  // namespace isa
