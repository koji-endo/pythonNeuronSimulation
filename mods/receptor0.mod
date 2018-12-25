: photo insensitive cell membrane model by Niven 2003
: conductance based model

NEURON {
  SUFFIX receptor2
  NONSPECIFIC_CURRENT il
  RANGE gl, el
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S)  = (siemens)
    (molar) = (1/liter)
    (mM)	= (millimolar)
    (nM)        = (nanomolar)
    FARADAY = (faraday) (coulomb)  :units are really coulombs/mole
    PI	= (pi) (1)
}

ASSIGNED{
 v (mV)
 il (mA/cm2)
}

PARAMETER {
  gl = 0.006 (mS/cm2)
  el = -48 (mV)
}

BREAKPOINT {
  il = gl * (v - el)
}
