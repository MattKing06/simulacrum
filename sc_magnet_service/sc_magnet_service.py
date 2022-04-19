import asyncio

from caproto import ChannelType
from caproto.server import ioc_arg_parser, run, pvproperty, PVGroup
from lcls_tools.devices.scLinac import CRYOMODULE_OBJECTS

import simulacrum


class MagnetPV(PVGroup):
    bdes = pvproperty(value=0.0, name="BDES",
                      dtype=ChannelType.FLOAT)
    ctrl = pvproperty(value=0, name="CTRL", dtype=ChannelType.ENUM,
                      enum_strings=(
                          "Ready", "TRIM", "PERTURB", "BCON_TO_BDES", "SAVE_BDES", "LOAD_BDES", "UNDO_BDES", "DAC_ZERO",
                          "CALIB", "STDZ", "RESET", "TURN_ON", "TURN_OFF", "DEGAUSS"))


class SCMagnetService(simulacrum.Service):
    def __init__(self):
        super().__init__()

        quads = {}
        xcors = {}
        ycors = {}

        for cm in CRYOMODULE_OBJECTS.values():
            quads[cm.quad.pvprefix] = MagnetPV(prefix=cm.quad.pvprefix)
            xcors[cm.xcor.pvprefix] = MagnetPV(prefix=cm.xcor.pvprefix)
            ycors[cm.ycor.pvprefix] = MagnetPV(prefix=cm.ycor.pvprefix)

        self.add_pvs(quads)
        self.add_pvs(xcors)
        self.add_pvs(ycors)


def main():
    service = SCMagnetService()
    asyncio.get_event_loop()
    _, run_options = ioc_arg_parser(
        default_prefix='',
        desc="Simulated SC Magnet Service")
    run(service, **run_options)


if __name__ == '__main__':
    main()
