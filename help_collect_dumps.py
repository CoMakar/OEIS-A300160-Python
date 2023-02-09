import json
from os import chdir, getcwd, listdir, path

from Common import linify
from Common.Printer import Printer
from Common.str_utils import get_now, log
from Helpers.near_power_helper import get_np_exponent


def main():
    APP = path.dirname(__file__)
    
    chdir(APP)
    if not path.exists("dumps"):
        print("Directory `dumps` does not exist")
        input("> Press Enter to exit...")
        exit()
        
    chdir("dumps")
    files = listdir()
    files = list(filter(lambda f: f.endswith("dump.json"), files))
    
    valid_numbers = []
    bad = []
    if files:   
        for file in files:
            with open(file, 'r') as dump_file:
                log(f"{dump_file.name:<32} File found")
                collected_numbers_information = dump_file.read()
                try:
                    json_dump = json.loads(collected_numbers_information) 
                    numbers = json_dump.get("numbers", None)
                    if numbers is not None and len(numbers) != 0:
                        log(f"{dump_file.name:<32} [{len(numbers)}] numbers collected")
                        valid_numbers.extend(numbers)
                    else:
                        log(f"{dump_file.name:<32} [!] no numbers")
                    
                except json.JSONDecodeError as e:
                    log(f"{dump_file.name:<32} Contains invalid JSON: {e}")
                    bad.append(dump_file.name)
        
        valid_numbers = sorted(set(valid_numbers))
        collected_numbers_information = [{"n": pos, "number": num, "length": length, "exponent": exp, "correlation": exp - length} 
                for pos, num, length, exp 
                in zip(
                    range(1, len(valid_numbers)+1), 
                    valid_numbers,
                    map(lambda n: len(str(n)), valid_numbers),
                    map(get_np_exponent, valid_numbers)
                    )]
        
        printer = Printer(5, 16)
        printer.printf(["#", "number", "length", "exponent", "correlation"])
        printer.printf(linify([i.values() for i in collected_numbers_information]))
        
        dump = {"numbers": collected_numbers_information}
        json_dump = json.dumps(dump, indent=4)
        now_date = get_now().replace(":", "_")
        try:
            with open(f"collected_numbers {now_date}.json", 'w') as dump_file:
                dump_file.write(json_dump)
        except Exception as e:
            print(f"Ops! Not dumped. Error: {e}")
        else:
            print(f"Dumped to {getcwd()} -> {dump_file.name}")
    else:
        print("No files found")
    
    input("> Press Enter to exit...")
    
            
if __name__ == "__main__":
    main()
