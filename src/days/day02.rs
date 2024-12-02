use std::fs::read_to_string;
use crate::etc::Solution;
use crate::SolutionPair;

pub fn solve() -> SolutionPair {
    let input = read_to_string("input/02.input").expect("Failed to read input file");
    let sanitized_input: Vec<Vec<i32>> = input
        .lines()
        .map(|line| line.split_whitespace().map(|s| s.parse().unwrap()).collect())
        .collect();

    fn is_safe(line: &[i32]) -> bool {
        let mut all_increasing = true;
        let mut all_decreasing = true;

        for i in 0..line.len() - 1 {
            let diff = line[i + 1] - line[i];
            if !(1..=3).contains(&diff) {
                all_increasing = false;
            }
            if !(-3..=-1).contains(&diff) {
                all_decreasing = false;
            }
        }

        all_increasing || all_decreasing
    }

    let mut ans1 = 0;
    for line in &sanitized_input {
        if is_safe(line) {
            ans1 += 1;
        }
    }

    let mut ans2 = 0;
    for line in &sanitized_input {
        if is_safe(line) {
            ans2 += 1;
            continue;
        }

        for i in 0..line.len() {
            let mut line_copy = line.to_vec();
            // remove one entry for each line and check if its now save
            line_copy.remove(i);
            if is_safe(&line_copy) {
                ans2 += 1;
                break;
            }
        }
    }

    (Solution::from(ans1), Solution::from(ans2))
}