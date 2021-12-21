#include <iostream>

#include <fstream>

#include <array>

#include <vector>

#include <random>

#include <future>

#include <chrono>

#include <atomic>

#include <string>

#include <sstream>

#include <algorithm>

#include <typeinfo>

#include <assert.h>

#include <immintrin.h>

using namespace std::chrono;
using namespace std;

// Enable to track stuff
constexpr bool COUNT_EXTRA = false;

// Typedefs
using TimePoint = std::chrono::steady_clock::time_point;

// Fast, dumb random number generator
// Via https://stackoverflow.com/questions/1640258/need-a-fast-random-generator-for-c
static uint64_t x = 123456789, y = 362436069, z = 521288629;
uint64_t static_rng(void)
{
    uint64_t t;
    x ^= x << 16;
    x ^= x >> 5;
    x ^= x << 1;

    t = x;
    x = y;
    y = z;
    z = t ^ x ^ y;

    return z;
}

struct rng {
    uint64_t x = 123456789;
    uint64_t y = 362436069;
    uint64_t z = 521288629;

    uint64_t gen()
    {
        uint64_t t;
        x ^= x << 16;
        x ^= x >> 5;
        x ^= x << 1;

        t = x;
        x = y;
        y = z;
        z = t ^ x ^ y;

        return z;
    }
};

// Helper to generate a small integer of type T
template <typename T>
T rng_small_num()
{
    constexpr T RNG_MIN = 0;
    constexpr T RNG_MAX = 1024;
    constexpr T RNG_DIFF = RNG_MAX - RNG_MIN;
    return T(RNG_MIN + static_rng() % RNG_DIFF);
}

// Fill a span with random numbers
template <typename T>
void fill_rng(T* begin, T* end)
{
    for (auto ptr = begin; ptr < end; ++ptr)
        *ptr = rng_small_num<T>();
}

// Print utility
std::string str_from_bytes(size_t num_bytes)
{
    int div = 0;
    while (num_bytes >= 1024) {
        num_bytes /= 1024;
        div += 1;
    }

    // I hate C++ so much
    std::ostringstream ss;
    ss << num_bytes;

    if (div == 0) {
        ss << " bytes";
    }
    else if (div == 1) {
        ss << "Kb";
    }
    else if (div == 2) {
        ss << "Mb";
    }
    else if (div == 3) {
        ss << "Gb";
    }
    else if (div == 4) {
        ss << "Tb";
    }
    else {
        ss << "unexpected";
    }

    return ss.str();
}

// A begin/end pointer pair with some utilities
template <typename T>
struct Slice {
    T* _begin = nullptr;
    T* _end = nullptr;

    Slice() = default;
    Slice(T* s, T* e)
        : _begin(s)
        , _end(e)
    {
        if (_end < _begin) {
            std::abort();
        }
    }
    Slice(Slice const& other) = default;
    Slice(std::vector<T>& v)
        : _begin(v.data())
        , _end(v.data() + v.size())
    {
    }
    Slice subslice(size_t offset)
    {
        return Slice(_begin + offset, _end);
    }
    Slice subslice(size_t offset, size_t new_length)
    {
        return Slice(_begin + offset, _begin + offset + new_length);
    }

    __attribute__((always_inline)) T* begin()
    {
        return _begin;
    }
    __attribute__((always_inline)) T* end()
    {
        return _end;
    }
    __attribute__((always_inline)) size_t size() const
    {
        return _end - _begin;
    }
    __attribute__((always_inline)) bool is_empty() const
    {
        return size() == 0;
    }
    __attribute__((always_inline)) T const& operator[](size_t index) const
    {
        return _begin[index];
    }

    template <size_t N>
    static Slice<T> from_array(std::array<T, N>& arr)
    {
        return Slice<T>(arr.data(), arr.data() + arr.size());
    }
};

// Structure holding summation result and timing info
struct Result {
    int64_t sum = 0;
    int64_t bytes_touched = 0;
    int64_t ops = 0;
    TimePoint start;
    TimePoint end;

    Result() = default;
    Result(int64_t _sum, int64_t _bytes_touched, int64_t _ops, TimePoint _start, TimePoint _end)
        : sum(_sum)
        , bytes_touched(_bytes_touched)
        , ops(_ops)
        , start(_start)
        , end(_end)
    {
    }

