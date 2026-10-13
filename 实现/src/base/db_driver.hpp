#pragma once

/**
 * DbDriver —— 双形态数据库驱动抽象（SS-8；SA-10 的落点）
 *
 * 设计依据：7.2.2「9 个逻辑类型 / 7 处 DDL 差异由 DbDriver 吸收」
 * 骨架：只给出接口形状。两个具体驱动（SqliteDriver / PostgresDriver）为后续实现留位。
 */

#include "isa/values.hpp"
#include <string>

namespace isa {

// LogicalType —— 语言的逻辑类型（9 个，7.2.2）；各方言的具体类型由驱动映射
enum class LogicalType {
    U64,        // BIGINT     / INTEGER
    I32,        // INTEGER    / INTEGER
    SmallInt,   // SMALLINT   / INTEGER
    Bool,       // BOOLEAN    / INTEGER
    Text,       // TEXT       / TEXT
    VarChar,    // VARCHAR(n) / TEXT
    Bytes,      // BYTEA      / BLOB
    Json,       // JSONB      / TEXT
    TimePoint,  // TIMESTAMPTZ/ TEXT
};

class DbDriver {
public:
    virtual ~DbDriver() = default;

    virtual DriverKind kind() const = 0;
    virtual std::string dialectFor(LogicalType t) const = 0;  // 9 个逻辑类型 → 方言类型
    virtual std::string nowExpr() const = 0;                  // 时刻表达式
    virtual std::string onConflictClause() const = 0;         // UPSERT 子句
};

}  // namespace isa
