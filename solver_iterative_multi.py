import json
import multiprocessing as mp
import tkinter as tk
import tkinter.messagebox as tk_MsgBox
import tkinter.scrolledtext as tk_ScrolledText
from dataclasses import dataclass
from datetime import datetime as dt
from enum import Enum
from os import chdir, get_terminal_size, getcwd, mkdir, path
from random import random
from time import sleep
from tkinter import ttk
from typing import Any, Iterable, List

try:
    import more_itertools as miter
except ImportError:
    print(f"{'REQUIRED PACKAGE NOT FOUND':-^32}") 
    print("`more-itertools` module is required and not found")
    print("< pip install more-itertools`")
    input("> Press Enter to exit...")
    exit()

from Common import linify
from Common.DontInterrupt import DontInterrupt
from Common.Printer import Printer
from Common.str_utils import log, flog, get_hms, get_now
from Common.Timer import Timer
from Common.validators import is_np_num, is_np_num_exp
from Config import iterative_config
from Iterative.near_power import get_data_sample


APP = path.dirname(__file__)


#SECTION - Synchronization message
# used for communication between the GUI and processes
class MsgType(Enum):
    WORKER_STATUS = "WrkState"
    LOG = "Log"
    WORKER_NUM_CHUNKS_TASKS = "WrkTasksChunksDone"
    CURRENT_LEN_EXP = "CurrentLenExp"
    WORKER_EXIT = "WorkerExit"
    

@dataclass
class Msg:
    type: MsgType
    body: Any
#!SECTION


