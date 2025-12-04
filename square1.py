"""
CASH APP / SQUARE INTERVIEW QUESTION
Crop Farming Optimization Problem

PART 1: Greedy Crop Selection
------------------------------
You have some starting money and want to plant crops to maximize profit.

Each crop has:
- name: string
- seed_cost: int (cost to plant)
- sell_value: int (price when you harvest it)
- grow_time: int (days until harvest)

Formula for daily net profit:
    (sell_value - seed_cost) / grow_time

Goal: Plant crops with the highest daily net profit until you run out of money.
      You CAN plant the same crop multiple times.

Return:
    - List of crops you planted (in order)
    - Remaining money

Example:
    starting_money = 200
    crops = [
        ("Cauliflower", 80, 175, 6),  # (175-80)/6 = $15.83/day
        ("Garlic", 40, 60, 6),         # (60-40)/6 = $3.33/day
        ("Kale", 70, 110, 3),          # (110-70)/3 = $13.33/day
        ("Turnip", 20, 35, 2)          # (35-20)/2 = $7.50/day
    ]

    Expected output:
        planted: ["Cauliflower", "Cauliflower", "Turnip", "Turnip"]
        remaining: 0
"""

def part1(starting_money, crops):
    # Initialize starting money
    money = starting_money

    # Determine Best Profit/Day, for each crop
    crop_data =[]
    for name, cost, value, days in crops:
        daily_profit = (value - cost) / days
        crop_data.append((daily_profit, name, cost))

    # Sort in best profit order
    crop_data.sort(reverse=True)
    print(crop_data)

    # Start Buying Crops until you run out of money
    planted = []
    for profit, name, cost in crop_data:
        # For each crop, buy as many as we can and move onto next
        while money >= cost:
            money -= cost
            planted.append(name)

    return planted, money

"""

================================================================================
PART 2: MULTI-DAY SIMULATION WITH REPLANTING
================================================================================

Problem:
Now you're farming over multiple days. Crops that you planted on the first day
will be harvested when enough time has passed, and the sell value can be added
to the available money and used to plant crops again just like the first day.

We should only plant crops that could be harvested before our number of days
left runs out.

We'll now be returning only our available money at the end of a number of days.

Goal:
Maximize your total money after a certain number of days by harvesting crops
and replanting.

Rules:
- Only plant crops that will mature BEFORE the deadline
- When a crop is ready, harvest it (add sell value to money)
- Use harvested money to plant more crops
- If you plant on day 1 with 2-day grow time, it harvests on day 3 (day 1 + 2)

Example:
    starting_money = 60
    num_days = 5
    crops = [same as Part 1]

    Day-by-day breakdown:

    Day 1: Starting money = $60
           Can plant Turnip (2-day grow, ready day 3) ✓
           Cannot plant Kale (3-day grow, ready day 4) ✗ (actually can!)
           Cannot plant Cauliflower (6-day grow, ready day 7) ✗
           Plant Turnip ($20) → Money = $40

    Day 2: Money = $40
           Nothing to harvest
           Plant Turnip ($20) → Money = $20

    Day 3: Money = $20
           Harvest Turnip from Day 1 → Money = $20 + $35 = $55
           Plant Turnip ($20) → Money = $35

    Day 4: Money = $35
           Harvest Turnip from Day 2 → Money = $35 + $35 = $70
           Plant Turnip ($20) → Money = $50
           Plant Turnip ($20) → Money = $30

    Day 5: Money = $30
           Harvest Turnip from Day 3 → Money = $30 + $35 = $65
           Plant Turnip ($20) → Money = $45
           Plant Turnip ($20) → Money = $25
           (These last 2 won't mature, but we still have the money)

    Final money after 5 days: $160
    (Money we have + value of crops that will mature later)
"""



def part2(starting_money, crops, num_days):
    """
    Simulate each day: harvest ready crops, then plant new ones greedily.
    Only plant crops that will mature before deadline.
    """

    # Initialize, and start on day 1
    money = starting_money
    harvested = []
    for day in range(1, num_days + 1):
        # On each day, we want to do the following:
        # Harvest Crops - list of days to get paid
        new_harvested = []
        for harvest_day, value in harvested:
            if day == harvest_day:
                money += value
            else:
                new_harvested.append((harvest_day, value))
        harvested = new_harvested

        # Determine Best Profit/Day, for each crop
        crop_data = []
        for name, cost, value, grow_time in crops:
            if day + grow_time <= num_days:
                daily_profit = (value - cost) / grow_time
                crop_data.append((daily_profit, cost, value, grow_time))

        # Sort the best crops we can still plant
        crop_data.sort(reverse=True)

        # Plant the best crops, and keep track of remaining money, and days to harvest
        for daily_profit, cost, value, grow_time in crop_data:
            while money >= cost:
                money -= cost
                harvested.append((day + grow_time, value))

    return money


# TEST CASES
if __name__ == "__main__":
    crops = [
        ("Cauliflower", 80, 175, 6),
        ("Garlic", 40, 60, 6),
        ("Kale", 70, 110, 3),
        ("Turnip", 20, 35, 2)
    ]

    print("=" * 60)
    print("PART 1 TEST")
    print("=" * 60)
    planted, remaining = part1(200, crops)
    print(f"Planted: {planted}")
    print(f"Remaining: ${remaining}")
    print(f"Expected: ['Cauliflower', 'Cauliflower', 'Turnip', 'Turnip'], $0")
    assert planted == ['Cauliflower', 'Cauliflower', 'Turnip', 'Turnip']
    assert remaining == 0
    print("✓ PASSED")

    print("\n" + "=" * 60)
    print("PART 2 TEST")
    print("=" * 60)
    final_money = part2(60, crops, 5)
    print(f"Final money: ${final_money}")
    print(f"Expected: $160")
    assert final_money == 160
    print("✓ PASSED")

