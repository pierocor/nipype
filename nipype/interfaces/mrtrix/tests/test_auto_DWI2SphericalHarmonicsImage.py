# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.mrtrix.tensors import DWI2SphericalHarmonicsImage
def test_DWI2SphericalHarmonicsImage_inputs():
    input_map = dict(out_filename=dict(position=-1,
    genfile=True,
    argstr='%s',
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    args=dict(argstr='%s',
    ),
    maximum_harmonic_order=dict(argstr='-lmax %s',
    ),
    normalise=dict(position=3,
    argstr='-normalise',
    ),
    terminal_output=dict(mandatory=True,
    nohash=True,
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(position=-2,
    mandatory=True,
    argstr='%s',
    ),
    encoding_file=dict(position=1,
    mandatory=True,
    argstr='-grad %s',
    ),
    )
    inputs = DWI2SphericalHarmonicsImage.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value
def test_DWI2SphericalHarmonicsImage_outputs():
    output_map = dict(spherical_harmonics_image=dict(),
    )
    outputs = DWI2SphericalHarmonicsImage.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value