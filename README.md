# PBIN-Packer
If you are looking for a code.pbin packer then this tool comes in handy

A PBIN Packer that only pack a folder into valid pbin file, no injection needed

# Prerequisites
Python

# Packing
`py tablelayout.py -i <folder>`

tablelayout.py will generate a .table.txt file which will have files name at parent dir first, then files at subfolder second. All alphabetical

`py buildpbin.py -i <folder> -table <table.txt generated from tablelayout> -o <outfile(ext doesnt matter)>`

Read builgpbin.py for more info on how it works(especially patching process)

# Unpacking
Since this tool only comes with packing and no unpack, you have to use WinRAR or 7z(WinRAR works better than 7z on Classic Offensive's code.pbin)
