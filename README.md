# Advent of Code 2024
Based on [agubelu's Rust template for Advent of Code](https://github.com/agubelu/AoC-rust-template) to easily run any day or combination of days and measure the execution time.

Each day has a `solve()` function that returns a pair of `Solution`. The type `Solution` is an enum that can contain any integer or a string.

You can create a `Solution` by specifying its type, for example `Solution::U32(value)`, or by using the From trait which is implemented for all supported types, for example, `Solution::from(value)`.

To run: `cargo run --release [days...]`

## Disclaimer

As I'm a rust newbie, this should not be seen as best practice or anything. I probably wrote the algorithm in Python
first and rewrote it to Rust. 