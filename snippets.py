# Top 10 memory users
import sys
def sizeof_fmt(num, suffix='B'):
    ''' by Fred Cirera,  https://stackoverflow.com/a/1094933/1870254, modified'''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

for name, size in sorted(((name, sys.getsizeof(value)) for name, value in locals().items()),
                         key= lambda x: -x[1])[:10]:
    print("{:>30}: {:>8}".format(name, sizeof_fmt(size)))
    
    
    
# Show progress bar
def update_progress(part, total=100, barLength=50):
    progress = (float(part)) / total
    status = ""
    if progress < 0:
        progress = 0
        status = "Negative...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rProgress: [{0}] ({2}/{3}) {1}% {4}".format("#"*block + "-"*(barLength-block), 
                                              int(progress*100), part, total,
                                              status)
    sys.stdout.write(text)
    sys.stdout.flush()
    
    
    
# Read a CSV file to Dataframe, filtering on one or two columns
# column name is string, value is a list of values
def read_csv_filtered(file, key1, value1, key2=None, value2=None, chuncksize=100000):
    iter_csv = pd.read_csv(file, iterator=True, chunksize=chuncksize, low_memory=False)
    if key2:
        df = pd.concat([chk[(chk[key1].isin(value1)) & (chk[key2].isin(value2))] for chk in iter_csv])
    else:
        df = pd.concat([chk[chk[key1].isin(value1)] for chk in iter_csv])
    return df


# Log function
logfile = "log.txt"
def log_line(desc, val):
    with open(logfile, "a") as myfile:
        myfile.write(desc + "," + str(val) + "\n")
def clear_log():
    with open(logfile, "w") as myfile:
        myfile.write("")    

        
# Check presence
def is_present(valname):
    return valname in locals()


# Get unique items with count from a list
mylist=['a', 'b', 'a']
sorted(sorted([(x, mylist.count(x)) for x in list(set(mylist))]), key=lambda y: y[1])
