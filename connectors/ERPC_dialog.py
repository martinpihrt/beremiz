#!/usr/bin/env python
# -*- coding: utf-8 -*-

# See COPYING file for copyrights details.



from itertools import repeat, islice, chain

from connectors.SchemeEditor import SchemeEditor


model = [('host', _("Host:")),
         ('port', _("Port:"))]

# (scheme, model, secure)
models = [("LOCAL", [], False), ("ERPC", model, False)]

Schemes = list(zip(*models))[0]

_PerSchemeConf = {sch: (mod, sec) for sch, mod, sec in models}


class ERPC_dialog(SchemeEditor):
    def __init__(self, scheme, *args, **kwargs):
        # ID selector is enabled only on ERPC (secure)
        self.model, self.EnableIDSelector = _PerSchemeConf[scheme]

        SchemeEditor.__init__(self, scheme, *args, **kwargs)

    # pylint: disable=unused-variable
    def SetLoc(self, loc):
        hostport, ID = list(islice(chain(loc.split("#"), repeat("")), 2))
        host, port = list(islice(chain(hostport.split(":"), repeat("")), 2))
        self.SetFields(locals())

    def GetLoc(self):
        if self.model:
            fields = self.GetFields()
            template = "{host}"
            if fields['port']:
                template += ":{port}"
            if self.EnableIDSelector:
                if fields['ID']:
                    template += "#{ID}"

            return template.format(**fields)
        return ''
