import random


class Infection:
    def modify_src(self):
        self.output_file.write('DEF ' + self.output_dir.split("\\")[-1].split(".")[0] + '() \n')
        #todo write warning as a KSS message (see 'KSS_82_messages_en.pdf') instead of a line in the file...
        self.output_file.write(';This file has been infected... run at your own risk!!\n')

        while self.i < len(self.input_file):
            if self.debug: print(str(self.i) + " ", end="")
            current = self.input_file[self.i].split()
            if current:
                if self.debug: print("Line in code: " + str(self.i + 1))
                #todo parse E1 value from file (if want to do the wiggles)...
                if current[0][:7] == "$VEL.CP" and self.default_velocity is None:
                    if self.debug: print("Getting exiting baseline velocity")
                    self.default_velocity = current[0][8:]
                    self.output_file.write(self.input_file[self.i])
                    self.i += 1
                elif current[0][:7] == "$ACC.CP" and self.default_acceleration is None:
                    if self.debug: print("Getting existing baseline acceleration")
                    self.default_acceleration = current[2]
                    self.output_file.write(self.input_file[self.i])
                    self.i += 1
                elif current[0][5:] == "Path":
                    if current[2] == "Toolpath":
                        if self.debug: print("Checking if in path - TRUE")
                        self.path = True
                        self.output_file.write(self.input_file[self.i])
                        self.i += 1
                    elif (current[2] == "LeadIn") or (current[2] == "Traverse") or (current[2] == "LeadOut"):
                        if self.debug: print("Checking if in path - FALSE")
                        self.path = False
                        self.output_file.write(self.input_file[self.i])
                        self.i += 1
                    else:
                        if self.debug: print("Atypical Path type - won't chang self.path")
                        self.output_file.write(self.input_file[self.i])
                        self.i += 1

                elif current[0] == "LIN":
                    #todo better way to handle the order in which viruses are called???
                    if self.path:
                        try:
                            max_skip = self.input_file[self.i:].index(";####Path 0 LeadOut\n") - 1
                        except:
                            max_skip = 0
                            if self.debug: print("Failure to find program length")

                        a, b = self.jitters.infect(self.output_file, self.input_file[self.i], self.default_acceleration,
                                                   self.default_velocity)
                        if a:
                            if self.debug: print("Jitters")
                            if b > max_skip > 0: b = max_skip
                            self.i += b
                        elif not a:
                            c, d = self.amnesia.infect(self.output_file)
                            if c:
                                if self.debug: print("Amnesia")
                                if d > max_skip > 0: d = max_skip
                                self.i += d
                            elif not c:
                                e, f = self.decay.infect(self.output_file, self.input_file[self.i])
                                if e:
                                    if self.debug: print("Decay")
                                    if f > max_skip > 0: f = max_skip
                                    self.i += f
                                else:
                                    if self.debug: print("No infection")
                                    self.output_file.write(self.input_file[self.i])
                                    self.i += 1
                    else:
                        if self.debug: print("No infections on lead-in/lead-out/traverse")
                        self.output_file.write(self.input_file[self.i])
                        self.i += 1
                else:
                    if self.debug: print("No criteria met")
                    self.output_file.write(self.input_file[self.i])
                    self.i += 1

            else:
                if self.debug: print("Blank line")
                self.output_file.write(self.input_file[self.i])
                self.i += 1

        self.output_file.close()

    def __init__(self, krl_input, jitter_percent=None, amnesia_percent=None, decay_percent=None):
        # handle input directory/file
        self.input_dir = krl_input
        self.input_file = open(self.input_dir, 'r').readlines()

        #handle output directory/file
        self.output_dir = krl_input[:-4] + "_infected" + krl_input[-4:]
        self.output_file = open(self.output_dir, 'w')

        #initialize infections
        self.jitters = Jitter(jitter_percent)
        self.amnesia = Amnesia(amnesia_percent)
        self.decay = Decay(decay_percent)

        #initialize other things
        self.i = 1
        self.default_velocity = None
        self.default_acceleration = None
        self.path = False
        self.debug = False