#SECTION - GUI Class
#---------------------------------------------------------------------------------------------------
#                                          GUI Class
#---------------------------------------------------------------------------------------------------
class GUI_Process_Manager(tk.Tk):
    def __init__(self, msg_queue: mp.Queue, workers: List["Worker"]):
        # interval between each GUI update event in ms
        self.update_interval = 100
        tk.Tk.__init__(self)
        self.workers = workers
        self.msg_queue = msg_queue
        
        self.title("Process manager")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.iconbitmap(default=f"{APP}\\ico\\favicon.ico")

        #------------------------------------------------
        #                Element creation
        #------------------------------------------------
        time_label = ttk.Label(self, text="00:00:00", font=("", 24), foreground="#a1a1a1")
        
        buttons_frame = ttk.Frame(self, borderwidth=1, relief=tk.RAISED, padding=[32, 8])
        pause_btn = ttk.Button(buttons_frame, text="Pause", command=self.BTN_Pause)
        resume_btn = ttk.Button(buttons_frame, text="Resume", state=tk.DISABLED, command=self.BTN_Resume)
        stop_btn = ttk.Button(buttons_frame, text="Stop", command=self.BTN_Stop)
        
        worker_info_frame = ttk.LabelFrame(self, text="Workers", borderwidth=1, relief=tk.SOLID, padding=[8, 8])
        status_frame = ttk.Frame(worker_info_frame)
        tasks_done_frame = ttk.Frame(worker_info_frame)
        current_task_frame = ttk.Frame(worker_info_frame)
        process_time_frame = ttk.Frame(worker_info_frame)
        
        status_label_list = [ttk.Label(status_frame, text=f"Wait...", padding=[4, 4]) for w in workers]
        tasks_done_label_list = [ttk.Label(tasks_done_frame, text="Wait...", padding=[0, 4]) for w in workers]
        current_task_label_list = [ttk.Label(current_task_frame, text="Wait...", padding=[0, 4]) for w in workers]
        process_time_label_list = [ttk.Label(process_time_frame, text="Wait...", padding=[0, 4]) for w in workers]

        logbox = tk_ScrolledText.ScrolledText(self, state=tk.DISABLED)
        
        #------------------------------------------------
        #                Element packing
        #------------------------------------------------
        time_label.pack(anchor=tk.N, padx=16, pady=16)
        buttons_frame.pack(anchor=tk.N, padx=8, pady=8)
        pause_btn.pack()
        resume_btn.pack()
        stop_btn.pack()
        
        worker_info_frame.pack(fill=tk.BOTH, padx=8, pady=8)
        worker_info_frame.columnconfigure(0, minsize=200)
        worker_info_frame.columnconfigure(1, minsize=150)
        worker_info_frame.columnconfigure(2, minsize=200)
        worker_info_frame.columnconfigure(3, minsize=200)

        status_frame.grid(row=0, column=0, sticky=tk.W)
        ttk.Label(status_frame, text="Status:").pack(anchor=tk.W)
        [w.pack(anchor=tk.W) for w in status_label_list]
        
        tasks_done_frame.grid(row=0, column=1, sticky=tk.W)
        ttk.Label(tasks_done_frame, text="Tasks/Chunks:").pack(anchor=tk.W)
        [w.pack(anchor=tk.W) for w in tasks_done_label_list]
        
        current_task_frame.grid(row=0, column=2, sticky=tk.W)
        ttk.Label(current_task_frame, text="Current task:").pack(anchor=tk.W)
        [w.pack(anchor=tk.W) for w in current_task_label_list]      
        
        process_time_frame.grid(row=0, column=3, sticky=tk.W)
        ttk.Label(process_time_frame, text="Task time:").pack(anchor=tk.W)
        [w.pack(anchor=tk.W) for w in process_time_label_list]
        
        logbox.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        
        #------------------------------------------------
        #                Save elements for
        #                later use
        #------------------------------------------------
        self.time_label = time_label
        self.pause_btn = pause_btn
        self.resume_btn = resume_btn
        self.stop_btn = stop_btn
        self.status_label_list = status_label_list
        self.tasks_done_label_list = tasks_done_label_list
        self.current_task_label_list = current_task_label_list
        self.process_time_label_list = process_time_label_list
        self.textbox = logbox
        
        self.process_time = [dt.now() for w in workers]
        self.exited_workers_id = []
        self.workers_alive_id = [w.id for w in workers]
        self.workers_num = len(workers)
        self.start_time = None
                     
        self.updater_id = self.after(self.update_interval, self.TH_update)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def start(self):
        self.start_time = dt.now()
        self.mainloop()
          
    def on_closing(self):
        # cancel update event
        self.after_cancel(self.updater_id)
        # unpuase all workers
        [w.resume() for w in self.workers]
        # disconnect processes from GUI thread
        # so processes will no be blocked
        [w.disconnect() for w in self.workers]
        self.destroy()

    #---------------------------------------------------------------------------
    #                            Button events
    #---------------------------------------------------------------------------
    def BTN_Pause(self):
        self.pause_btn["state"] = tk.DISABLED
        self.resume_btn["state"] = tk.ACTIVE
        for worker in self.workers:
            worker.pause()
        
    def BTN_Resume(self):
        self.pause_btn["state"] = tk.ACTIVE
        self.resume_btn["state"] = tk.DISABLED
        for worker in self.workers:
            worker.resume()
        
    def BTN_Stop(self):
        confirmation = tk_MsgBox.askyesno("Stop", "Are you sure you want to stop?")
        
        if confirmation:
            self.stop_btn["state"] = tk.DISABLED
            self.resume_btn["state"] = tk.DISABLED
            self.pause_btn["state"] = tk.DISABLED
            for worker in self.workers:
                worker.resume()
                worker.stop()
             
    #---------------------------------------------------------------------------
    #                            Update events
    #---------------------------------------------------------------------------
    def TH_update(self):
        msgs = []
        while not self.msg_queue.empty():
            msgs.append(self.msg_queue.get())
            
        for entry in msgs:
            if entry.type == MsgType.WORKER_STATUS:
                self.update_worker_status(entry.body)
            elif entry.type == MsgType.LOG:
                self.write_log(entry.body)
            elif entry.type == MsgType.WORKER_NUM_CHUNKS_TASKS:
                self.update_tasks_done(entry.body)
            elif entry.type == MsgType.CURRENT_LEN_EXP:
                self.update_current_task(entry.body)
            elif entry.type == MsgType.WORKER_EXIT:
                self.workers_alive_id.remove(entry.body)
                self.exited_workers_id.append(entry.body)
                
        for worker_id in self.workers_alive_id:
            label = self.process_time_label_list[worker_id]
            then = self.process_time[worker_id]
            label.config(text=get_hms(dt.now() - then))
        
        if len(self.workers_alive_id) != 0:   
            self.time_label.config(text=get_hms(dt.now() - self.start_time))

        self.updater_id = self.after(self.update_interval, self.TH_update)

    def update_worker_status(self, worker):
        id, name, status = worker["id"], worker["name"], worker["status"]
        if status == WorkerStates.RUNNING:
            bg = "#b6e376"
            fg = "#40821f"
        elif status == WorkerStates.PAUSED:
            bg = "#e0ca58"
            fg = "#6e4500"
        elif status == WorkerStates.ERROR:
            bg = "#fa78e6"
            fg = "#4a0d41"    
        elif status in (WorkerStates.STOPPED, WorkerStates.FINISHED):
            bg = "#e37676"
            fg = "#690808"
            
        self.status_label_list[id].config(text=f"{name}(@{id}) status: {status.value}", background=bg, foreground=fg)
 
    def write_log(self, text: str):        
        self.textbox.config(state=tk.NORMAL)
        self.textbox.insert(tk.END, f"{flog(text)}\n")
        self.textbox.config(state=tk.DISABLED)
        self.textbox.yview_moveto(1)
        
    def update_tasks_done(self, worker):
        id, tasks, chunks = worker["id"], worker["tasks"], worker["chunks"]
        self.tasks_done_label_list[id].config(text=f"{tasks}/{chunks}")
        
    def update_current_task(self, worker):
        id, num_len, exponent = worker["id"], worker["num_len"], worker["exponent"]
        self.current_task_label_list[id].config(text=f"len={num_len} : exp={exponent}")
        self.update_process_time(id)
        
    def update_process_time(self, worker_id):
        self.process_time[worker_id] = dt.now()