    Result& operator+=(Result const& other)
    {
        sum += other.sum;
        if
            constexpr(COUNT_EXTRA)
            {
                bytes_touched += other.bytes_touched;
                ops += other.ops;
            }
        return *this;
    }
};

// Structure holding 16 ints
struct matrix4x4 {
    std::array<int, 16> nums;

    static matrix4x4 gen_random()
    {
        matrix4x4 result;
        fill_rng(result.nums.data(), result.nums.data() + result.nums.size());
        return result;
    }
};

// Structure holding 16 ints with functions that operate in simd
struct matrix4x4_simd {
    std::array<int, 16> nums;
    static matrix4x4_simd gen_random()
    {
        matrix4x4_simd result;
        fill_rng(result.nums.data(), result.nums.data() + result.nums.size());
        return result;
    }
};

// Structure to hold a unique_ptr<matrix4x4>
struct unique_matrix4x4 {
    std::unique_ptr<matrix4x4> ptr;

    static unique_matrix4x4 gen_random()
    {
        unique_matrix4x4 result;
        result.ptr = std::make_unique<matrix4x4>();
        fill_rng(result.ptr->nums.data(), result.ptr->nums.data() + result.ptr->nums.size());
        return result;
    }
};

// Utilities to generate random elements
template <typename T>
T generate_random_element()
{
    return rng_small_num<T>();
}
template <>
matrix4x4 generate_random_element()
{
    return matrix4x4::gen_random();
}
template <>
matrix4x4_simd generate_random_element()
{
    return matrix4x4_simd::gen_random();
}
template <>
unique_matrix4x4 generate_random_element()
{
    return unique_matrix4x4::gen_random();
}

template <typename T>
Result sum(Slice<T> data)
{
    constexpr size_t element_size = sizeof(T);

    Result result;
    const auto begin = data.begin();
    const auto end = data.end();
    for (auto ptr = begin; ptr < end; ++ptr) {
        result.sum += *ptr;
        if
            constexpr(COUNT_EXTRA)
            {
                result.ops += 1;
                result.bytes_touched += element_size;
            }
    }

    return result;
}

template <typename T>
Result sum(Slice<T> data, Slice<uint32_t> indices)
{
    constexpr size_t element_size = sizeof(T);

    Result result;
    for (uint32_t idx : indices) {
        result.sum += data[idx];
        if
            constexpr(COUNT_EXTRA)
            {
                result.ops += 1;
                result.bytes_touched += element_size;
            }
    }

    return result;
}

template <>
Result sum(Slice<matrix4x4> data)
{
    constexpr size_t element_size = sizeof(matrix4x4);
    assert(element_size == 16 * sizeof(int));

    Result result;
    const auto begin = data.begin();
    const auto end = data.end();
    for (auto ptr = begin; ptr < end; ++ptr) {
        result.sum += ptr->nums[0];
        result.sum += ptr->nums[1];
        result.sum += ptr->nums[2];
        result.sum += ptr->nums[3];
        result.sum += ptr->nums[4];
        result.sum += ptr->nums[5];
        result.sum += ptr->nums[6];
        result.sum += ptr->nums[7];
        result.sum += ptr->nums[8];
        result.sum += ptr->nums[9];
        result.sum += ptr->nums[10];
        result.sum += ptr->nums[11];
        result.sum += ptr->nums[12];
        result.sum += ptr->nums[13];
        result.sum += ptr->nums[14];
        result.sum += ptr->nums[15];
        if
            constexpr(COUNT_EXTRA)
            {
                result.ops += 16;
                result.bytes_touched += element_size;
            }
    }

    return result;
}

