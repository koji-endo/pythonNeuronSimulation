: test FitzHugh-Nagumo model

NEURON {
  SUFFIX fhn
  RANGE a, b, tau
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
 iext
}

PARAMETER {
  a = 0.7
  b = 0.8
  tau = 1000
}

STATE {
  w
  v
}

BREAKPOINT {
  SOLVE states METHOD derivimplicit
}

INITIAL {
  v = 0
  w = 0
}

DERIVATIVE states {
  v' = v - v^3 - w + iext
  w' = (v - a - b*w) / tau
}
