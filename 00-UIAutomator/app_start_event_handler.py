import time
from random import randint
import csv

def get_iphone_size(device_name):
    with open('iphone_info.csv', 'r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        if row['name'] == device_name:
          return row['size']


def get_random_value(size):
    size = size.split('x')
    x_size = float(size[0])
    y_size = float(size[1])
    x = randint(1+30, int(x_size)-30)
    y = randint(1+30, int(y_size)-30)
    print(x, y)
    return x, y


def write_info(csv_name, x, y, time, loading_time, is_first):
    file_name = csv_name+".csv"
    with open(file_name, 'a') as csvfile:
      fieldnames = ['x_axis', 'y_axis', 'time', 'loading-time']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      if is_first:
        writer.writeheader()
      writer.writerow({'x_axis':x, 'y_axis':y, \
                       'time':time,'loading-time':loading_time})


def main(args):
     size = get_iphone_size(args.name)
     count = args.time
     start_time = time.time()
     for count in range(0, count):
       loading_start_time = time.time()
       x_axis, y_axis = get_random_value(size)
       result = input("click? - ")
       time.sleep(10)
       print("sleep end")
       cur_time = time.time() - start_time
       loading_time = time.time() - loading_start_time
       if count == 0:
         write_info(args.csv, x_axis, y_axis, cur_time, loading_time, True)
       else:
         write_info(args.csv, x_axis, y_axis, cur_time, loading_time, False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", 
                        required=True,
                        help="input name of iphone model")
    parser.add_argument("-c", "--csv",
                        required=True,
                        help="input output csv name")
    parser.add_argument("-t", "--time",
                        required=True,
                        type=int,
                        help="set experiment time")
    args = parser.parse_args()
    main(args)