template <>
Result sum(Slice<matrix4x4> data, Slice<uint32_t> indices)
{
    constexpr size_t element_size = sizeof(matrix4x4);
    assert(element_size == 16 * sizeof(int));

    Result result;
    const auto begin = indices.begin();
    const auto end = indices.end();
    for (uint32_t idx : indices) {
        auto const& nums = data[idx].nums;
        result.sum += nums[0];
        result.sum += nums[1];
        result.sum += nums[2];
        result.sum += nums[3];
        result.sum += nums[4];
        result.sum += nums[5];
        result.sum += nums[6];
        result.sum += nums[7];
        result.sum += nums[8];
        result.sum += nums[9];
        result.sum += nums[10];
        result.sum += nums[11];
        result.sum += nums[12];
        result.sum += nums[13];
        result.sum += nums[14];
        result.sum += nums[15];
        if
            constexpr(COUNT_EXTRA)
            {
                result.ops += 16;
                result.bytes_touched += element_size;
            }
    }

    return result;
}

// Only one version of this because I'm lazy.
Result inc_sum(Slice<matrix4x4> data)
{
    constexpr size_t element_size = sizeof(matrix4x4);
    assert(element_size == 16 * sizeof(int));

    Result result;
    result.start = std::chrono::high_resolution_clock::now();
    const auto begin = data.begin();
    const auto end = data.end();
    for (auto ptr = begin; ptr < end; ++ptr) {
        ptr->nums[0] += 1;
        ptr->nums[1] += 1;
        ptr->nums[2] += 1;
        ptr->nums[3] += 1;
        ptr->nums[4] += 1;
        ptr->nums[5] += 1;
        ptr->nums[6] += 1;
        ptr->nums[7] += 1;
        ptr->nums[8] += 1;
        ptr->nums[9] += 1;
        ptr->nums[10] += 1;
        ptr->nums[11] += 1;
        ptr->nums[12] += 1;
        ptr->nums[13] += 1;
        ptr->nums[14] += 1;
        ptr->nums[15] += 1;

        result.sum += ptr->nums[0];
        result.sum += ptr->nums[1];
        result.sum += ptr->nums[2];
        result.sum += ptr->nums[3];
        result.sum += ptr->nums[4];
        result.sum += ptr->nums[5];
        result.sum += ptr->nums[6];
        result.sum += ptr->nums[7];
        result.sum += ptr->nums[8];
        result.sum += ptr->nums[9];
        result.sum += ptr->nums[10];
        result.sum += ptr->nums[11];
        result.sum += ptr->nums[12];
        result.sum += ptr->nums[13];
        result.sum += ptr->nums[14];
        result.sum += ptr->nums[15];
        if
            constexpr(COUNT_EXTRA)
            {
                result.ops += 16;
                result.bytes_touched += element_size;
            }
    }
    result.end = std::chrono::high_resolution_clock::now();

    return result;
}

template <>
Result sum(Slice<matrix4x4_simd> data)
{
    constexpr size_t element_size = sizeof(matrix4x4);
    assert(element_size == 16 * sizeof(int));

    Result result;
    const auto begin = data.begin();
    const auto end = data.end();
    __m256i simd_sum{
        0
    };
    for (auto ptr = begin; ptr < end; ++ptr) {
        int* data = ptr->nums.data();
        simd_sum = _mm256_add_epi32(simd_sum, _mm256_load_si256(reinterpret_cast<__m256i const*>(data)));
        simd_sum = _mm256_add_epi32(simd_sum, _mm256_load_si256(reinterpret_cast<__m256i const*>(data + 8)));

        if
            constexpr(COUNT_EXTRA)
            {
                result.ops += 2;
                result.bytes_touched += element_size;
            }
    }

    result.sum += simd_sum[0];
    result.sum += simd_sum[1];
    result.sum += simd_sum[2];
    result.sum += simd_sum[3];
    result.sum += simd_sum[4];
    result.sum += simd_sum[5];
    result.sum += simd_sum[6];
    result.sum += simd_sum[7];

    return result;
}

template <>
Result sum(Slice<matrix4x4_simd> data, Slice<uint32_t> indices)
{
    constexpr size_t element_size = sizeof(matrix4x4);
    assert(element_size == 16 * sizeof(int));

    Result result;
    const auto begin = data.begin();
    const auto end = data.end();
    __m256i simd_sum{
        0
    };

    for (auto idx : indices) {
        int const* ptr = data[idx].nums.data();
        simd_sum = _mm256_add_epi32(simd_sum, _mm256_load_si256(reinterpret_cast<__m256i const*>(ptr)));
        simd_sum = _mm256_add_epi32(simd_sum, _mm256_load_si256(reinterpret_cast<__m256i const*>(ptr + 8)));

        if
            constexpr(COUNT_EXTRA)
            {
                result.ops += 2;
                result.bytes_touched += element_size;
            }
    }

    result.sum += simd_sum[0];
    result.sum += simd_sum[1];
    result.sum += simd_sum[2];
    result.sum += simd_sum[3];
    result.sum += simd_sum[4];
    result.sum += simd_sum[5];
    result.sum += simd_sum[6];
    result.sum += simd_sum[7];

    return result;
}

