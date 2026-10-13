#pragma once

/**
 * isa::Result<T> / isa::Err —— 统一的可预期失败表达
 *
 * 设计依据：《软件详细设计文档》6.4「返回」规则 + 类设计总则 G-6
 *   「可预期失败一律 Result<T>；可能无结果用 optional<T>；方法不抛异常」
 */

#include <optional>
#include <string>
#include <utility>
#include <variant>

namespace isa {

enum class ErrCode {
    Unauthorized,     // 登录失败：NoSuchUser / BadPassword / Disabled
    NotFound,
    Invalid,
    Conflict,         // 同名工作区冲突等
    Disabled,
    TooOld,           // 轨迹已被裁剪，不可回退
    AddrOutOfRange,
    TraceDisabled,
    Internal,
    NotImplemented,   // 骨架占位；实现完成后应彻底消失
};

struct Err {
    ErrCode code{ErrCode::Internal};
    std::string message;
};

template <class T>
class Result {
public:
    Result(T v) : v_(std::move(v)) {}    // NOLINT: 允许直接 return 值
    Result(Err e) : v_(std::move(e)) {}  // NOLINT: 允许直接 return 错误

    static Result ok(T v) { return Result(std::move(v)); }
    static Result err(Err e) { return Result(std::move(e)); }
    static Result err(ErrCode c, std::string m = {}) { return Result(Err{c, std::move(m)}); }

    bool isOk() const { return v_.index() == 0; }
    bool isErr() const { return v_.index() == 1; }

    const T& value() const { return std::get<0>(v_); }
    T& value() { return std::get<0>(v_); }
    const Err& error() const { return std::get<1>(v_); }

private:
    std::variant<T, Err> v_;
};

// 引用返回的特化：std::variant 不允许引用备选，故以指针承载
template <class T>
class Result<T&> {
public:
    Result(T& v) : p_(&v) {}             // NOLINT
    Result(Err e) : e_(std::move(e)) {}  // NOLINT

    static Result ok(T& v) { return Result(v); }
    static Result err(Err e) { return Result(std::move(e)); }
    static Result err(ErrCode c, std::string m = {}) { return Result(Err{c, std::move(m)}); }

    bool isOk() const { return p_ != nullptr; }
    bool isErr() const { return p_ == nullptr; }

    T& value() const { return *p_; }
    const Err& error() const { return e_; }

private:
    T* p_{nullptr};
    Err e_{};
};

template <>
class Result<void> {
public:
    Result() = default;
    Result(Err e) : e_(std::move(e)) {}  // NOLINT

    static Result ok() { return Result(); }
    static Result err(Err e) { return Result(std::move(e)); }
    static Result err(ErrCode c, std::string m = {}) { return Result(Err{c, std::move(m)}); }

    bool isOk() const { return !e_.has_value(); }
    bool isErr() const { return e_.has_value(); }
    const Err& error() const { return *e_; }

private:
    std::optional<Err> e_;
};

}  // namespace isa
