from cx_Freeze import setup, Executable
 
setup(
    name = "MyApp" ,
    version = "0.1" ,
    description = "test" ,
    executables = [Executable("main.py")] ,
    )