template <>
Result sum(Slice<unique_matrix4x4> data)
{
    constexpr size_t element_size = sizeof(matrix4x4);
    assert(element_size == 16 * sizeof(int));

    Result result;
    const auto begin = data.begin();
    const auto end = data.end();
    for (auto ptr = begin; ptr < end; ++ptr) {
        auto const& nums = ptr->ptr->nums;
        result.sum += nums[0];
        result.sum += nums[1];
        result.sum += nums[2];
        result.sum += nums[3];
        result.sum += nums[4];
        result.sum += nums[5];
        result.sum += nums[6];
        result.sum += nums[7];
        result.sum += nums[8];
        result.sum += nums[9];
        result.sum += nums[10];
        result.sum += nums[11];
        result.sum += nums[12];
        result.sum += nums[13];
        result.sum += nums[14];
        result.sum += nums[15];
        if
            constexpr(COUNT_EXTRA)
            {
                result.ops += 16;
                result.bytes_touched += element_size;
            }
    }

    return result;
}

template <>
Result sum(Slice<unique_matrix4x4> data, Slice<uint32_t> indices)
{
    constexpr size_t element_size = sizeof(matrix4x4);
    assert(element_size == 16 * sizeof(int));

    Result result;
    const auto begin = indices.begin();
    const auto end = indices.end();
    for (uint32_t idx : indices) {
        auto const& nums = data[idx].ptr->nums;
        result.sum += nums[0];
        result.sum += nums[1];
        result.sum += nums[2];
        result.sum += nums[3];
        result.sum += nums[4];
        result.sum += nums[5];
        result.sum += nums[6];
        result.sum += nums[7];
        result.sum += nums[8];
        result.sum += nums[9];
        result.sum += nums[10];
        result.sum += nums[11];
        result.sum += nums[12];
        result.sum += nums[13];
        result.sum += nums[14];
        result.sum += nums[15];
        if
            constexpr(COUNT_EXTRA)
            {
                result.ops += 16;
                result.bytes_touched += element_size;
            }
    }

    return result;
}

// Numerical constants
constexpr int64_t THOUSAND = 1000;
constexpr int64_t MILLION = THOUSAND * THOUSAND;
constexpr int64_t BILLION = MILLION * THOUSAND;

constexpr size_t KILO = 1024;
constexpr size_t MEGA = KILO * 1024;
constexpr size_t GIGA = MEGA * 1024;

// System constants
constexpr size_t CACHE_LINE = 64;
constexpr size_t L1_CORE = KILO * 32;
constexpr size_t L2_CORE = KILO * 256;
constexpr size_t L3_CORE = MEGA * 2;
constexpr size_t NUM_CORES = 6;

// Time utilities
inline auto ns_since(std::chrono::time_point<std::chrono::steady_clock> start)
{
    return duration_cast<nanoseconds>(high_resolution_clock::now() - start).count();
}

inline auto us_since(std::chrono::time_point<std::chrono::steady_clock> start)
{
    return duration_cast<microseconds>(high_resolution_clock::now() - start).count();
}

inline auto ms_since(std::chrono::time_point<std::chrono::steady_clock> start)
{
    return duration_cast<milliseconds>(high_resolution_clock::now() - start).count();
}

inline auto ms_since_and_reset(std::chrono::time_point<std::chrono::steady_clock>& start)
{
    auto now = high_resolution_clock::now();
    auto result = duration_cast<milliseconds>(now - start).count();
    start = now;
    return result;
}

inline auto ns_to_ms(int64_t ns)
{
    return ns / 1000 / 1000;
}

