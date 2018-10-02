:ribbon synapse
:graded synaptic transmission based on presynaptic voltage

NEURON {
  POINT_PROCESS gsyn
  RANGE vpre
  RANGE vth, vre, k, gsat, n, g, numsyn
  NONSPECIFIC_CURRENT i
}

UNITS {
    (mA) = (milliamp)
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (S)  = (siemens)
    (uS) = (microsiemens)
    (nS) = (nanosiemens)
    (molar) = (1/liter)
    (mM)	= (millimolar)
    (nM)        = (nanomolar)
    FARADAY = (faraday) (coulomb)  :units are really coulombs/mole
    PI	= (pi) (1)
}

PARAMETER {
  vth = -80(mV)
  k = 20 (nS/mV)
  gsat = 800(nS)
  n = 1
  numsyn = 1
  vre = -80(mV)
}

ASSIGNED{
  v (mV)
  g (uS)
  i (nA)
  vpre (mV)
}

BREAKPOINT {
  if (vpre >= vth){
    g = k * pow((vpre - vth), n)
    if (g > gsat){
      g = gsat
    }
  }
  else {
    g = 0
  }
  i = g * (v - vre) * numsyn
}
