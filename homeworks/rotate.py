#!/usr/bin/python

def array_left_rotation(n, length):
    nums = range(1,int(length)+1)
    print "start with", nums;
    for x in range(1, int(n)+1):

        tmp = nums[0];
        for index, name in enumerate(nums):
            if (index+1) < len(nums):
                nums[index] = nums[index+1];
            else:
                #last element
                nums[index] = tmp;
        #print "rotation #", x, "now have", nums
    print nums;

print "Welcome to rotator, enter number of rotations"
rotations = raw_input();
print "enter size of array to rotate"
mylen =raw_input();

array_left_rotation(rotations, mylen);