template <typename T, typename GEN>
std::vector<T> generate_elements(size_t num_elements, GEN gen)
{
    std::cout << "Begin alloc. Elements: [" << num_elements << "]  Bytes: [" << num_elements * sizeof(T) << "]";
    auto time_start = high_resolution_clock::now();

    std::vector<T> result;
    result.reserve(num_elements);
    for (auto i = 0; i < num_elements; ++i) {
        result.push_back(gen());
    }

    std::cout << " ... completed in " << ms_since(time_start) << " ms" << std::endl;
    return result;
}

template <typename T, typename GEN>
std::vector<T> generate_bytes(size_t num_bytes, GEN gen)
{
    if (num_bytes % sizeof(T) != 0)
        std::abort();

    auto num_elements = num_bytes / sizeof(T);
    return generate_elements<T, GEN>(num_elements, gen);
}

template <typename T>
std::vector<T> generate_shuffled_indices(size_t count)
{
    std::vector<T> result;
    result.reserve(count);

    std::vector<T> temp;
    temp.reserve(count);

    // Fill temp
    for (size_t i = 0; i < count; ++i) {
        temp.push_back((T)i);
    }

    // Shuffle into result
    while (count > 1) {
        // Copy random value
        auto index = static_rng() % count;
        auto value = temp[index];
        result.push_back(value);

        // Replace value with last value and decrement size
        temp[index] = temp[count - 1];
        count -= 1;
    }
    result.push_back(temp[0]);

    return result;
}

template <typename T>
std::vector<Slice<T> > generate_slices(Slice<T> data, size_t num_slices)
{
    std::vector<Slice<T> > result;

    size_t slice_len = data.size() / num_slices;
    for (auto i = 0; i < num_slices - 1; ++i) {
        auto begin = data.begin() + slice_len * i;
        auto end = begin + slice_len;
        result.emplace_back(begin, end);
    }
    result.emplace_back(data.begin() + slice_len * (num_slices - 1), data.end());

    return result;
}

template <typename T>
std::vector<Slice<T> > generate_slices(Slice<T> data, size_t num_slices, size_t elements_per_slice)
{
    if (elements_per_slice * num_slices > data.size())
        std::abort();

    std::vector<Slice<T> > result;

    for (auto i = 0; i < num_slices; ++i) {
        auto begin = data.begin() + elements_per_slice * i;
        auto end = begin + elements_per_slice;
        result.emplace_back(begin, end);
    }

    return result;
}

template <typename T>
Result sum(Slice<T> slice, size_t elements_to_read)
{
    Result result;

    auto start = std::chrono::high_resolution_clock::now();
    for (;;) {
        if (elements_to_read > slice.size()) {
            result += sum(slice);
            elements_to_read -= slice.size();
        }
        else {
            if (elements_to_read > 0) {
                auto begin = slice.begin();
                auto end = begin + elements_to_read;
                auto subslice = Slice<T>(begin, end);
                result += sum(subslice);
            }
            break;
        }
    }
    auto end = std::chrono::high_resolution_clock::now();

    result.start = start;
    result.end = end;

    return result;
}

template <typename T>
Result sum(Slice<T> data_slice, Slice<uint32_t> indices, size_t elements_to_read)
{
    if (indices.is_empty())
        return sum(data_slice, elements_to_read);

    Result result;

    size_t num_indices = indices.size();

    auto start = std::chrono::high_resolution_clock::now();
    for (;;) {
        if (elements_to_read > num_indices) {
            result += sum(data_slice, indices);
            elements_to_read -= num_indices;
        }
        else {
            if (elements_to_read > 0) {
                auto begin = indices.begin();
                auto end = begin + elements_to_read;
                auto indices_subslice = Slice<uint32_t>(begin, end);
                result += sum(data_slice, indices_subslice);
            }
            break;
        }
    }
    auto end = std::chrono::high_resolution_clock::now();

    result.start = start;
    result.end = end;
    return result;
}

