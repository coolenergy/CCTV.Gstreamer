from typing import Union

from gi.repository import Gst

def must_link(ok: Union[bool, Gst.PadLinkReturn]):

    if isinstance(ok, bool):
        if not ok:
            raise RuntimeError('Error linking pads.')
        return

    elif isinstance(ok, Gst.PadLinkReturn):
        if ok != Gst.PadLinkReturn.OK:
            raise RuntimeError(f'Error linking pads. {ok}')
        return

    raise ValueError(f'No way to interpret link result from type {type(ok)}.')
