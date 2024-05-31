import tkinter as tk
from fractions import Fraction
import timeit

def hybrid_sort(array, reverse=False):
    return merge_sort_shell_sort_hybrid(array, reverse)

def merge_sort_shell_sort_hybrid(array, reverse):
    steps = []

    def shell_sort(array):
        n = len(array)
        gap = n // 2
        while gap > 1:  
            for i in range(gap, n):
                temp = array[i]
                j = i
                while j >= gap and (array[j - gap][0] > temp[0] if not reverse else array[j - gap][0] < temp[0]):
                    array[j] = array[j - gap]
                    j -= gap
                array[j] = temp
                steps.append((list(x[1] for x in array), "Shell Sort"))
            gap //= 2
        return array
    
    def merge_sort(array):
        if len(array) > 1:
            mid = len(array) // 2
            left_half = array[:mid]
            right_half = array[mid:]

            merge_sort(left_half)
            merge_sort(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if (left_half[i][0] < right_half[j][0] if not reverse else left_half[i][0] > right_half[j][0]):
                    array[k] = left_half[i]
                    i += 1
                else:
                    array[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                array[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                array[k] = right_half[j]
                j += 1
                k += 1
            steps.append((list(x[1] for x in array), "Merge Sort"))

    array = shell_sort(array)
    merge_sort(array)
    return steps

def update_canvas(canvas, array, current_index=None):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    bar_width = width // len(array)
    max_val = max([float(Fraction(x)) for x in array])
    for i, value in enumerate(array):
        x0 = i * bar_width
        y0 = height
        x1 = (i + 1) * bar_width
        y1 = height - (float(Fraction(value)) / max_val) * height * 0.9  # Scale to fit canvas
        color = "sky blue"
        if i == current_index:
            color = "orange"  # Warna elemen saat ini
        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        canvas.create_text((x0 + x1) / 2, y1 - 10, text=str(value), fill="black")

def process_data(data, reverse=False):
    fraction_data = [(Fraction(x), x) for x in data]
    global steps
    steps = hybrid_sort(fraction_data, reverse)
    return steps

def update_display(reverse=False):
    global step_index, steps
    data = entry.get().split(',')
    
    try:
        # Coba proses input
        start_time = timeit.default_timer()
        steps = process_data(data, reverse)
        end_time = timeit.default_timer()
        
        time_taken = end_time - start_time
        time_label.config(text=f"Waktu yang dibutuhkan: {time_taken:.10f} detik")
        
        step_index = 0
        update_canvas(canvas, steps[step_index][0])
        result_label.config(text=f"Pecahan yang Diurutkan: {', '.join(steps[step_index][0])}")
        step_label.config(text=f"Langkah: {step_index + 1}/{len(steps)}")
        stage_label.config(text=f"Tahap: {steps[step_index][1]}")
    except ValueError:
        result_label.config(text="Input tidak valid, masukkan pecahan yang benar.")
        time_label.config(text="Waktu yang dibutuhkan: 0.0000000000 detik")
        
def next_step():
    global step_index
    if step_index < len(steps) - 1:
        step_index += 1
        update_canvas(canvas, steps[step_index][0])
        result_label.config(text=f"Pecahan yang Diurutkan: {', '.join(steps[step_index][0])}")
        step_label.config(text=f"Langkah: {step_index + 1}/{len(steps)}")
        stage_label.config(text=f"Tahap: {steps[step_index][1]}")

def prev_step():
    global step_index
    if step_index > 0:
        step_index -= 1
        update_canvas(canvas, steps[step_index][0])
        result_label.config(text=f"Pecahan yang Diurutkan: {', '.join(steps[step_index][0])}")
        step_label.config(text=f"Langkah: {step_index + 1}/{len(steps)}")
        stage_label.config(text=f"Tahap: {steps[step_index][1]}")

def reset_steps():
    global step_index
    step_index = 0
    update_canvas(canvas, steps[step_index][0])
    result_label.config(text=f"Pecahan yang Diurutkan: {', '.join(steps[step_index][0])}")
    step_label.config(text=f"Langkah: {step_index + 1}/{len(steps)}")
    stage_label.config(text=f"Tahap: {steps[step_index][1]}")

root = tk.Tk()
root.title("Penyortiran Data Pecahan")
root.geometry("600x650")

# Background color
root.configure(bg="lightblue")

entry_label = tk.Label(root, text="Masukkan pecahan (dipisahkan dengan koma):", bg="lightblue")
entry_label.pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack()

sort_asc_button = tk.Button(root, text="Ascending", command=lambda: update_display(False))
sort_asc_button.pack(pady=10)

sort_desc_button = tk.Button(root, text="Descending", command=lambda: update_display(True))
sort_desc_button.pack(pady=10)

result_label = tk.Label(root, text="Pecahan yang Diurutkan: ", bg="lightblue")
result_label.pack()

canvas = tk.Canvas(root, bg="white", height=300)
canvas.pack(fill=tk.BOTH, expand=True)

step_button_frame = tk.Frame(root, bg="lightblue")
step_button_frame.pack(pady=10)

prev_button = tk.Button(step_button_frame, text="Previous Step", command=prev_step)
prev_button.pack(side="left", padx=10)

next_button = tk.Button(step_button_frame, text="Next Step", command=next_step)
next_button.pack(side="left", padx=10)

reset_button = tk.Button(step_button_frame, text="Reset", command=reset_steps)
reset_button.pack(side="left", padx=10)

step_label = tk.Label(root, text="Step: 0/0", bg="lightblue")
step_label.pack(pady=10)

time_label = tk.Label(root, text="Waktu yang dibutuhkan: 0.0000000000 detik", bg="lightblue")
time_label.pack(pady=10)

stage_label = tk.Label(root, text="Tahap: ", bg="lightblue")
stage_label.pack(pady=10)

# Variable untuk melacak langkah-langkah
steps = []
step_index = 0

root.mainloop()