template <typename T, typename OP>
void run(ofstream& json, std::string type_name, Slice<T> full_data, Slice<uint32_t> indices, Slice<size_t> block_sizes, Slice<size_t> bytes_to_read_slice, Slice<size_t> num_threads, size_t num_loops, OP op)
{
    if (!block_sizes.is_empty() && block_sizes.size() != bytes_to_read_slice.size())
        std::abort();

    const size_t element_size = sizeof(T);
    std::string block_str = block_sizes.is_empty() ? "Large Block" : "Small Blocks";
    std::string access_str = indices.is_empty() ? "Sequential Access" : "Random Access";
    std::string access_label = indices.is_empty() ? "seq" : "rand";

    json << "  {" << std::endl;
    json << "    \"title\": \"" << type_name << " - " << block_str << " - " << access_str << "\"," << std::endl;
    json << "    \"lines\": [" << std::endl;

    // For each block_size
    for (auto idx = 0; idx < bytes_to_read_slice.size(); ++idx) {
        const auto bytes_to_read = bytes_to_read_slice[idx];
        const auto block_size = block_sizes.is_empty() ? full_data.size() : block_sizes[idx];
        const size_t elements_to_read = bytes_to_read / element_size;
        bool block_per_thread = !block_sizes.is_empty();
        size_t label_num = block_sizes.is_empty() ? bytes_to_read : block_size;

        if (block_per_thread) {
            std::cout << "  Block Size: " << block_sizes[idx] << std::endl;
        }

        json << "      {" << std::endl;
        json << "        \"num_bytes\": " << bytes_to_read << "," << std::endl;
        json << "        \"label\": \"" << str_from_bytes(label_num) << " " << access_label << "\"," << std::endl;
        json << "        \"thread_times\": [" << std::endl;

        // For 1..num_threads
        for (auto thread_count : num_threads) {

            // Compute data slices
            std::vector<Slice<T> > data_slices = {};
            std::vector<Slice<uint32_t> > index_slices = {};
            std::vector<uint32_t> block_indices = {};

            // Compute index slices
            if (block_per_thread == false) {
                if (indices.is_empty()) {
                    // many data slices, no indices
                    data_slices = generate_slices(full_data, thread_count);
                }
                else if (!indices.is_empty()) {
                    // one data slice, many indices slices
                    data_slices = {
                        full_data
                    };
                    index_slices = generate_slices<uint32_t>(indices, thread_count);
                }
            }
            else {
                const size_t elements_per_block = block_size / element_size;

                if (indices.is_empty()) {
                    // many data slices, no indices
                    data_slices = generate_slices(full_data, thread_count, elements_per_block);
                }
                else if (!indices.is_empty()) {
                    // many data slices, new indices
                    data_slices = generate_slices(full_data, thread_count, elements_per_block);
                    auto len = data_slices[0].size();

                    block_indices = generate_shuffled_indices<uint32_t>(len);
                    index_slices = {
                        block_indices
                    };
                }
            }

            std::cout << std::flush << "    " << thread_count << " Threads: ";
            json << "          ["; // thread entry

            // Run loop_num times
            int64_t total_time = 0;
            Result result;

            for (auto loop_num = 0; loop_num < num_loops; ++loop_num) {
                // Create threads
                std::vector<std::future<Result> > futures;
                std::atomic_bool spin_block = true;
                std::atomic_size_t latch = thread_count;

                for (size_t thread = 0; thread < thread_count; ++thread) {
                    auto data_slice = data_slices.size() > 1 ? data_slices[thread] : data_slices[0];
                    Slice<uint32_t> index_slice = index_slices.empty() ? Slice<uint32_t>() : (index_slices.size() > 1 ? index_slices[thread] : index_slices[0]);

                    // Compute elements to read for this thread
                    // Thread 0 gets remainder
                    size_t elements_to_read_for_thread = elements_to_read / thread_count;
                    if (thread == 0)
                        elements_to_read_for_thread += elements_to_read % thread_count;

                    futures.push_back(std::async(std::launch::async, [data_slice, index_slice, op, elements_to_read_for_thread, &latch, &spin_block]() {
                        // Signal Ready
                        --latch;

                        // Spin until told to go
                        while (spin_block) {
                        };

                        // Do work
                        return op(data_slice, index_slice, elements_to_read_for_thread);
                    }));
                }

                // Wait until all threads are ready to go
                while (latch > 0) {
                };

                // Release the kraken!
                spin_block = false;

                // Run to complete
                auto time_start = high_resolution_clock::now();
                for (auto& future : futures)
                    result += future.get();
                auto elapsed_ns = ns_since(time_start);

                // Print results
                total_time += elapsed_ns;
                std::cout << ns_to_ms(elapsed_ns) << " " << std::flush;
                json << elapsed_ns;
                if (loop_num != num_loops - 1)
                    json << ", ";
            }

            double avg_ns = (double)total_time / num_loops;
            double avg_ms = avg_ns / MILLION;
            double gigabytes_per_sec = ((double)bytes_to_read / GIGA) / (avg_ns / BILLION);

            result.bytes_touched /= num_loops;
            result.ops /= num_loops;
            std::cout << "  Speed: (" << gigabytes_per_sec << ")  AvgMS: (" << avg_ms << ")  BytesTouched: (" << result.bytes_touched << ")  Ops: (" << result.ops << ")  Sum: (" << result.sum << ")" << std::endl;

            if
                constexpr(COUNT_EXTRA)
                {
                    if (result.bytes_touched != bytes_to_read) {
                        std::cout << "Expected to touch [" << bytes_to_read << "] bytes but actually touched [" << result.bytes_touched << "]" << std::endl;
                    }
                }
            json << "]," << std::endl; // close thread entry
        }

        json << "        ]" << std::endl; // close thread_times
        json << "      }," << std::endl; // close line entry
        std::cout << std::endl;
    }

    json << "    ]" << std::endl; // close lines
    json << "  }," << std::endl; // close plot
}

