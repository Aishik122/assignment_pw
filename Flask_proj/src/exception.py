import sys

def error_message_detail(error,error_detail:sys):
    _,_,exe_tb = error_detail.exe_info()
    file_name = exe_tb.tb_frame.f_code.co_filename
    error_message = f"Error occured in python script [{file_name}] \n line Number [{exe_tb.lineno}]  \n error msg [{error}]"
    return error_message
class CustomException(Exception):
    def __init__ (self,error_message,error_detail:sys):
        super.__init__ (error_message) 
        self.error_message = error_message_detail(error_message,error_detail=error_detail)
    def __str__(self):
        return self.error_message 
    


