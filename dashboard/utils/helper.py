def get_min_block_value(demand, current_value):
    min_value = min(current_value + 1, 96)
    return demand[f"block{min_value}"]


def get_max_block_value(demand, current_value):
    max_value = max(current_value - 1, 1)
    return demand[f"block{max_value}"]


def calculate_current_value(current_block, from_block, to_block, from_value, to_value):
    
    current_value = from_value + (
            (current_block - from_block) *
            (to_value - from_value) / (to_block - from_block + 1)
    )
    return current_value


def add_action(demand, from_block, to_block, from_value, to_value):
    calculated = []
    block_ranges = dict([(f"block{i}", i) for i in range(from_block, to_block + 1)])

    if isinstance(demand, dict):
     for block, current_block in block_ranges.items():
        current_block_value = demand[block]
        current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
        block_value = current_block_value + current_value
        calculated.append((block, block_value))
    else:
     for block, current_block in block_ranges.items():
        current_block_value = getattr(demand, block)
        current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
        block_value = current_block_value + current_value
        calculated.append((block, block_value))

    return dict(calculated)


def multiply_action(demand, from_block, to_block, from_value, to_value):
    calculated = []
    
    block_ranges = dict([(f"block{i}", i) for i in range(from_block, to_block + 1)])

    if isinstance(demand, dict):
     for block, current_block in block_ranges.items():
        current_block_value = demand[block]
        current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
        block_value = current_block_value * current_value
        calculated.append((block, block_value))
    else:
   
     for block, current_block in block_ranges.items():
         current_block_value = getattr(demand, block)
         current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
         block_value = current_block_value * current_value
         calculated.append((block, block_value))

    return dict(calculated)


def average_action(demand,demandref, from_block, to_block, from_value, to_value):
    calculated = []
    block_ranges = dict([(f"block{i}", i) for i in range(from_block, to_block + 1)])
    for block, current_block in block_ranges.items():
        current_block_value = demand[block]

        current_block_value_ref=demandref[block]

        current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
        
        block_value = (current_block_value * current_value) + (current_block_value_ref *(1-current_value))
        # print("block_value avg",block_value)
        calculated.append((block, block_value))
    return dict(calculated)


def shift_left_action(demand, from_block, to_block, from_value, to_value):
    calculated = []
    block_ranges = dict([(f"block{i}", i) for i in range(from_block, to_block + 1)])
    
    if isinstance(demand, dict):
     for block, current_block in block_ranges.items():
        current_block_value = demand[block]
        current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
        min_block_value = get_min_block_value(demand, current_block)
        block_value = (current_block_value * current_value) + (min_block_value * (1 - current_value))
        calculated.append((block, block_value))
    else:
     for block, current_block in block_ranges.items():
         current_block_value = getattr(demand, block)
         current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
         min_block_value = get_min_block_value(demand, current_block)
         block_value = (current_block_value * current_value) + (min_block_value * (1 - current_value))
         calculated.append((block, block_value))
    return dict(calculated)


def shift_right_action(demand, from_block, to_block, from_value, to_value):
    calculated = []
    block_ranges = dict([(f"block{i}", i) for i in range(from_block, to_block + 1)])

    if isinstance(demand, dict):
     for block, current_block in block_ranges.items():
        current_block_value = demand[block]
        current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
        min_block_value = get_min_block_value(demand, current_block)
        block_value = (current_block_value * current_value) + (max_block_value * (1 - current_value))
        calculated.append((block, block_value))

    else: 
     for block, current_block in block_ranges.items():
         current_block_value = getattr(demand, block)
         current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
         max_block_value = get_max_block_value(demand, current_block)
         block_value = (current_block_value * current_value) + (max_block_value * (1 - current_value))
         calculated.append((block, block_value))
    return dict(calculated)


def smooth_action(demand, from_block, to_block, from_value, to_value):
    calculated = []
    block_ranges = dict([(f"block{i}", i) for i in range(from_block, to_block + 1)])
    if isinstance(demand, dict):
     for block, current_block in block_ranges.items():
        current_block_value = demand[block]
        current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
        max_block_value = get_max_block_value(demand, current_block)
        min_block_value = get_min_block_value(demand, current_block)
        block_value = (current_block_value * current_value) + (
                 (max_block_value + min_block_value) * (1 - current_value) / 2
         ) 
        calculated.append((block, block_value))
    else : 
     for block, current_block in block_ranges.items():
         current_block_value = getattr(demand, block)
         current_value = calculate_current_value(current_block, from_block, to_block, from_value, to_value)
         max_block_value = get_max_block_value(demand, current_block)
         min_block_value = get_min_block_value(demand, current_block)
         block_value = (current_block_value * current_value) + (
                 (max_block_value + min_block_value) * (1 - current_value) / 2
         ) 
         calculated.append((block, block_value))
    return dict(calculated)