template <typename T>
void run_suite(
    ofstream& json,
    std::string type_str,
    size_t num_loops,
    size_t num_threads,
    size_t bytes_to_generate,
    Slice<size_t> block_sizes,
    Slice<size_t> bytes_to_read_seq,
    Slice<size_t> bytes_to_read_rand)
{
    std::cout << "-----------------------\n" << type_str << "\n----------------------" << std::endl;

    // Generate shared data
    std::vector<size_t> num_generated_bytes = {
        bytes_to_generate
    };
    Slice<size_t> num_generated_bytes_slice = {
        num_generated_bytes
    };

    std::vector<T> elements = generate_bytes<T>(bytes_to_generate, []() {
        return generate_random_element<T>();
    });
    auto elements_slice = Slice<T>(elements);

    std::cout << "Generating indices ..." << std::flush;
    auto time_start = high_resolution_clock::now();
    std::vector<uint32_t> indices = generate_shuffled_indices<uint32_t>(elements.size());
    auto indices_slice = Slice<uint32_t>(indices);
    std::cout << " ... completed in " << ms_since(time_start) << " ms" << std::endl
              << std::endl;

    std::vector<size_t> threads;
    for (size_t i = 0; i < num_threads; ++i)
        threads.push_back(i + 1);
    auto threads_slice = Slice<size_t>(threads);

    auto op_sum = [](Slice<T> slice, Slice<uint32_t> indices, size_t num_loops) {
        return ::sum(slice, indices, num_loops);
    };

    //auto op_inc_sum = [](Slice<T> slice, Slice<uint32_t> indices, size_t num_loops) {
    //	return ::inc_sum(slice, indices, num_loops);
    //};

    std::vector<size_t> four_gb{
        GIGA * 4
    };
    Slice<size_t> slice_four_gb(four_gb);

    std::vector<size_t> one_gb{
        GIGA
    };
    Slice<size_t> slice_one_gb(one_gb);

    // data=4gb, read=4gb, threads=1..N, access=seq, op=sum
    if (true) {
        std::string graph_title = type_str + " - Large Block - Sequential Access";
        std::cout << graph_title << std::endl;
        run(json, type_str, elements_slice, Slice<uint32_t>(), Slice<size_t>(), slice_four_gb, threads_slice, num_loops, op_sum);
    }

    // data=4gb, read=4gb, threads=1..N, access=rng, op=sum
    if (true) {
        std::cout << "Large Block - Random Access" << std::endl;
        run(json, type_str, elements_slice, indices_slice, Slice<size_t>(), one_gb, threads_slice, num_loops, op_sum);
    }

    // data=L1..RAM, read=4gb, threads=1..N, access=seq, op=sum
    if (true) {
        std::cout << "Small Blocks - Sequential Access" << std::endl;
        run(json, type_str, elements_slice, Slice<uint32_t>(), block_sizes, bytes_to_read_seq, threads_slice, num_loops, op_sum);
    }

    // data=L1..RAM, read=4gb, threads=1..N, access=rng, op=sum
    if (true) {
        std::cout << "Small Blocks - Random Access" << std::endl;
        run(json, type_str, elements_slice, indices_slice, block_sizes, bytes_to_read_rand, threads_slice, num_loops, op_sum);
    }

    if (true) {
    }
}