#!SECTION
        
        
#SECTION - Worker related classes
#---------------------------------------------------------------------------------------------------
#                                          Worker states
#---------------------------------------------------------------------------------------------------
class WorkerStates(Enum):
        RUNNING = "Running"
        PAUSED = "Paused"
        FINISHED = "Finished"
        STOPPED = "Stopped"
        ERROR = "Error"


#---------------------------------------------------------------------------------------------------
#                                          Worker Class
#---------------------------------------------------------------------------------------------------
class Worker(mp.Process):    
    def __init__(self, worker_id, worker_name: str, 
                 task_queue: mp.Queue, result_queue: mp.Queue, 
                 time_log_queue: mp.Queue, msg_queue: mp.Queue):
        self.CHUNK_SIZE = iterative_config.CHUNK_SIZE
        mp.Process.__init__(self)
        self.name = worker_name
        self.id = worker_id
        
        self.tasks = task_queue
        self.results = result_queue
        
        self.time_log_queue = time_log_queue
        
        self.msg_queue = msg_queue
        
        self.paused_event = mp.Event()
        self.stopped_event = mp.Event()
        self.resumed_event = mp.Event()
        self.exit_event = mp.Event()
        self.disconnected_event = mp.Event()
        
        self.error_occurred = mp.Event()
        self.intrrupted = mp.Event()
        # Not the best idea to use a queue to store only one value,
        # but it doesn't require synchronization from outside the object
        self.error_string = mp.Queue() 
        
        self.num_tasks_done = 0
        self.num_chunks_done = 0
        self.curr_num_len = 0
        self.curr_exp = 0
        
        self.state = None
        self.sync_status(WorkerStates.RUNNING)
    
    def run(self):
        try:
            # while any tasks available
            while not self.tasks.empty():
                self._process_task(self.tasks.get())
                self.num_tasks_done += 1
                self.sync_tasks_chunks()
                
        except Exception as e:
            self.error_occurred.set()
            self.error_string.put(f"[len:{self.curr_num_len} exp:{self.curr_exp}] -> {str(e)}")
            self.sync_status(WorkerStates.ERROR)
            sleep(random() * 3.141)
            self.sync_log(f"{self.name:<8} [len:{self.curr_num_len} exp:{self.curr_exp}] Error: {e}")
            self.send_msg(MsgType.WORKER_EXIT, msg=self.id)
            self.time_log_queue.put(f"[{get_now()}] {self.name}(@{self.id}) Error")
            self.exit_event.set()
            raise e
        
        except KeyboardInterrupt:
            self.intrrupted.set()
            self.sync_status(WorkerStates.STOPPED)
            self.sync_log(f"{self.name:<8} Stopped")
            self.send_msg(MsgType.WORKER_EXIT, msg=self.id)
            self.time_log_queue.put(f"[{get_now()}] {self.name}(@{self.id}) Stopped")
            self.exit_event.set()
            exit()
            
        else:
            self.sync_status(WorkerStates.FINISHED)
            self.sync_log(f"{self.name:<8} No tasks available. Finished")
            self.send_msg(MsgType.WORKER_EXIT, msg=self.id)
            self.time_log_queue.put(f"[{get_now()}] {self.name}(@{self.id}) Finished")
            self.exit_event.set()
        
    def _process_task(self, task: "Task"):        
        num_len, exponent = task.num_len, task.exponent
        pairs_to_check = get_data_sample(num_len, exponent)
        
        self.curr_exp = exponent
        self.curr_num_len = num_len
        self.sync_current_task()
            
        timer = Timer()
        pause_timer = Timer()
        total_downtime = 0
        timer.tic()
                   
        self.sync_log(f"{self.name:<8} [len={num_len:<4} exp={exponent:<4}] Processing...")
        
        chunks = miter.chunked(pairs_to_check, self.CHUNK_SIZE)
        for chunk in chunks:
            # check for any events before processing chunk
            if self.disconnected_event.is_set():
                # this will prevent process from blocking
                # if msg_queue consumber (aka GUI) is already destroyed
                self.msg_queue.cancel_join_thread()
                self.disconnected_event.clear()
            
            if self.paused_event.is_set():
                pause_timer.tic()
                # block until resumed_event is set
                self.wait_for_resume()
                paused_time_sec = pause_timer.toc()
                total_downtime += paused_time_sec
                paused_hms = get_hms(Timer.sec_to_timedelta(paused_time_sec))
                self.sync_log(f"{self.name:<8} [len={num_len:<4} exp={exponent:<4}] Was paused for: {paused_hms}")
                self.time_log_queue.put(f"[{get_now()}] {self.name}(@{self.id}) [len={num_len} exp={exponent}] || paused: {paused_hms}")
                    
            self._process_chunk(chunk, exponent)
            
            self.num_chunks_done += 1
            self.sync_tasks_chunks()
                    
            if self.stopped_event.is_set():
                # reroute to try-catch block inside run()
                raise KeyboardInterrupt

        else:
            elapsed_time_sec = timer.toc()
            elapsed_hms = get_hms(Timer.sec_to_timedelta(elapsed_time_sec))
            self.sync_log(f"{self.name:<8} [len={num_len:<4} exp={exponent:<4}] Elapsed: {elapsed_hms}")
            self.time_log_queue.put(f"[{get_now()}] {self.name}(@{self.id}) [len={num_len} exp={exponent}] == elapsed: {elapsed_hms}")
            if total_downtime != 0:
                cpu_time_sec = elapsed_time_sec - total_downtime
                cpu_hms = get_hms(Timer.sec_to_timedelta(cpu_time_sec))
                self.sync_log(f"{self.name:<8} [len={num_len:<4} exp={exponent:<4}] CPU time: {cpu_hms}")
                self.time_log_queue.put(f"[{get_now()}] {self.name}(@{self.id}) [len={num_len} exp={exponent}] ~~ CPU time: {cpu_hms}")
        
    def _process_chunk(self, chunk: Iterable["Task"], exponent: int):
        np_nums = []
        for pair in chunk:            
            if is_np_num_exp(pair[0], exponent):
                np_nums.append(pair[0])
                
            if is_np_num_exp(pair[1], exponent):
                np_nums.append(pair[1])
            
        if np_nums:
            self.results.put(np_nums)
              
    def wait_for_resume(self):
        self.sync_status(WorkerStates.PAUSED)
        self.sync_log(f"{self.name:<8} Paused")
        self.resumed_event.wait()
        self.sync_status(WorkerStates.RUNNING)
        self.sync_log(f"{self.name:<8} Resumed")
            
    #------------------------------------------------
    #            event based interface
    #------------------------------------------------
    def pause(self):
        # only event cab be set from outside
        # event handline should be done inside run()
        self.resumed_event.clear()
        self.paused_event.set()
        
    def resume(self):
        # only event cab be set from outside
        # event handline should be done inside run()
        self.paused_event.clear()
        self.resumed_event.set()
        
    def disconnect(self):
        # only event cab be set from outside
        # event handline should be done inside run()
        self.disconnected_event.set()
            
    def stop(self):
        # only event cab be set from outside
        # event handline should be done inside run()
        self.stopped_event.set()
        
    #------------------------------------------------
    #                send info to GUI
    #------------------------------------------------
    def send_msg(self, msg_type: MsgType, msg: any):
        self.msg_queue.put(Msg(msg_type, msg))
             
    def sync_log(self, text: str):
        log(text)
        self.send_msg(MsgType.LOG, text)
           
    def sync_status(self, status: WorkerStates):
        self.state = status
        self.send_msg(MsgType.WORKER_STATUS, {"name": self.name, "id": self.id, "status": self.state})
            
    def sync_tasks_chunks(self):
        self.send_msg(MsgType.WORKER_NUM_CHUNKS_TASKS, {"id": self.id, "tasks": self.num_tasks_done, "chunks": self.num_chunks_done})
        
    def sync_current_task(self):
        self.send_msg(MsgType.CURRENT_LEN_EXP, {"id": self.id, "num_len": self.curr_num_len, "exponent": self.curr_exp})
