def find_time(step, reps, t):
    max_n = 1000000
    result = (((1 + (max_n/step))*reps*(max_n/step))/2) * t
    return (result/60)/60

step = int(input("Enter the step size: ")) #step = 500
reps = int(input("Enter the reps: ")) #reps = 5
time = float(input("Enter the time per step: ")) #time = 0.005
print(f"Time taken for step {step}: {find_time(step, reps, time)} hours") # 2.77h