int main()
{
    // TODO(Jonathon): This will write the file somewhere under Bazel's
    // execution root, which is not helpful. Refactor so that the program
    // requires an absolute output path.
    std::string filename = "data.json";
    std::ofstream json(filename, std::ios::binary);

    json << "plots = [" << std::endl;

    // Default values
    size_t bytes_to_generate = GIGA;

    size_t num_loops = 12;
    size_t num_threads = 12;

    constexpr size_t BLOCK_COUNT = 8;
    std::array<size_t, BLOCK_COUNT> block_sizes_arr = {
        L1_CORE / 2,
        L1_CORE,
        L2_CORE / 2,
        L2_CORE,
        L3_CORE / 2,
        L3_CORE,
        L3_CORE * 12,
        MEGA * 64
    };
    auto block_sizes = Slice<size_t>::from_array<>(block_sizes_arr);

    std::array<size_t, BLOCK_COUNT> bytes_to_read_seq_arr = {
        GIGA * 32,
        GIGA * 32,
        GIGA * 16,
        GIGA * 16,
        GIGA * 8,
        GIGA * 8,
        GIGA * 4,
        GIGA * 4
    }; // for sequential access
    auto bytes_to_read_seq = Slice<size_t>::from_array<>(bytes_to_read_seq_arr);

    std::array<size_t, BLOCK_COUNT> bytes_to_read_rand_arr = {
        GIGA * 4,
        GIGA * 4,
        GIGA * 2,
        GIGA * 2,
        GIGA * 1,
        GIGA * 1,
        GIGA / 2,
        GIGA / 2
    }; // for random access
    auto bytes_to_read_rand = Slice<size_t>::from_array<>(bytes_to_read_rand_arr);

    if (true) {
        run_suite<int>(json, "int32", num_loops, num_threads, bytes_to_generate, block_sizes, bytes_to_read_seq, bytes_to_read_rand);
    }

    if (true) {
        run_suite<matrix4x4>(json, "matrix4x4", num_loops, num_threads, bytes_to_generate, block_sizes, bytes_to_read_seq, bytes_to_read_rand);
    }

    if (true) {
        run_suite<matrix4x4_simd>(json, "matrix4x4_simd", num_loops, num_threads, bytes_to_generate, block_sizes, bytes_to_read_seq, bytes_to_read_rand);
    }

    if (true) {
        // matrix4x4_unique is super slow. so reduce size/times
        num_threads = std::min(num_threads, (size_t)6);
        num_loops = std::min(num_loops, (size_t)6);
        constexpr size_t seq_size = GIGA * 4;
        std::array<size_t, BLOCK_COUNT> bytes_to_read_seq_arr = {
            seq_size,
            seq_size,
            seq_size,
            seq_size,
            seq_size,
            seq_size,
            seq_size,
            seq_size
        };
        auto bytes_to_read_seq = Slice<size_t>::from_array<>(bytes_to_read_seq_arr);

        constexpr size_t rand_size = GIGA;
        std::array<size_t, BLOCK_COUNT> bytes_to_read_rand_arr = {
            rand_size,
            rand_size,
            rand_size,
            rand_size,
            rand_size / 2,
            rand_size / 2,
            rand_size / 4,
            rand_size / 4
        }; // for random access
        auto bytes_to_read_rand = Slice<size_t>::from_array<>(bytes_to_read_rand_arr);

        run_suite<unique_matrix4x4>(json, "matrix4x4_unique", num_loops, num_threads, bytes_to_generate, block_sizes, bytes_to_read_seq, bytes_to_read_rand);
    }

    json << "]" << std::endl; // close plots
    json.close();
}
