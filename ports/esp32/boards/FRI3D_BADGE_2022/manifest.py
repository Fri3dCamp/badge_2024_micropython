include("$(PORT_DIR)/boards/FRI3D_BADGE_COMMON/manifest.py")

module("lis2hh12.py", base_path="$(MPY_DIR)/micropython-lis2hh12")
module("lis2hh12_int.py", base_path="$(MPY_DIR)/driver/lis2hh12_int")
