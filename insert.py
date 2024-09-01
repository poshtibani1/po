import os
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

rs = requests.Session()
rs.trust_env = False

print("[!] Changes to all .txt files will be applied from \"insert.txt\"")

try:
    insert_file = open("./insert.txt", "r", encoding="utf-8")
    insert_lines = insert_file.readlines()
    files = [os.path.join("./", f) for f in os.listdir("./") if os.path.isfile(os.path.join("./", f)) and f.lower().endswith(".txt") and f.lower() != "insert.txt"]
    for file in files:
        try:
            f = open(file, "r+", encoding="utf-8")
            lines = f.readlines()
            f.close()
            for i in range(len(insert_lines), 0, -1):
                if insert_lines[i-1].strip().lower().startswith("http://") or insert_lines[i-1].strip().lower().startswith("https://"):
                    try:
                        request = rs.get(insert_lines[i-1].strip(), timeout=30, allow_redirects=True, verify=False)
                        rt = request.text
                        rt_list = rt.split("\n")
                        for r in range(len(rt_list), 0, -1):
                            if rt_list[r-1].strip() != "":
                                lines.insert(1, rt_list[r-1].strip())
                    except:
                        print(f"[X] Error link: {insert_lines[i-1].strip()}")
                elif insert_lines[i-1].strip() == "":
                    pass
                else:
                    lines.insert(1, insert_lines[i-1].strip())
            f = open(file, "w", encoding="utf-8")
            f.write("\n".join([f.strip() for f in lines]))
            f.close()
            print(f"[ok] Inserted: {os.path.basename(file)}")
        except:
            print(f"[X] Error: {os.path.basename(file)}")
    insert_file.close()
except:
    print("[X] There's no \"insert.txt\" file")