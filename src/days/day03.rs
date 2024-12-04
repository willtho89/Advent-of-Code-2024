use regex::Regex;
use std::fs::read_to_string;
use crate::etc::Solution;
use crate::SolutionPair;

pub fn solve() -> SolutionPair {
    let input = read_to_string("input/03.input").expect("Failed to read input file");

    // Part 1
    let pattern = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    let mut ans1 = 0;

    for cap in pattern.captures_iter(&input) {
        let num1: i64 = cap[1].parse().unwrap();
        let num2: i64 = cap[2].parse().unwrap();
        ans1 += num1 * num2;
    }

    // Part 2
    let mul_pattern = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    let do_pattern = Regex::new(r"do\(\)").unwrap();
    let dont_pattern = Regex::new(r"don't\(\)").unwrap();

    // Use find_iter to include the matched patterns as tokens
    let tokens: Vec<&str> = Regex::new(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
        .unwrap()
        .find_iter(&input)
        .map(|m| m.as_str())
        .collect();

    let mut enabled = true;
    let mut ans2 = 0;

    for token in tokens {
        if do_pattern.is_match(token) {
            enabled = true;
        } else if dont_pattern.is_match(token) {
            enabled = false;
        } else if enabled {
            if let Some(cap) = mul_pattern.captures(token) {
                let num1: i64 = cap[1].parse().unwrap();
                let num2: i64 = cap[2].parse().unwrap();
                ans2 += num1 * num2;
            }
        }
    }

    (Solution::from(ans1), Solution::from(ans2))
}