class Virus:
    def __init__(self, percentage):
        self.percentage = percentage if percentage is not None else 0.1

    def _check(self):
        return random.random() < self.percentage


class Jitter(Virus):
    def __init__(self, percentage=None, velocity=None, acceleration=None, distance=None, wait=None,
                 skip=None):
        super(Jitter, self).__init__(percentage)
        self.velocity = velocity if velocity is not None else 0.25
        self.acceleration = acceleration if acceleration is not None else 1
        self.distance = distance if distance is not None else 100
        self.wait = wait if wait is not None else 15
        self.skip = skip if skip is not None else 2

    def infect(self, out_file, in_line, in_accel, in_velo):
        if self._check():
            out_file.write(';*****INFECTED WITH THE JITTERS!*****\n')
            out_file.write(';EXTRUDE = FALSE\n')  # turn off extruder
            out_file.write('$IPO_MODE = #TCP\n')  # set to tool coordinates
            out_file.write(''.join(['$VEL.CP = ', str(self.velocity), '\n']))  # set new velocity
            out_file.write(''.join(['$ACC.CP = ', str(self.acceleration), '\n']))  # set new acceleration
            out_file.write(''.join(['LIN_REL { Z ', str(self.distance / 5), ' } C_DIS\n']))
            out_file.write(''.join(['$ACC.CP = ', str(in_accel), '\n']))  # reset default acceleration
            out_file.write(''.join(['LIN_REL { Z ', str(self.distance), ' } C_DIS\n']))
            out_file.write(''.join(['LIN_REL { Z -', str(self.distance / 3), ' } C_DIS\n']))
            out_file.write(''.join(['LIN_REL { Z ', str(self.distance / 3), ' } C_DIS\n']))
            out_file.write(''.join(['LIN_REL { Z -', str(self.distance / 5), ' } C_DIS\n']))
            out_file.write(''.join(['LIN_REL { Z ', str(self.distance / 5), ' }\n']))
            out_file.write(''.join(['WAIT SEC ', str(self.wait), '\n']))
            out_file.write('$IPO_MODE = #BASE\n')  # reset to base coordinates
            out_file.write(''.join(['$VEL.CP = ', str(in_velo), '\n']))  # reset default velocity
            out_file.write(in_line)  # continue to proper position
            out_file.write(';EXTRUDE = TRUE\n')  # turn on extruder
            out_file.write(';****CURED OF THE JITTERS!***\n')
            return True, self.skip
        else:
            return False, None


class Amnesia(Virus):
    def __init__(self, percentage=None, skip=None):
        super(Amnesia, self).__init__(percentage)
        self.skip = skip if skip is not None else 4

    def infect(self, out_file):
        if self._check():
            out_file.write(';**********AMNESIA?*********\n')
            return True, self.skip
        else:
            return False, None


class Decay(Virus):
    def __init__(self, percentage=None, delay=None):
        super(Decay, self).__init__(percentage)
        self.delay = delay if delay is not None else 2

    def infect(self, out_file, in_line):
        if self._check():
            out_file.write(';************DECAY**********\n')
            out_file.write('WAIT SEC ' + str(self.delay) + '\n')
            out_file.write(in_line)
            return True, 1
        else:
            return False, None

# MAIN FUNCTION
if __name__ == "__main__":

    import os

    print("Voight-Kampff")
    print("A program for exploring neurological disorders in industrial robots")
    print("\nWARNING!!\nAuthor is not liable for equipment damages that may result from running code generated by "
          "this program\nUSE AT YOUR OWN RISK!\n\n")

    file_dir = None

    while True:
        file_dir = input("Enter file path: ").strip('"')
        try:
            assert os.path.exists(file_dir), "No file found in given directory."
            assert file_dir.lower().endswith('.src'), "Supplied file is not a KRL file."
            break
        except AssertionError as e:
            print(e.args[0] + "\n")

    if file_dir:
        my_test = Infection(file_dir)
        my_test.debug = True
        my_test.modify_src()
        print("Infection complete")
