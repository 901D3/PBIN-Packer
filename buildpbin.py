import zipfile
import argparse
from pathlib import Path

#buildpbin.py -i <folder> -table <table file> -o <outfile(ext doesnt matter)>

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="Root folder of source files", required=True)
parser.add_argument("-table", help="Path to .table.txt", required=True)
parser.add_argument("-o", help="Output file", required=True)
parser.add_argument("-log", help="Enable logging", action="store_true")
args = parser.parse_args()

root_dir = Path(args.i).resolve()
table_file = Path(args.table)
output_zip = Path(args.o)
log = args.log
with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_STORED) as zipf:
    with open(table_file, "r", encoding="utf-8") as f:
        for line in f:
            arc_path = line.strip().replace("\\", "/")
            if not arc_path:
                continue

            relative_path = Path(arc_path)
            try:
                relative_subpath = relative_path.relative_to(root_dir.name)
            except ValueError:
                relative_subpath = relative_path
            real_file = root_dir / relative_subpath
            if args.log == True: 
                print(f"Processing: {arc_path}")
            if real_file.is_file():
                zipf.write(real_file, arcname=arc_path)
            else:
                print(f"Skipping: {arc_path}")

with open(output_zip, "r+b") as f: #zip patcher to valid pbin
    data = bytearray(f.read())
    i = 0
    length = len(data)
    data = bytearray(bytes.fromhex('50 41 4E 02' + '00 ' * 512) + data) #insert PAN\x02 and 512B of 0s
    while i < length - 4:
        if args.log == True: 
            print(hex(i))
        i2 = i
        if data[i:i+4] == b'\x50\x4B\x03\x04': #search for PK\x03\x04
            if args.log == True:
                print(f"PK\x03\x04\x0A\x00 found at {hex(i2 + 1)}")
            data[i+4:i+6] = b'\x0A\x00' #overwrite next 2 bytes to \x0A\x00
        elif data[i:i+4] == b'\x50\x4B\x01\x02': #search for PK\x01\x02
            if args.log == True:
                print(f"PK\x01\x02\x0A\x00\x14\x00 found at {hex(i2 + 1)}")
            data[i+4:i+8] = b'\x14\x00\x0A\x00' #overwrite next 4 bytes to \x14\x00\x0A\x00
        i += 1
    eocd_sig = b'\x50\x4B\x05\x06' #search for PK\x05\x06 (EOCD)
    eocd_pos = data.rfind(eocd_sig)
    if eocd_pos == -1:
        raise ValueError("EOCD not found in file.")
    data[eocd_pos + 20:eocd_pos + 22] = (32).to_bytes(2, 'little')
    comment = bytes.fromhex('58 5A 50 31 20 30' + '00 ' * 26 + '36 00 00 02') #overwrite 32 bytes to this magic "XZP1 0" starting from P and count to the right 22 bytes
    #this cool metadata included in csgo vanilla code.pbin and classic offensive code.pbin. 1 byte before 36 00 00 02, you can put anything and it doesnt affect the ui
    comment_pos = eocd_pos + 22
    data = (
        data[:comment_pos] + comment + data[comment_pos + len(comment):]
    )
    f.seek(0)
    f.write(data)
    f.truncate()