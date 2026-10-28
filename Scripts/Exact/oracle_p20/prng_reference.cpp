// Independent reference derived ONLY from master Part I I.4 PRNG/variate
// definitions (METHODOLOGY_v3 sections 6.1, 6.5, 6.8 supply method context).
// No prototype/A source. Compile/execute ONLY by parent on Owls, nice 19.
// Public permutation positions are zero-based. Model IDs, if attached to
// positions, are zero-based ORIGINAL IDs: Part-I original j maps to j-1.
// This executable emits finite deterministic reference vectors, not samples
// for statistical inference. Native uint64_t overflow supplies modulo 2^64.
#include <array>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <limits>
#include <numeric>
#include <vector>

static_assert(std::numeric_limits<std::uint64_t>::digits == 64, "need uint64");
static_assert(sizeof(double) == 8 && std::numeric_limits<double>::is_iec559,
              "need IEEE binary64");

struct Generator {
    std::array<std::uint64_t, 4> state{};
    std::uint64_t draws = 0;

    Generator(std::uint64_t seed, std::uint64_t stream) {
        std::uint64_t x = (seed << 32) + stream;
        for (auto& word : state) {
            x += UINT64_C(0x9e3779b97f4a7c15);
            auto z = x;
            z = (z ^ (z >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
            z = (z ^ (z >> 27)) * UINT64_C(0x94d049bb133111eb);
            word = z ^ (z >> 31);
        }
    }
    static std::uint64_t rotate(std::uint64_t x, unsigned k) {
        return (x << k) | (x >> (64 - k));
    }
    std::uint64_t next() {
        const auto result = rotate(state[1] * UINT64_C(5), 7) * UINT64_C(9);
        const auto t = state[1] << 17;
        state[2] ^= state[0];
        state[3] ^= state[1];
        state[1] ^= state[2];
        state[0] ^= state[3];
        state[2] ^= t;
        state[3] = rotate(state[3], 45);
        ++draws;
        return result;
    }
    double uniform() { return static_cast<double>(next() >> 11) * 0x1p-53; }
    std::vector<unsigned> permutation(unsigned size) {
        std::vector<unsigned> result(size);
        std::iota(result.begin(), result.end(), 0u);
        for (unsigned i = size; i > 1; --i) {
            const auto j = static_cast<unsigned>(uniform() * i);
            const auto old = result[i - 1];
            result[i - 1] = result[j];
            result[j] = old;
        }
        return result;
    }
};

template<class Container> void array_json(const Container& values) {
    std::cout << '[';
    bool first = true;
    for (const auto value : values) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << value;
    }
    std::cout << ']';
}

int main() {
    std::cout << "{\"schema\":1,\"clause\":\"Part I I.4\",\"cases\":[";
    bool first = true;
    for (const auto seed : {UINT64_C(1), UINT64_C(2026102201), UINT64_C(2147483647)}) {
        for (unsigned stream = 0; stream < 14; ++stream) {
            if (!first) std::cout << ',';
            first = false;
            Generator words(seed, stream), uniforms(seed, stream), orders(seed, stream);
            std::cout << "{\"seed\":" << seed << ",\"stream\":" << stream
                      << ",\"initial_state\":";
            array_json(words.state);
            std::vector<std::uint64_t> word_values, uniform_bits;
            for (unsigned i = 0; i < 32; ++i) {
                word_values.push_back(words.next());
                const double u = uniforms.uniform();
                std::uint64_t bits;
                std::memcpy(&bits, &u, sizeof(bits));
                uniform_bits.push_back(bits);
            }
            std::cout << ",\"words\":"; array_json(word_values);
            std::cout << ",\"uniform_bits\":"; array_json(uniform_bits);
            std::cout << ",\"state_after_words\":"; array_json(words.state);
            std::cout << ",\"permutations\":[";
            bool first_order = true;
            for (unsigned size : {0u, 1u, 2u, 7u, 19u, 7u}) {
                if (!first_order) std::cout << ',';
                first_order = false;
                const auto order = orders.permutation(size);
                std::cout << "{\"size\":" << size << ",\"positions\":";
                array_json(order);
                std::cout << ",\"draw_count\":" << orders.draws << '}';
            }
            std::cout << "],\"state_after_orders\":";
            array_json(orders.state);
            std::cout << '}';
        }
    }
    std::cout << "]}\n";
    return 0;
}