#!SECTION    


#--------------------------------------------------------------------------------------------------------------------------
#                                                      STARTUP
#--------------------------------------------------------------------------------------------------------------------------
@dataclass
class Task:
    num_len: int
    exponent: int

def get_tasks(min_digits: int, max_digits: int,
              lower_exp_limit: int, upper_exp_limit: int):
    tasks = []
    for num_len in range(min_digits, max_digits+1):
        for exp in range(num_len-lower_exp_limit, num_len+upper_exp_limit+1):
            tasks.append(Task(num_len, exp))
                         
    return tasks
    

#------------------------------------------------
#                MAIN
#------------------------------------------------
def main():
    MIN_DIGITS      = iterative_config.MIN_DIGITS
    MAX_DIGITS      = iterative_config.MAX_DIGITS
    UEXPL           = iterative_config.UPPER_EXP_LIMIT
    LEXPL           = iterative_config.LOWER_EXP_LIMIT   
    NPRC            = iterative_config.PROCESSES
    USE_GUI         = iterative_config.USE_GUI
    WIDTH           = get_terminal_size().columns // 2
    
    
    chdir(APP)
    if not path.exists("dumps"):
        mkdir("dumps")
    chdir("dumps")
    
    start_date = dt.now()
    start_date_string = get_now()
        
    msg_queue = mp.Queue()
    task_queue = mp.Queue()
    result_queue = mp.Queue()
    time_log_queue = mp.Queue()
    
    task_queue.cancel_join_thread()
    msg_queue.cancel_join_thread()
    result_queue.cancel_join_thread()
    time_log_queue.cancel_join_thread()
    
    for task in get_tasks(MIN_DIGITS, MAX_DIGITS, LEXPL, UEXPL):
        task_queue.put(task)
        
    workers = [Worker(id, f"proc_{id+1}", task_queue, result_queue, time_log_queue, msg_queue) for id in range(0, NPRC)]
    if USE_GUI:
        gui = GUI_Process_Manager(msg_queue, workers)
    
    was_interrupted = False
    error_occured = False
    whois_interrupted: List[Worker] = []
    whois_errored: List[Worker] = []
    results = []
    time_log = []
    
    
    print(f"#{'START':-^{WIDTH}}#")    
    with Timer("MAIN"):
        with DontInterrupt():
            [worker.start() for worker in workers]
            
            if USE_GUI:
                gui.start()
            else:
                [worker.disconnect() for worker in workers]
                
            # using .join() or .is_alive() to wait for all workers to finish 
            # is impossibe due to it will create a deadlock situation
            # using manually created event instead
            any_alive = True
            while any_alive:
                any_alive = not all([worker.exit_event.is_set() for worker in workers])
                sleep(1)
                
            error_occured = any([worker.error_occurred.is_set() for worker in workers])
            was_interrupted = any([worker.intrrupted.is_set() for worker in workers])
            
            for worker in workers:
                if worker.intrrupted.is_set():
                    whois_interrupted.append(worker)
                if worker.error_occurred.is_set():
                    whois_errored.append(worker)
                    
            while not result_queue.empty():
                results.extend(result_queue.get())
                
            while not time_log_queue.empty():
                time_log.append(time_log_queue.get())
                
            [worker.join() for worker in workers]
                
    print(f"#{'END':-^{WIDTH}}#")

    
    end_date_string = get_now()
    elapsed = dt.now() - start_date
    
    valid_numbers = sorted(list(set(results)))
    sum_value = 0
    extra_validation_results = [False]
    longest_num_len = 0

    
    print()


    if len(valid_numbers) > 0:
        sum_value = sum(valid_numbers)
        extra_validation_results = [is_np_num(num) for num in valid_numbers]
        longest_num_len = len(str(valid_numbers[-1]))
    
        printer = Printer(2, WIDTH // 2) 
        
        print(f"#{'VALID NUMBERS':-^{WIDTH}}#")  
        printer.printf(["#", "number"])
        printer.printf(linify(enumerate(valid_numbers, 1)))
        
        print(f"SUM = {sum_value}")
        
        print(f"#{'EXTRA_VALIDATION':-^{WIDTH}}#") 
        printer.printf(["number", "passed"])
        printer.printf(linify(zip(valid_numbers, extra_validation_results)))
    
    
    dump = {
        "config": {
            "min digits":                       MIN_DIGITS,
            "max digits":                       MAX_DIGITS,
            "number of processes":              NPRC,
            "upper exponent limit":             UEXPL,
            "lower exponent limit":             LEXPL,
        },
        "time info": {
            "start date":                       start_date_string,
            "end date":                         end_date_string,
            "elapsed":                          get_hms(elapsed),
            "log":                              time_log
        },
        "numbers info": {
            "numbers":                          valid_numbers,
            "quantity of valid integers":       len(valid_numbers),
            "longest integer length":           longest_num_len,
            "sum value":                        sum_value,
            "extra validation passed":          False not in extra_validation_results,
        },
        "interrupts": {
            "was interrupted":                  was_interrupted,
        },
        "errors": {
            "error occurred":                   error_occured
        }
    }
    
    if error_occured:
        dump["errors"]["errors occured in"] = [f"{w.name}(@{w.id}):{w.error_string.get()}" for w in whois_errored]
        
    if was_interrupted:
        dump["interrupts"]["interrupted workers"] = [f"{w.name}(@{w.id})" for w in whois_interrupted]
    
    json_dump = json.dumps(dump, indent=4)
    
    
    try:
        name_part = f"[F{MIN_DIGITS}_T{MAX_DIGITS}] [U{UEXPL}_L{LEXPL}]"
        name_part += "_I" if was_interrupted else ""
        name_part += "_E" if error_occured else ""
        with open(f"{name_part}_dump.json", 'w') as dump_file:
            dump_file.write(json_dump)
    except Exception as e:
        log(f"Ops! Not dumped. Error: {e}")
    else:
        log(f"Dumped to {getcwd()} -> {dump_file.name}")
        
    input("> Press Enter to exit...")


if __name__ == "__main__":
    mp.set_start_method("spawn")
    main()
