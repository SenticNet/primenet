# from benchmark_isa import *
class RejectingDict(dict): 
    def __setitem__(self, k, v):  
        if k in self.keys():
            print (k + " is a duplicate: keep the best of the two and remove the other one\n")
        else:
            return super(RejectingDict, self).__setitem__(k, v)
        
# new_dictionary = RejectingDict(isa_benchmark) 
# new_dictionary['application_server']=32

# print(new_dictionary)
# print(new_dictionary)
# new_dictionary("tiem","ta")
