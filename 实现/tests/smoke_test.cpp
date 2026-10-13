/**
 * 冒烟测试 —— 验证骨架可编译、可链接，且少数已给出真实实现的类型行为正确。
 *
 * 说明：框架目前是空骨架，绝大多数方法体是占位实现；本测试只覆盖三类：
 *   ① CancelToken（唯一给出完整实现的原语）
 *   ② Result<T> / Result<void>
 *   ③ 值类型的构造与比较、位掩码枚举的运算符
 */

#include "isa/result.hpp"
#include "isa/values.hpp"

#include <cassert>
#include <iostream>

int main() {
    using namespace isa;

    // ① CancelToken
    CancelToken tk;
    assert(!tk.isCancelled());
    tk.cancel();
    assert(tk.isCancelled());
    tk.reset();
    assert(!tk.isCancelled());

    // ② Result<T> 与 Result<void>
    Result<int> ok = Result<int>::ok(7);
    assert(ok.isOk() && ok.value() == 7);

    Result<int> bad = Result<int>::err(ErrCode::Internal, "x");
    assert(bad.isErr() && bad.error().code == ErrCode::Internal);

    Result<void> nothing = Result<void>::ok();
    assert(nothing.isOk());

    // ③ 位掩码枚举与值类型
    Field fields = Field::Pc | Field::Gpr;
    assert(has(fields, Field::Gpr));
    assert(!has(fields, Field::Mem));

    WriteOp a{};
    a.kind = WriteKind::Gpr;
    a.index = 10;
    WriteOp b{};
    b.kind = WriteKind::Gpr;
    b.index = 10;
    assert(a == b);
    b.index = 11;
    assert(!(a == b));

    std::cout << "smoke: ok" << std::endl;
    return 0;
}
