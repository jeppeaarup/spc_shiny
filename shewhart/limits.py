from dataclasses import dataclass
from common import CalibrationStats

@dataclass
class ShewhartLimits:
    """Center line and control/warning limits for a Shewhart chart."""
    center: float
    ucl: float
    lcl: float
    uwl: float
    lwl: float


def compute_limits(cal_stats: CalibrationStats, k_warning: float = 2, k_control: float = 3) -> ShewhartLimits:
    """Compute Shewhart control/warning limits from calibration stats."""
    std = cal_stats.std
    mean = cal_stats.mean
    control_spacer = k_control * std
    warning_spacer = k_warning * std
    return ShewhartLimits(
        center=mean,
        ucl=mean + control_spacer,
        lcl=mean - control_spacer,
        uwl=mean + warning_spacer,
        lwl=mean - warning_spacer
    )