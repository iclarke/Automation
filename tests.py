one_turf = {'surface': 1.6 * 1.64, 'cost': 20}
garden = 30

total_cost = (garden / one_turf['surface']) * one_turf['cost']
print(f'Total cost is : {total_cost}')
