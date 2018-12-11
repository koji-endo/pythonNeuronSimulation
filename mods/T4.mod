: Lamina neuron model resembling Morris-Lecar neuron model by Lazar et al 2014
: conductance based model

NEURON {
  SUFFIX T4
  NONSPECIFIC_CURRENT il
  RANGE gl, el
}

UNITS {
    (mA) = (milliamp)
    (uA) = (microamp)
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
  gl = 10 (mS/cm2)
  el = -50 (mV)
}

BREAKPOINT {
  il = gl * (v - el)
}
