#pragma once

/**
 * isa::span —— 最小非拥有只读/可写视图
 *
 * 设计依据：《软件详细设计文档》6.4「参数传递」——大值类型用 span<const T> 传只读视图
 * 说明：设计的构建约束是 C++17（SAD 5.1.4），C++17 无 std::span；为守住「内核层零第三方
 *       链接」，此处提供最小实现，而不是引入 GSL。
 */

#include <cstddef>
#include <type_traits>
#include <vector>

namespace isa {

template <class T>
class span {
public:
    span() = default;
    span(T* p, std::size_t n) : p_(p), n_(n) {}
    span(T* b, T* e) : p_(b), n_(static_cast<std::size_t>(e - b)) {}

    template <class U, class = std::enable_if_t<std::is_convertible<U*, T*>::value>>
    span(const std::vector<U>& v) : p_(v.data()), n_(v.size()) {}  // NOLINT

    template <std::size_t N, class = std::enable_if_t<std::is_convertible<T (*)[N], T*>::value>>
    span(T (&a)[N]) : p_(a), n_(N) {}  // NOLINT

    T* data() const { return p_; }
    std::size_t size() const { return n_; }
    bool empty() const { return n_ == 0; }
    T& operator[](std::size_t i) const { return p_[i]; }
    T* begin() const { return p_; }
    T* end() const { return p_ + n_; }

private:
    T* p_{nullptr};
    std::size_t n_{0};
};

template <class T>
bool operator==(span<T> a, span<T> b) {
    if (a.size() != b.size()) return false;
    for (std::size_t i = 0; i < a.size(); ++i)
        if (!(a[i] == b[i])) return false;
    return true;
}

template <class T>
bool operator!=(span<T> a, span<T> b) { return !(a == b); }

}  // namespace isa
