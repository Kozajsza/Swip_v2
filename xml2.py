import datetime
import random

# Get the current date and time
now = datetime.datetime.now()

# Format the date and time as a string
date_time_str = now.strftime("%Y%m%d%H%M%S")

# Generate four random numbers
random_numbers = [random.randint(0, 9) for _ in range(4)]

# Combine the date and time string with the random numbers
output = date_time_str + "".join(str(x) for x in random_numbers)

# Print the output
print(output)
