use crate::{Solution, SolutionPair};
use std::fs::read_to_string;

pub fn solve() -> SolutionPair {
    let input = read_to_string("input/01.input").expect("Failed to read input file");
    let lines: Vec<&str> = input.lines().collect();

    let mut left: Vec<i32> = Vec::new();
    let mut right: Vec<i32> = Vec::new();

    for line in lines {
        let parts: Vec<i32> = line.split_whitespace()
            .map(|s| s.parse().unwrap())
            .collect();
        left.push(parts[0]);
        right.push(parts[1]);
    }

    left.sort();
    right.sort();

    let mut ans1 = 0;
    for i in 0..left.len() {
        ans1 += (left[i] - right[i]).abs();
    }

    let mut ans2 = 0;
    for &l in &left {
        ans2 += l * right.iter().filter(|&&r| r == l).count() as i32;
    }

    (Solution::from(ans1), Solution::from(ans2))
}