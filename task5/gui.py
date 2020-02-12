from tkinter import *
from tkinter import messagebox
import numpy as np
from neural import NeuralNet


class MainApp(Tk):

    def __init__(self, *args, **kwargs):

        super(MainApp, self).__init__(*args, **kwargs)

        Tk.wm_title(self, "Neural network")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.M = 10
        self.learning_algorithm = "Backpropagation"
        self.architecture = [20, 5, 5]
        self.learning_rate = 0.2
        self.max_iter = 10000

        self.frames = {}

        for F in (MainPage, OptionsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(Frame):

    def __init__(self, parent, controller):
        super(MainPage, self).__init__(parent)

        self.controller = controller
        self.neural_net = None
        self.current_gesture = []

        self.canvas = Canvas(self, width=800, height=500)
        self.canvas.pack(expand=YES, fill=BOTH)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        self.class_label = Label(self, text="Class:")
        self.class_label.pack(padx=15)
        self.slider = Scale(self, from_=1, to=5, tickinterval=1, orient=HORIZONTAL)
        self.slider.pack(padx=15, pady=5)

        self.toggle_btn = Button(self, text="Learning", relief=RAISED, command=self.toggle)
        self.toggle_btn.pack(padx=15, pady=5)

        self.button_options = Button(self, text="Options", command=lambda: controller.show_frame(OptionsPage))
        self.button_options.pack(padx=15, pady=5)

        self.button_clear_file = Button(self, text="Clear file", command=self.clear_file)
        self.button_clear_file.pack(padx=15, pady=5)

        self.button_quit = Button(self, text="Quit", command=parent.quit)
        self.button_quit.pack(padx=15, pady=5)

    def toggle(self):
        if self.toggle_btn.config('relief')[-1] == SUNKEN:
            self.toggle_btn.config(text="Learning", relief=RAISED)
            self.neural_net = None
        else:
            self.toggle_btn.config(text="Testing", relief=SUNKEN)
            self.neural_net = NeuralNet("data.txt", algorithm=self.controller.learning_algorithm,
                                        layer_arch=self.controller.architecture,
                                        learning_rate=self.controller.learning_rate,
                                        max_iter=self.controller.max_iter)
            self.neural_net.learn()

    def paint(self, event):
        x1, y1 = event.x + 1, event.y + 1
        x2, y2 = event.x - 1, event.y - 1
        self.canvas.create_oval(x1, y1, x2, y2)
        self.current_gesture.append([event.x, event.y])

    def _on_release(self, event):
        self.canvas.delete("all")

        data = self.transform_data()
        total_distance = 0
        # print(data)

        for first, second in zip(data, data[1:]):
            total_distance += np.linalg.norm(first - second)
        # print(total_distance)

        representatives = [data[0]]
        dist = 0
        k = 1
        for i in range(1, len(data)):
            dist += np.linalg.norm(data[i] - data[i - 1])
            if dist >= k*total_distance/(self.controller.M - 1):
                representatives.append(data[i])
                k += 1
        while len(representatives) < self.controller.M:
            representatives.append(data[len(data) - 1])

        if self.neural_net is None:
            self.store_data(representatives)

        else:
            inputs = []
            for pair in representatives:
                for elem in pair:
                    inputs.append(elem)

            index_class, alfabet_class = self.neural_net.get_class(inputs)
            self.slider.set(index_class + 1)
            print(alfabet_class)

        self.current_gesture = []

    def transform_data(self):
        vector = np.array(self.current_gesture)
        centroid = np.mean(vector, axis=0)
        translated = vector - centroid
        transformer = np.max(np.abs(translated), axis=1)
        scaled = translated / transformer.reshape(-1, 1)
        return scaled

    def store_data(self, representatives):
        classes = np.zeros(5)
        data_class = self.slider.get()
        classes[data_class - 1] = 1
        data = np.array(representatives)
        with open("data.txt", "a") as f:
            for point in data:
                for coordinate in point:
                    f.write(str(coordinate) + ' ')
            for c in classes:
                f.write(str(c) + ' ')
            f.write("\n")

    def clear_file(self):
        with open("data.txt", "w") as f:
            f.write("")





class OptionsPage(Frame):

    def __init__(self, parent, controller):
        super(OptionsPage, self).__init__(parent)

        label_repr = Label(self, text="Number of representative points: ")
        label_repr.grid(row=0, column=0)

        label_arch = Label(self, text="Neural network architecture (input integers split by 'x'): ")
        label_arch.grid(row=2, column=0)

        self.label_first_slot = Label(self, text=str(20) + 'x')
        self.label_first_slot.grid(row=2, column=1)

        sv = StringVar()

        def callback():
            try:
                i = int(self.entry_repr.get())
            except ValueError:
                return False
            self.label_first_slot.config(text=str(int(i) * 2) + 'x')
            return True

        self.entry_repr = Entry(self, width=10, textvariable=sv, validate="focusout", validatecommand=callback)
        self.entry_repr.insert(0, "10")
        self.entry_repr.grid(row=0, column=1)

        self.entry_second = Entry(self, width=25)
        self.entry_second.insert(0, "5")
        self.entry_second.grid(row=2, column=2)

        self.label_last_slot = Label(self, text='x' + str(5))
        self.label_last_slot.grid(row=2, column=3)

        label_learning_algorithm = Label(self, text="Choose a learning algorithm: ")
        label_learning_algorithm.grid(row=3, column=0)

        self.var = StringVar(self)
        self.var.set("Backpropagation")
        self.menu = OptionMenu(self, self.var, "Backpropagation", "Stochastic backpropagation", "Mini-batch Backpropagation")
        self.menu.grid(row=3, column=1)

        self.learning_rate_label = Label(self, text="Enter a learning rate (double): ")
        self.learning_rate_label.grid(row=4, column=0)

        self.entry_lr = Entry(self, width=10)
        self.entry_lr.insert(0, "0.2")
        self.entry_lr.grid(row=4, column=1)

        self.max_iter_label = Label(self, text="Enter maximum number of iterations for learning algorithms (int): ")
        self.max_iter_label.grid(row=5, column=0)

        self.max_iter_entry = Entry(self, width=20)
        self.max_iter_entry.insert(0, "10000")
        self.max_iter_entry.grid(row=5, column=1)

        self.save_button = Button(self, text="Save options", command=lambda: self.save_options(controller))
        self.save_button.grid(pady=50, row=6, columnspan=3)

        self.back_button = Button(self, text="Back", command=lambda: controller.show_frame(MainPage))
        self.back_button.grid(pady=50, row=7, columnspan=3)

    def save_options(self, controller):
        try:
            controller.M = int(self.entry_repr.get())
        except ValueError:
            messagebox.showwarning("Warning!", "Please input a positive integer for the number of representatives.")
            return
        controller.learning_algorithm = self.var.get()
        controller.architecture = self.label_first_slot.cget("text") + self.entry_second.get() + self.label_last_slot.cget("text")
        controller.architecture = [int(layer) for layer in controller.architecture.split('x')]
        controller.learning_rate = float(self.entry_lr.get())
        controller.max_iter = int(self.max_iter_entry.get())
        print(controller.M)
        print(controller.learning_algorithm)
        print(controller.architecture)
        print(controller.learning_rate)
        print(controller.max_iter)





if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
