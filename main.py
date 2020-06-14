import phf

from com_input import DvachInput

phfsys = phf.PHFSystem()
phfsys.import_provider_sources("providers")
phfsys.import_hook_sources("hooks")
phfsys.add_input_source(DvachInput())

phfsys.start()
