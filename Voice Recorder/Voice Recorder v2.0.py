from scipy.io.wavfile import write
from colorama import Fore
import sounddevice as sd 
import numpy as np
import threading


freq = 44100

final_recording_name = "Recording_1.wav"

recordings = []

state = "stopped"


def main():
   command_thread = threading.Thread(target=handle_commands)
   command_thread.start()


   

def record():
   global recordings, state

   state = "recording"

   while state == "recording":
      recording_segment = sd.rec(int(freq), samplerate=freq, channels=1)

      sd.wait()

      recordings.append(recording_segment)


def handle_commands():
   global state

   print_help()

   while True:
      print_current_state()

      command = input(Fore.MAGENTA + "Command (write 'help' if you need): " + Fore.RESET).lower().strip()

      match command:

         case "start" | "r":
            if state != "recording":
               print()
               print(Fore.BLACK + "========================")
               print(Fore.GREEN + "--- Recording started!")
               print(Fore.BLACK + "========================" + Fore.RESET)

               threading.Thread(target=record).start()

            else:
               print(Fore.RED + "<!> Recording is already started" + Fore.RESET)

         case "pause" | "p":
            if state == "recording":
               print()
               print(Fore.BLACK +"========================")
               print(Fore.YELLOW + "--- Recording paused!")
               print(Fore.BLACK + "========================" + Fore.RESET)

               state = "paused"

            else:
               print(Fore.RED + "<!> Recording is not started" + Fore.RESET)

         case "stop" | "s":
            if state == "recording" or state == "paused":
               print()
               print(Fore.BLACK + "========================")
               print(Fore.RED + "--- Recording stopped!")
               print(Fore.BLACK + "========================" + Fore.RESET)

               state = "stopped"
               save_recording()

            else:
               print(Fore.RED + "<!> Recording is not started or paused" + Fore.RESET)

         case "help" | "h":
            print_help()

         case "exit" | "e":
            print()
            print(Fore.CYAN + "Thanks for using this recorder :)" + Fore.RESET)
            break

         case _:
            print()
            print(Fore.RED + "Invalid command")
            print(Fore.WHITE + "Please enter one of the commands mentioned above" + Fore.RESET)


def save_recording():
   global recordings, state

   if state == "stopped":
      final_recording = np.concatenate(recordings, axis=0)

      write(final_recording_name, freq, final_recording)

      print()
      print(Fore.GREEN + f"The recording was successfully saved as {final_recording_name}" + Fore.RESET)

   else:
      print(Fore.RED + "Failed to save the recording: whether the recording was not stopped or an error occurred" + Fore.RESET)


def print_help():
   print()
   print(Fore.MAGENTA + "---------- Recorder Commands ----------" + Fore.RESET)
   print(Fore.CYAN + "  start / r : Start recording")
   print("  pause / p : Pause the recording")
   print("  stop / s : Stop and save the recording" + Fore.RESET)
   print()
   print(Fore.YELLOW + "  exit / e : exit the program" + Fore.RESET)


def print_current_state():
   global state

   print()
   
   if state == "recording":
      print(Fore.CYAN + "== Current state: " + Fore.GREEN + state.capitalize() + Fore.RESET)
   elif state == "paused":
      print(Fore.CYAN + "== Current state: " + Fore.YELLOW + state.capitalize() + Fore.RESET)
   else:
      print(Fore.CYAN + "== Current state: " + Fore.RED + state.capitalize() + Fore.RESET)

   print()



if __name__ == "__main__":
   main()