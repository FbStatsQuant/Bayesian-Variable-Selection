"""Read current memory and inherited job limits for execution evidence; no mutation."""
import os
import platform


def memory_limits():
    if platform.system()!="Windows":
        import resource
        return dict(platform=platform.system(),address_space_limit=resource.getrlimit(resource.RLIMIT_AS))
    import ctypes as c
    from ctypes import wintypes as w
    class Memory(c.Structure):
        _fields_=[("length",w.DWORD),("load_percent",w.DWORD)]+[(name,c.c_ulonglong) for name in
            ("total_physical","available_physical","total_commit","available_commit","total_virtual","available_virtual","available_extended_virtual")]
    class Basic(c.Structure):
        _fields_=[("per_process_time",c.c_longlong),("per_job_time",c.c_longlong),("flags",w.DWORD),
            ("min_working_set",c.c_size_t),("max_working_set",c.c_size_t),("active_process_limit",w.DWORD),
            ("affinity",c.c_size_t),("priority",w.DWORD),("scheduling_class",w.DWORD)]
    class IO(c.Structure):
        _fields_=[(name,c.c_ulonglong) for name in ("read_operations","write_operations","other_operations","read_bytes","write_bytes","other_bytes")]
    class Extended(c.Structure):
        _fields_=[("basic",Basic),("io",IO),("process_memory_limit",c.c_size_t),("job_memory_limit",c.c_size_t),
            ("peak_process_memory",c.c_size_t),("peak_job_memory",c.c_size_t)]
    kernel=c.WinDLL("kernel32",use_last_error=True)
    kernel.GetCurrentProcess.restype=c.c_void_p
    kernel.IsProcessInJob.argtypes=[c.c_void_p,c.c_void_p,c.POINTER(w.BOOL)]
    kernel.QueryInformationJobObject.argtypes=[c.c_void_p,c.c_int,c.c_void_p,w.DWORD,c.POINTER(w.DWORD)]
    kernel.GlobalMemoryStatusEx.argtypes=[c.POINTER(Memory)]
    state=Memory();state.length=c.sizeof(Memory)
    result=dict(platform=platform.platform(),pid=os.getpid())
    if kernel.GlobalMemoryStatusEx(c.byref(state)):
        result["memory_bytes"]={name:getattr(state,name) for name,_ in Memory._fields_ if name not in {"length","load_percent"}}
        result["memory_load_percent"]=state.load_percent
    inside=w.BOOL()
    if kernel.IsProcessInJob(kernel.GetCurrentProcess(),None,c.byref(inside)):
        result["in_job"]=bool(inside.value)
        if inside.value:
            limits=Extended()
            if kernel.QueryInformationJobObject(None,9,c.byref(limits),c.sizeof(limits),None):
                result["job_limits"]={"flags":limits.basic.flags,"process_memory_limit":limits.process_memory_limit,
                    "job_memory_limit":limits.job_memory_limit,"active_process_limit":limits.basic.active_process_limit,
                    "max_working_set":limits.basic.max_working_set,"peak_job_memory":limits.peak_job_memory}
            else: result["job_query_winerror"]=c.get_last_error()
    else: result["job_membership_winerror"]=c.get_last_error()
    return result
