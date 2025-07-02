
import streamlit as st
import random
from itertools import permutations
import operator

# === CONFIG ===
LARGE_NUMS = [25, 50, 75, 100]
SMALL_NUMS = list(range(1, 11)) * 2
OPERATORS = [('+', operator.add), ('-', operator.sub), ('*', operator.mul), ('/', operator.truediv)]

st.set_page_config(page_title="Countdown Numbers Game", layout="centered")
st.title("Countdown Numbers Game")
st.markdown("**Can you reach the target using these numbers?**")

# === Generate Game ===
def generate_game():
    nums = random.sample(LARGE_NUMS, random.randint(0, 4)) + random.sample(SMALL_NUMS, 6)
    nums = random.sample(nums, 6)
    target = random.randint(100, 999)
    return nums, target

# Only initialize once
if 'numbers' not in st.session_state:
    st.session_state.numbers, st.session_state.target = generate_game()

# Display puzzle
st.subheader(f"Target: {st.session_state.target}")
st.write(f"Numbers: `{st.session_state.numbers}`")
st.write("Use + – × ÷ to combine the numbers and hit the target!")

# === Solver ===
def try_all_combinations(numbers, target):
    closest = None
    closest_expr = ""
    min_diff = float('inf')

    def compute(nums, exprs):
        nonlocal closest, closest_expr, min_diff
        if len(nums) == 1:
            result = nums[0]
            if abs(result - target) < min_diff:
                min_diff = abs(result - target)
                closest = result
                closest_expr = exprs[0]
            return

        for i in range(len(nums)):
            for j in range(len(nums)):
                if i != j:
                    for symbol, func in OPERATORS:
                        try:
                            a, b = nums[i], nums[j]
                            val = func(a, b)
                            if val != int(val) or val < 0:
                                continue
                            new_nums = [val] + [nums[k] for k in range(len(nums)) if k != i and k != j]
                            new_expr = f"({exprs[i]} {symbol} {exprs[j]})"
                            new_exprs = [new_expr] + [exprs[k] for k in range(len(exprs)) if k != i and k != j]
                            compute(new_nums, new_exprs)
                        except ZeroDivisionError:
                            continue

    compute(numbers, list(map(str, numbers)))
    return closest, closest_expr

# === Buttons ===
col1, col2 = st.columns(2)

with col1:
    if st.button("New Puzzle"):
        st.session_state.numbers, st.session_state.target = generate_game()
        st.rerun()

with col2:
    if st.button("Reveal Solution"):
        with st.spinner("Thinking hard..."):
            solution, expression = try_all_combinations(st.session_state.numbers, st.session_state.target)
            if solution == st.session_state.target:
                st.success(f"Perfect! `{expression}` = {solution}")
            else:
                st.warning(f"Closest: `{solution}`\n\n`{expression}`\n Off by {abs(solution - st.session_state.target)}")
