import VoightKampff as VK
import tkinter as tk
from tkinter import messagebox, filedialog


class VKGui:
    version = 1.0

    def __init__(self, master):
        master.title('Voight-Kampff')
        master.resizable(width=False, height=False)
        self.main_frame = tk.Frame(master,
                                   width=100,
                                   height=100)
        self.main_frame.pack()

        self.controls = {}
        self.create_widgets(self.main_frame)

    def create_widgets(self, main):

        ### FILE SELECTION ###
        self.b1 = tk.Button(main,
                            text='Select file',
                            underline=0,
                            command=self.open)
        #todo get key binding to work properly!
        self.b1.bind('s', self.key_handler)
        self.b1.grid(row=0, padx=10, pady=15, sticky='WE')

        self.e1 = tk.Entry(main)
        self.e1.insert(0, "No file selected...")
        self.e1.configure(state='readonly')
        self.e1.grid(row=0, column=1, padx=10, columnspan=3, sticky='WE')


        ### LABELFRAMES ###
        self.v2 = tk.LabelFrame(main, text='Amnesia', padx=10, pady=10)
        self.v2.grid_columnconfigure(0, minsize=100)
        self.v2.grid(row=1, padx=10, pady=5, columnspan=4)

        self.v3 = tk.LabelFrame(main, text='Decay', padx=10, pady=10)
        self.v3.columnconfigure(0, minsize=100)
        self.v3.grid(row=2, padx=10, pady=5, columnspan=4)

        self.v1 = tk.LabelFrame(main, text='Jitter', padx=10, pady=10)
        self.v1.columnconfigure(0, minsize=100)
        self.v1.grid(row=3, padx=10, pady=5, columnspan=4)

        ## CONTROLS ##
        self.controls[('jitter', 'percent')] = VKControl(self.v1, "Percent")
        self.controls[('jitter', 'percent')].slider.config(to=1)
        self.controls[('jitter', 'percent')].grid(0)

        self.controls[('jitter', 'velocity')] = VKControl(self.v1, "Velocity")
        self.controls[('jitter', 'velocity')].slider.config(from_=0.1, to=1)
        self.controls[('jitter', 'velocity')].grid(1)

        self.controls[('jitter', 'acceleration')] = VKControl(self.v1, "Acceleration")
        self.controls[('jitter', 'acceleration')].slider.config(from_=1, to=5)
        self.controls[('jitter', 'acceleration')].grid(2)

        self.controls[('jitter', 'distance')] = VKControl(self.v1, "Distance")
        self.controls[('jitter', 'distance')].slider.config(from_=10, to=99)
        self.controls[('jitter', 'distance')].grid(3)

        self.controls[('jitter', 'wait')] = VKControl(self.v1, "Wait")
        self.controls[('jitter', 'wait')].slider.config(to=60, resolution=1)
        self.controls[('jitter', 'wait')].grid(4)

        self.controls[('jitter', 'skip')] = VKControl(self.v1, "Skip")
        self.controls[('jitter', 'skip')].slider.config(from_=1, to=20, resolution=1)
        self.controls[('jitter', 'skip')].grid(5)

        self.controls[('amnesia', 'percent')] = VKControl(self.v2, "Percent")
        self.controls[('amnesia', 'percent')].slider.config(to=1)
        self.controls[('amnesia', 'percent')].grid(0)

        self.controls[('amnesia', 'skip')] = VKControl(self.v2, "Skip")
        self.controls[('amnesia', 'skip')].slider.config(from_=5, to=50, resolution=1)
        self.controls[('amnesia', 'skip')].grid(1)

        self.controls[('decay', 'percent')] = VKControl(self.v3, "Percent")
        self.controls[('decay', 'percent')].slider.config(to=1)
        self.controls[('decay', 'percent')].grid(0)

        self.controls[('decay', 'wait')] = VKControl(self.v3, "Wait")
        self.controls[('decay', 'wait')].slider.config(from_=1, to=10, resolution=1)
        self.controls[('decay', 'wait')].grid(1)

        ### OTHER FUNCTIONS ###
        self.b2 = tk.Button(main,
                            text='Run VK',
                            command=self.execute,
                            underline=0,)
        self.b2.grid(row=4, padx=10, pady=5, sticky='WE')

        self.b3 = tk.Button(main,
                            text='Export Settings',
                            command=self.save,
                            underline=0)
        self.b3.grid(row=4, column=1, padx=2, pady=5, sticky='E')

        self.b4 = tk.Button(main,
                            text='Import Settings',
                            command=self.imports,
                            underline=0)
        self.b4.grid(row=4, column=2, padx=2, pady=5, sticky='E')

        self.b5 = tk.Button(main,
                            text='About',
                            command=self.info,
                            underline=0)
        self.b5.grid(row=4, column=3, padx=10, pady=5, sticky='E')

    def key_handler(self, event):
        #todo get keypress event handler working properly
        print("keypress")

    def open(self):
        options = {'title': 'Select file to open',
                   'defaultextension': '.src',
                   'filetypes': [('KRL files', '.src')],
                   'initialdir': 'C:\\'}
        update_text = filedialog.askopenfilename(**options)

        if update_text:
            self.e1.configure(state='normal')
            self.e1.delete(0, tk.END)
            self.e1.insert(0, update_text)
            self.e1.configure(state='readonly')
        else:
            pass

    def save(self):
        options = {'title': 'Export settings as',
                   'defaultextension': '.vkdat',
                   'filetypes': [('VK data files', '.vkdat')],
                   'initialdir': 'C:\\'}
        file_name = filedialog.asksaveasfilename(**options)

        if file_name:
            export_file = open(file_name, 'w')
            export_file.write('Voight-Kampff, v{0}\n\n'.format(self.version))
            export_file.write(self.e1.get() + '\n')
            for i in sorted(self.controls.keys()):
                export_file.write('{0}, {1}, {2}\n'.format(i[0], i[1], self.controls[i].slider.get()))
            export_file.close()
        else:
            pass

    def imports(self):
        options = {'title': 'Select settings file to import',
                   'defaultextension': '.vkdat',
                   'filetypes': [('VK data files', '.vkdat')],
                   'initialdir': 'C:\\'}
        file_dir = filedialog.askopenfilename(**options)

        if file_dir:
            import_file = open(file_dir, 'r')
            file_lines = import_file.read().splitlines()

            self.e1.configure(state='normal')
            self.e1.delete(0, tk.END)
            self.e1.insert(0, file_lines[2])
            self.e1.configure(state='readonly')

            for line in file_lines[3:]:
                items = line.split(', ')
                self.controls[(items[0], items[1])].slider.set(float(items[2]))
        else:
            pass

    def info(self):
        messagebox.showinfo("Voight-Kampff v1.0",
                            "Developed by Aaron M "
                            "Willette\ngithub.com/pixelwhore/Voight-Kampff\ncontact@pixelwhore.com"
                            "\n\nLicensed under the GNU General Public License (GPL) version 3.\nThis means you "
                            "are free to use it and modify it, but if you distribute your modifications you "
                            "must distribute the source of your modifications as well.")

    def execute(self):
        if not self.e1.get() == "No file selected...":
            my_infection = VK.Infection(self.e1.get(),
                                        float(self.controls[('jitter', 'percent')].slider.get()),
                                        float(self.controls[('amnesia', 'percent')].slider.get()),
                                        float(self.controls[('decay', 'percent')].slider.get()))

            my_infection.amnesia.skip = int(self.controls[('amnesia', 'skip')].slider.get())
            my_infection.decay.delay = int(self.controls[('decay', 'wait')].slider.get())
            my_infection.jitters.velocity = float(self.controls[('jitter', 'velocity')].slider.get())
            my_infection.jitters.acceleration = float(self.controls[('jitter', 'acceleration')].slider.get())
            my_infection.jitters.distance = float(self.controls[('jitter', 'distance')].slider.get())
            my_infection.jitters.wait = int(self.controls[('jitter', 'wait')].slider.get())
            my_infection.jitters.skip = int(self.controls[('jitter', 'skip')].slider.get())

            #my_infection.debug = True
            my_infection.modify_src()

            messagebox.showwarning("Infection complete!",
                                   "The SRC file has been modified, run at your own risk!")
        else:
            pass



class VKControl:

    def __init__(self, parent, label_text):
        self.label = tk.Label(parent, text=label_text + ":")
        self.value = tk.Label(parent, width=4)
        self.slider = tk.Scale(parent,
                               showvalue=0,
                               orient="horizontal",
                               digits=3,
                               resolution=0.01,
                               length=150,
                               command=self.update)

    def grid(self, my_row):
        self.label.grid(row=my_row, sticky="E")
        self.value.grid(row=my_row, column=1, sticky="E")
        self.slider.grid(row=my_row, column=2, sticky="W")

    def update(self, new_value):
        update_text = "{0: >5.2f}".format(float(new_value))
        self.value.configure(text=update_text)



if __name__ == "__main__":
    root = tk.Tk()
    main_gui = VKGui(root)
    root.mainloop()
