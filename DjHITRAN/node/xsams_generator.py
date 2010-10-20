# xsams_generator.py

def xsams_generator(transitions, states, molecules, sources):
    yield '<?xml version="1.0" encoding="UTF-8"?>\n'
    # the next line is for my convenience in validating the xml only:
    yield '<?oxygen NVDLSchema="XNXML.nvdl"?>'
    yield '<XSAMSData xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'

    yield '\n<Sources>\n'
    for source in sources:
        for line in source.xsams():
            yield line
    yield '</Sources>\n'

    yield '\n<States>\n'
    yield '  <Molecules>\n'
    for molecule in molecules:
        for molecule in molecules:
            for line in molecule.xsams():
                yield line
            molecID = molecule.molecid
            for state in states:
                if state.molecid == molecID:
                    for line in state.xsams():
                        yield line
            yield '      </Molecule>\n'
    yield '  </Molecules>\n'
    yield '</States>\n'

    yield '\n<Processes>\n'
    yield '<Radiative>\n'
    for transition in transitions:
        for line in transition.xsams():
            yield line
    yield '</Radiative>\n'
    yield '</Processes>\n'

    yield '</XSAMSData>\n'
